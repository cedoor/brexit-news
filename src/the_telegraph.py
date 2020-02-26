import os

import src.utils as utils

website_base_url = "https://www.telegraph.co.uk"
website_url = website_base_url + "/brexit/page-"
number_of_pages = 367


def get_body_content(body):
    content = ""

    for paragraph in body.select("p"):
        content += "\n" + paragraph.get_text()

    return content


def start():
    file_name = os.path.splitext(os.path.basename(__file__))[0]
    articles = utils.open_data(file_name)

    print()
    utils.progress(0)

    for page_number in range(1, number_of_pages + 1):
        main_page = utils.scrape_page(website_url + str(page_number))

        article_anchors = main_page.select("article a.list-headline__link")

        for j, article_anchor in enumerate(article_anchors):
            article_url = article_anchor.get('href')
            article_url = website_base_url + article_url

            if utils.article_exist(articles, article_url) or utils.is_404(article_url):
                continue

            article_page = utils.scrape_page(article_url)

            if article_page.select_one("h1.headline__heading") is not None:
                article_title = article_page.select_one("h1.headline__heading").get_text()
            elif article_page.select_one("h1.e-headline") is not None:
                article_title = article_page.select_one("h1.e-headline").get_text()
            else:   # In this case is not a conventional article, like https://www.telegraph.co.uk/politics/2019/12/12/general-election-polls-tracker-latest-uk-odds-2019-opinion-poll/
                continue

            # In this case is not an useful article
            if article_page.select_one("article") is None:
                continue

            article_body = get_body_content(article_page.select_one("article"))

            if article_page.select_one(".article-date time") is not None:
                article_date = article_page.select_one(".article-date time")["datetime"]
            elif article_page.select_one(".article__byline-date time") is not None:
                article_date = article_page.select_one(".article__byline-date time")["datetime"]
            else:   # In this case is not a conventional article, like https://www.telegraph.co.uk/politics/2019/12/12/will-election-results-declared-area-timetable-night/
                continue

            article_timestamp = utils.datetime_to_timestamp(article_date)

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
        
        utils.progress(page_number / number_of_pages * 100)

    utils.summary(file_name, articles)