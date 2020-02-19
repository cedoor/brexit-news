import json
import sys
from os import path, makedirs
from urllib.error import URLError
from urllib.request import urlopen, Request

import dateutil.parser as date_parser
from bs4 import BeautifulSoup


def scrape_page(url):
    # To see available User-Agent, go to http://httpbin.org/get.
    request = Request(url, headers={"User-Agent": "Chrome/79.0.3945.117"})

    return BeautifulSoup(urlopen(request), features="html.parser")


def get_api_key(file_name, url_api_access):
    api_keys_path = "./.api_keys"
    file_path = "%s/.%s" % (api_keys_path, file_name)

    if path.exists(file_path):
        file = open(file_path, "r")
        print("Using stored API for %s" % (file_name))
        print()
        return file.read()
    
    api_key = input("Insert a valid API key for %s (%s): " % (file_name, url_api_access))
    print()
    
    if not path.exists(api_keys_path):
        makedirs(api_keys_path)
   
    file = open(file_path, "w+")
    file.write(api_key)
    
    print("API key for %s stored" % (file_name))
    print()
    return api_key


def is_404(url):
    # To see available User-Agent, go to http://httpbin.org/get.
    request = Request(url, headers={"User-Agent": "Chrome/79.0.3945.117"})
    try:
        urlopen(request)
    except URLError:
        return True

    return False


def data_path(file_name):
    return "./data/" + file_name + ".json"


def article_exist(articles, url):
    for article in articles:
        if article["url"] == url:
            return True
        
    return False


def datetime_to_timestamp(datetime):
    return int(date_parser.parse(datetime).timestamp())


def open_data(file_name):
    file_path = data_path(file_name)

    if not path.exists(file_path):
        print("Creating data/%s.json file...\n" % (file_name))
        return []

    with open(file_path, "r") as fp:
        articles = json.load(fp)
    
    # Remove unuseful or broken articles
    for article in articles:
        if not article["title"] or not article["url"] or not article["timestamp"] or not article["content"]:
            articles.remove(article)


    print("Updating data/%s.json file..." % (file_name))
    return articles


def save_data(file_name, data):
    file_path = data_path(file_name)

    with open(file_path, "w") as fp:
        json.dump(data, fp, indent=4, ensure_ascii=False)


def summary(file_name, data):
    print("\n\n✔ %d articles saved in data/%s.json file!" % (len(data), file_name))


def progress(i):
    sys.stdout.write("\r%d%%" % i)
    sys.stdout.flush()
