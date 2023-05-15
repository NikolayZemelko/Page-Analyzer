import os

from dotenv import load_dotenv
from datetime import datetime

import psycopg2
from psycopg2.extras import DictCursor

from flask import Flask, request, render_template, redirect, \
    url_for, flash, get_flashed_messages

import requests

from page_analyzer.checkUrl import valid_url, normalize_url
from page_analyzer.parseUrlData import parse_url_data


load_dotenv()
app = Flask(__name__)
DATABASE_URL = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def get_start():
    return render_template(
        'index.html'
    )


@app.route('/urls')
def get_urls():

    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT DISTINCT ON (url_id) "
                        "urls.id AS id, "
                        "urls.name AS name, "
                        "url_checks.created_at AS date, "
                        "url_checks.status_code AS status_code "
                        "FROM urls "
                        "LEFT JOIN url_checks "
                        "ON urls.id = url_checks.url_id "
                        "ORDER BY url_id DESC, url_checks.id DESC;")
            urls = cur.fetchall()

    return render_template(
        'urls/index.html',
        urls=urls
    )


@app.route('/urls/<id>')
def get_url(id):

    url = dict()
    with psycopg2.connect(os.getenv('DATABASE_URL')) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id=%s", (id,))
            url = cur.fetchone()
            cur.execute("SELECT * FROM url_checks "
                        "WHERE url_id=%s ORDER BY id DESC;", (id,))
            checks = cur.fetchall()

    return render_template(
        'url/index.html',
        messages=get_flashed_messages(with_categories=True),
        url=url,
        checks=checks
    )


@app.route('/urls', methods=['POST'])
def post_url():

    url = request.form.get('url')
    normalized_url = normalize_url(url)

    if not normalized_url:
        flash('URL обязателен', 'error')

    validated_url = valid_url(normalized_url)

    if not validated_url:
        flash('Некорректный URL', 'error')
        messages = sorted(get_flashed_messages(with_categories=True),
                          key=lambda message: message[0] == 'error',
                          reverse=True)

        return render_template(
            'index.html',
            messages=messages,
        ), 422

    with psycopg2.connect(os.getenv('DATABASE_URL')) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:

            cur.execute("SELECT * FROM urls WHERE name=%s", (normalized_url,))
            already_exist = cur.fetchone()

            if not already_exist:
                cur.execute("INSERT INTO urls (name, created_at) "
                            "VALUES (%s, %s);",
                            (normalized_url, datetime.now()))
                conn.commit()

                with open('./database.sql', 'a') as database_sql:
                    database_sql.write('\n' + str(cur.query)[2:-1])

                flash('Страница успешно добавлена', 'success')
            else:

                flash('Страница уже существует', 'message')

            cur.execute('SELECT id FROM urls WHERE name=%s', (normalized_url,))
            id = cur.fetchone()[0]
            print(id)

    return redirect(url_for('get_url', id=id))


@app.route('/urls/<id>', methods=['POST'])
def get_checks_url(id):

    with psycopg2.connect(os.getenv('DATABASE_URL')) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:

            cur.execute("SELECT * FROM urls WHERE id=%s", (id,))
            url = cur.fetchone()
            url_name = url.get('name')

            try:
                r = requests.get(url_name)
                url_data = parse_url_data(url_name)

                h1 = url_data.get('h1')
                title = url_data.get('title')
                desc = url_data.get('description')
                status_code = r.status_code

                cur.execute("INSERT INTO url_checks "
                            "(url_id, created_at, status_code, h1, title, description) "  # noqa E501
                            "VALUES (%s, %s, %s, %s, %s, %s);",
                            (id, datetime.now(), status_code, h1, title, desc))
                conn.commit()
                cur.execute("SELECT * FROM url_checks "
                            "WHERE url_id=%s ORDER BY id DESC;", (id,))
                checks = cur.fetchall()

                flash('Страница успешно проверена', 'success')
            except requests.ConnectionError:
                checks = None
                flash('Произошла ошибка при проверке', 'error')

    return render_template(
        'url/index.html',
        checks=checks,
        messages=get_flashed_messages(with_categories=True),
        url=url
    )
