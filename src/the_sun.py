import os

import src.utils as utils

website_url = "https://www.thesun.co.uk/news/brexit/page/"
number_of_pages = 88


def get_body_content(body):
    content = ""

    for paragraph in body.select("p"):
        paragraph_text = paragraph.get_text()
        if "We pay for your stories!" not in paragraph_text:
            content += "\n" + paragraph_text

    return content


def start():
    articles = []

    utils.progress(0)

    for page_number in range(1, number_of_pages + 1):
        main_page = utils.scrape_page(website_url + str(page_number))

        article_anchors = main_page.select(".teaser-item a.teaser-anchor")

        for j, article_anchor in enumerate(article_anchors):
            article_url = article_anchor.get('href')

            article_page = utils.scrape_page(article_url)

            article_title = article_page.select_one("h1.article__headline").get_text()
            article_body = get_body_content(article_page.select_one(".article__content"))

            article_date = article_page.select_one(".article__published span").string
            article_date += article_page.select_one(".article__timestamp").string
            article_timestamp = utils.datetime_to_timestamp(article_date)

            articles.append({
                "title": article_title,
                "url": article_url,
                "timestamp": article_timestamp,
                "content": article_body
            })

        utils.progress(page_number / number_of_pages * 100)

    # Save all articles in a file.
    utils.save_data(os.path.splitext(os.path.basename(__file__))[0], articles)
