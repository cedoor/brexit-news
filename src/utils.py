import json
from urllib.request import urlopen

from bs4 import BeautifulSoup


def get_page(url):
    return BeautifulSoup(urlopen(url).read(), features="html.parser")


def get_body_content(body):
    content = ""

    for paragraph in body.select("p"):
        content += "\n" + paragraph.get_text()

    return content


def save_data(file_name, data):
    with open("../data/" + file_name + ".json", 'w') as fp:
        json.dump(data, fp, indent=True)
