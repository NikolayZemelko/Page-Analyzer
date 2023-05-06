from bs4 import BeautifulSoup
import requests


def parse_url_data(url):

    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    h1 = '' if soup.h1 is None else soup.h1.get_text()
    title = '' if soup.title is None else soup.title.get_text()
    content_raw = soup.find("meta", recursive=True, attrs={'name': 'description'})
    content = '' if content_raw is None else content_raw['content']

    return {
        'h1': h1,
        'title': title,
        'description': content
        }
