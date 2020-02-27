import os
import sys
import json
import requests

import src.utils as utils

url_api_access = "https://open-platform.theguardian.com/access/"

api_endpoint = "https://content.guardianapis.com/search"

def request_articles(page_number, api_key):
    return requests.get(api_endpoint, {
                "tag": "politics/eu-referendum",
                "section": "politics",
                "order-by": "newest",
                "show-fields": "trailText,bodyText,wordcount,publication",
                "page-size": 200,
                "page": page_number,
                "api-key": api_key
            }).json()["response"]


def start():
    file_name = os.path.splitext(os.path.basename(__file__))[0]
    api_key = utils.get_api_key(file_name, url_api_access)
    articles = utils.open_data(file_name)
    page_number = 1

    print()
    utils.progress_bar(0, 100)

    while True:
        try:
            # Get the request response passing all API parameters.
            response = request_articles(page_number, api_key)
        except KeyError:
            sys.stdout.write("\rSeems like your API key for %s is invalid" % (file_name))
            print("\nStored API key: %s" % (api_key))

            api_key = utils.set_api_key(file_name, url_api_access)

            # Get the request response passing all API parameters.
            response = request_articles(page_number, api_key)


        # Map from request response to standard data JSON structure.
        temp_articles = list(map(lambda d: {
            "title": d["webTitle"],
            "url": d["webUrl"],
            "timestamp": utils.datetime_to_timestamp(d["webPublicationDate"]),
            "content": d["fields"]["bodyText"]
        }, response["results"]))


        # Remove unuseful or broken articles
        for article in temp_articles[:]: # note the [:] creates a slice
            if utils.article_exist(articles, article["url"]):
                temp_articles.remove(article)
            elif not article["title"] or not article["url"] or not article["timestamp"] or not article["content"]:
                temp_articles.remove(article)


        if page_number == response["pages"]:
            break

        page_number += 1

        utils.progress_bar(page_number, response["pages"])

        if not temp_articles:
            continue
        else:
            articles += temp_articles

            # Save articles in a file.
            utils.save_data(file_name, articles)
    
    utils.summary(file_name, articles)
