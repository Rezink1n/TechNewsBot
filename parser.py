from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

from news_database import add_news_db

ua = UserAgent()

site = 'ixbt.com'
url = f'https://www.{site}/news'
headers = {'user-agent': f'{ua.random}'}


def add_news():
    print('h', end='')
    req = requests.get(url, headers)
    src = req.text
    print('n', end='')
    big_temp_list = []
    soup = BeautifulSoup(src, 'lxml')
    try:
        news = soup.find(class_='mobb mobb2').find_parent().find_all(class_='item')
    except:
        news = soup.find(class_='mobb mobb2').find_all(class_='item')
    for item in news:
        news_time = item.find('span', class_='time_iteration_icon_light').text
        try:
            news_a = item.find('a', class_='comments_link').find_next('a')
        except:
            news_a = item.find('a')
        news_name_bold = news_a.find('strong').text
        news_name_slim = news_a.text[len(news_name_bold):]
        news_href = 'https://www.ixbt.com' + news_a.get('href')
        temp_list = [news_time, news_name_bold, news_name_slim, news_href]
        big_temp_list.append(temp_list)
    for tl in big_temp_list:
        add_news_db(tl[0], tl[1], tl[2], tl[3])


def main():
    pass


if __name__ == '__main__':
    main()
