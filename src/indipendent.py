import os
from datetime import date, timedelta

import src.utils as utils

website_url = "https://www.independent.co.uk"
archive_url = website_url + "/archive/"
        

def get_body_content(article_page, article_url):
    content = ""

    if article_page.select_one(".body-content") is not None:
        body = article_page.select_one(".body-content")
    elif article_page.select_one(".text-wrapper") is not None:
        body = article_page.select_one(".text-wrapper")
    elif article_page.select_one(".m-detail--body") is not None:
        body = article_page.select_one(".m-detail--body")
    else:   # content not found
        return content

    for paragraph in body.select("p"):
        content += "\n" + paragraph.get_text()
    
    return content


def start():
    file_name = os.path.splitext(os.path.basename(__file__))[0]
    articles = utils.open_data(file_name)
    
    print()
    utils.progress(0)

    start_date = date(2016, 1, 1)
    end_date = date.today()

    delta = end_date - start_date       # as timedelta

    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        archive_date_url = archive_url + str(day)

        archive_date_page = utils.scrape_page(archive_date_url)

        archive = archive_date_page.select_one(".archive")
        archive_articles = archive.find_all("h2")

        for j, article in enumerate(archive_articles):
            article_title = article.get_text()
            article_url = website_url + article.select_one("a").get("href")

            if "brexit" not in article_title.lower():
                continue
            
            if utils.article_exist(articles, article_url) or utils.is_404(article_url):
                continue

            article_page = utils.scrape_page(article_url)

            if article_page.select_one("amp-timeago") is not None:
                article_date = article_page.select_one("amp-timeago").get("datetime")
            elif article_page.select_one("time") is not None:
                article_date = article_page.select_one("time").get("datetime")
            else:
                continue
            
            article_timestamp = utils.datetime_to_timestamp(article_date)

            article_body = get_body_content(article_page, article_url)
            if not article_body:
                continue
                
            articles.append({
                "title": article_title,
                "url": article_url,
                "timestamp": article_timestamp,
                "content": article_body
            })

            # Save articles in a file.
            utils.save_data(file_name, articles)

        utils.progress(i / (delta.days + 1) * 100)

    utils.summary(file_name, articles)
