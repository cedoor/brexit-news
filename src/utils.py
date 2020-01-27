import json
import sys
from urllib.request import urlopen

from bs4 import BeautifulSoup

import dateutil.parser as dp

def scrape_page(url):
    return BeautifulSoup(urlopen(url).read(), features="html.parser")


def datetime_to_timestamp(datetime):
    return int(dp.parse(datetime).timestamp())


def save_data(file_name, data):
    with open("./data/" + file_name + ".json", 'w') as fp:
        json.dump(data, fp, indent=4, ensure_ascii=False)
    print("\n\n✔ %d articles saved in data/%s.json file!" % (len(data), file_name))


def progress(i):
    sys.stdout.write("\r%d%%" % i)
    sys.stdout.flush()
