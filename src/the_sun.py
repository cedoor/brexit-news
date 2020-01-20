import src.utils as utils


def get_body_content(body):
    content = ""

    for paragraph in body.select("p"):
        paragraph_text = paragraph.get_text()
        if "We pay for your stories!" not in paragraph_text:
            content += "\n" + paragraph_text

    return content


def start():
    articles = []

    for page_number in range(1, 89):
        main_page = utils.scrape_page("https://www.thesun.co.uk/news/brexit/page/" + str(page_number))

        article_anchors = main_page.select(".teaser-item a.teaser-anchor")

        for j, article_anchor in enumerate(article_anchors):
            article_url = article_anchor.get('href')

            article_page = utils.scrape_page(article_url)

            print(article_url)
            article_title = article_page.select_one("h1.article__headline").string
            article_body = get_body_content(article_page.select_one(".article__content"))

            article_date = article_page.select_one(".article__datestamp").string
            article_date += article_page.select_one(".article__timestamp").string

            articles.append({
                "title": article_title,
                "content": article_body,
                "url": article_url,
                "date": article_date
            })

        utils.progress(page_number / 88 * 100)

    utils.save_data("the_sun", articles)
