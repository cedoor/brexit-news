from os import environ

import requests

import src.utils as utils


def start():
    api_endpoint = "http://content.guardianapis.com/search"
    api_key = environ["GUARDIAN_API_KEY"]

    all_data = []
    page_number = 1

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
        all_data = all_data + list(map(lambda d: {
            "title": d["webTitle"],
            "url": d["webUrl"],
            "date": d["webPublicationDate"],
            "content": d["fields"]["bodyText"]
        }, response["results"]))

        if page_number == response["pages"]:
            break

        page_number += 1

        utils.progress(page_number / response["pages"] * 100)

    # Save all data in a file.
    utils.save_data("theGuardian", all_data)
