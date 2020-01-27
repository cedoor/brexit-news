import json
import sys
from urllib.request import urlopen as uReq, Request

from bs4 import BeautifulSoup

import dateutil.parser as dp

def scrape_page(url):
    req = Request(url, headers = {'User-Agent': 'Chrome/79.0.3945.117'}) #To see avaiable User-Agent, go to http://httpbin.org/get
    page = uReq(req)
    return BeautifulSoup(page, features="html.parser")


def is_404(url):
    req = Request(url, headers = {'User-Agent': 'Chrome/79.0.3945.117'}) #To see avaiable User-Agent, go to http://httpbin.org/get
    try:
        page = uReq(req)
    except:
        return True
    
    return False


def datetime_to_timestamp(datetime):
    return int(dp.parse(datetime).timestamp())


def save_data(file_name, data):
    with open("./data/" + file_name + ".json", 'w') as fp:
        json.dump(data, fp, indent=4, ensure_ascii=False)
    print("\n\n✔ %d articles saved in data/%s.json file!" % (len(data), file_name))


def progress(i):
    sys.stdout.write("\r%d%%" % i)
    sys.stdout.flush()
