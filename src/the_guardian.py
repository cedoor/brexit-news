import os
import json
import requests

import src.utils as utils

url_api_access = "https://open-platform.theguardian.com/access/"

api_endpoint = "https://content.guardianapis.com/search"


def start():
    file_name = os.path.splitext(os.path.basename(__file__))[0]
    api_key = utils.get_api_key(file_name, url_api_access)
    articles = utils.open_data(file_name)
    page_number = 1

    print()
    utils.progress(0)

    while True:
        # Get the request response passing all API parameters.
        response = requests.get(api_endpoint, {
            "tag": "politics/eu-referendum",
            "section": "politics",
            "order-by": "newest",
            "show-fields": "trailText,bodyText,wordcount,publication",
            "page-size": 200,
            "page": page_number,
            "api-key": api_key
        }).json()["response"]


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

        utils.progress(page_number / response["pages"] * 100)

        if not temp_articles:
            continue
        else:
            articles += temp_articles

            # Save articles in a file.
            utils.save_data(file_name, articles)
    
    utils.summary(file_name, articles)
