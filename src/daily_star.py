import os

import src.utils as utils

website_url = "https://www.dailystar.co.uk/latest/brexit?pageNumber="
number_of_pages = 88


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

        article_anchors = main_page.select(".teaser a.headline")

        for j, article_anchor in enumerate(article_anchors):
            article_url = article_anchor.get('href')

            if utils.article_exist(articles, article_url) or utils.is_404(article_url):
                continue

            article_page = utils.scrape_page(article_url)

            article_title = article_page.select_one("h1.section-theme-background-indicator").get_text()
            
            # In this case is not an useful article, like
            # https://www.dailystar.co.uk/news/latest-news/eu-referendum-live-blog-vote-17096947
            if article_page.select_one(".article-body") is None:
                continue
            
            article_body = get_body_content(article_page.select_one(".article-body"))

            if article_page.select_one(".date-published") is not None:
                article_date = article_page.select_one(".date-published")["datetime"]
            else:
                article_date = article_page.select_one(".date-updated").string
            article_timestamp = utils.datetime_to_timestamp(article_date)

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
