import json
import sys
from urllib.error import URLError
from urllib.request import urlopen, Request

import dateutil.parser as date_parser
from bs4 import BeautifulSoup


def scrape_page(url):
    # To see available User-Agent, go to http://httpbin.org/get.
    request = Request(url, headers={"User-Agent": "Chrome/79.0.3945.117"})

    return BeautifulSoup(urlopen(request), features="html.parser")


def is_404(url):
    # To see available User-Agent, go to http://httpbin.org/get.
    request = Request(url, headers={"User-Agent": "Chrome/79.0.3945.117"})
    try:
        urlopen(request)
    except URLError:
        return True

    return False


def datetime_to_timestamp(datetime):
    return int(date_parser.parse(datetime).timestamp())


def save_data(file_name, data):
    with open("./data/" + file_name + ".json", "w") as fp:
        json.dump(data, fp, indent=4, ensure_ascii=False)

    print("\n\n✔ %d articles saved in data/%s.json file!" % (len(data), file_name))


def progress(i):
    sys.stdout.write("\r%d%%" % i)
    sys.stdout.flush()
