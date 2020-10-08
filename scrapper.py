import requests
from bs4 import BeautifulSoup

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
URL = 'https://habr.com/ru/all/'

def is_desired(article, keywords):
    article_id = article.parent.attrs.get('id')
    # если идентификатор не найден, это что-то странное, пропускаем
    if not article_id:
        return False

    title = article.find('a', class_='post__title_link')
    title_text_low = title.text.lower()

    hubs = article.find_all('a', class_='hub-link')
    hubs_text_low = ', '.join([hub_elem.text.lower() for hub_elem in hubs])

    article_body = article.find('div', class_='post__text')
    article_text_low = article_body.text.lower()

    for keyword in keywords:
        if keyword in title_text_low or keyword in hubs_text_low or keyword in article_text_low:
            return keyword

def get_article_description(article):
    title_element = article.find('a', class_='post__title_link')
    date_element = article.find('span', class_='post__time')
    href = title_element.attrs.get('href')
    return f"{date_element.text} - {title_element.text} - {href}"

def check_hubr_articles(keywords):
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.find_all('article', class_='post')
    for article in articles:
        keyword = is_desired(article, keywords)
        if keyword:
            print(f"По ключу '{keyword}' найдена статья: {get_article_description(article)}")

if __name__ == '__main__':
    check_hubr_articles(KEYWORDS)