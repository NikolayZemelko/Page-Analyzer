import os
import psycopg2

from psycopg2.extras import DictCursor
from flask import Flask, request, render_template, redirect, \
    url_for, flash, get_flashed_messages
from datetime import datetime
from page_analyzer.validator import valid_url
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def get_start():
    return render_template(
        'index.html'
    )


@app.route('/urls')
def get_urls():

    with psycopg2.connect(os.getenv('DATABASE_URL')) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT urls.id AS id, urls.name AS name, MAX(url_checks.created_at) AS date "
                        "FROM urls JOIN url_checks ON urls.id = url_checks.url_id GROUP BY urls.id;")
            urls_dict = cur.fetchall()
            sorted_urls_dict = sorted(urls_dict,
                                      key=lambda url: url[0],
                                      reverse=True)

    return render_template(
        'urls/index.html',
        urls=sorted_urls_dict
    )


@app.route('/urls/<id>')
def get_url(id):

    url = dict()
    with psycopg2.connect(os.getenv('DATABASE_URL')) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id=%s", (id,))
            url = cur.fetchone()

    return render_template(
        'url/index.html',
        messages=get_flashed_messages(with_categories=True),
        url=url
    )


@app.route('/urls', methods=['POST'])
def post_url():

    url = request.form.get('url')
    if not url:
        flash('URL обязателен', 'error')

    valid = valid_url(url)

    if not valid:
        flash('Некорректный URL', 'error')
        messages = sorted(get_flashed_messages(with_categories=True),
                          key=lambda message: message[0] == 'error',
                          reverse=True)

        return render_template(
            'index.html',
            messages=messages,
        )

    with psycopg2.connect(os.getenv('DATABASE_URL')) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:

            cur.execute("SELECT * FROM urls WHERE name=%s", (url,))
            already_exist = cur.fetchone()

            if not already_exist:
                cur.execute("INSERT INTO urls (name, created_at) "
                            "VALUES (%s, %s);",
                            (url, datetime.now()))
                conn.commit()

                with open('./database.sql', 'a') as database_sql:
                    database_sql.write('\n' + str(cur.query)[2:-1])

                flash('Страница успешно добавлена', 'success')
            else:

                flash('Страница уже существует', 'message')

            cur.execute('SELECT id FROM urls WHERE name=%s', (url,))
            id = cur.fetchone()[0]

    return redirect(url_for('get_url', id=id))


@app.route('/urls/<id>/checks', methods=['POST'])
def get_checks_url(id):

    with psycopg2.connect(os.getenv('DATABASE_URL')) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("INSERT INTO url_checks (url_id, created_at) "
                        "VALUES (%s, %s);", (id, datetime.now(),))
            conn.commit()
            cur.execute("SELECT id, created_at FROM url_checks WHERE url_id=%s;", (id,))
            check = cur.fetchone()
            cur.execute("SELECT * FROM urls WHERE id=%s", (id,))
            url = cur.fetchone()
            flash('Страница успешно проверена', 'success')
    return render_template(
        'url/index.html',
        check=check,
        messages=get_flashed_messages(with_categories=True),
        url=url
    )
