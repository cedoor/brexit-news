import os

import requests

import src.utils as utils

api_endpoint = "http://content.guardianapis.com/search"
api_key = os.environ["GUARDIAN_API_KEY"]


def start():
    articles = []
    page_number = 1

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
        articles = articles + list(map(lambda d: {
            "title": d["webTitle"],
            "url": d["webUrl"],
            "timestamp": utils.datetime_to_timestamp(d["webPublicationDate"]),
            "content": d["fields"]["bodyText"]
        }, response["results"]))

        if page_number == response["pages"]:
            break

        page_number += 1

        utils.progress(page_number / response["pages"] * 100)

    # Save all articles in a file.
    utils.save_data(os.path.splitext(os.path.basename(__file__))[0], articles)
