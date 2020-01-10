import src.utils as utils


def start():
    page = utils.get_page("https://www.theguardian.com/politics/eu-referendum/all")

    articles = []

    article_anchors = page.select("section .fc-item__container > a")

    number_of_articles = len(article_anchors)

    print("")

    for i, article_anchor in enumerate(article_anchors):
        page = utils.get_page(article_anchor.get('href'))

        article_body = page.select_one("article .content__article-body")

        if article_body is not None:
            articles.append({
                "title": page.select_one("article .content__header .content__headline").string,
                "content": utils.get_body_content(article_body)
            })

        utils.progress((i + 1) / number_of_articles * 100)

    utils.save_data("guardian", articles)

    print("\n\nData saved in data/guardian.json file!")
