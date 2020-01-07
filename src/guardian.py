import src.utils as utils

page = utils.get_page("https://www.theguardian.com/politics/eu-referendum/all")

articles = []

for article_anchor in page.select("section .fc-item__container > a"):
    page = utils.get_page(article_anchor.get('href'))

    article_body = page.select_one("article .content__article-body")

    if article_body is not None:
        articles.append({
            "title": page.select_one("article .content__header .content__headline").string,
            "content": utils.get_body_content(article_body)
        })

utils.save_data("guardian", articles)
