import requests
from bs4 import BeautifulSoup

url = "https://www.hindustantimes.com/"


def return_full_news_data(logger=None):
    if logger:
        logger.info("Requesting URL")

    response = requests.get(url)

    if logger:
        logger.info(str(response))
        logger.info('Making Soup Object ...')

    soup = BeautifulSoup(response.content, 'html5lib')

    if logger:
        logger.info("Soup Object Made!")
        logger.info("Trying to locate the proper div(s) of news sections")

    blocks = soup.find_all('div', {'class': 'random-list-sec'})

    news = {}

    for block in blocks:
        news_block = {}
        heading = block.find('div', {'class': 'new-h2-head'}).find('a')
        news_block['heading'] = heading.text.title()

        paras = block.find_all('div', {'class': 'para-txt'})

        news_list = []

        for para in paras:
            para = para.find('a')
            block_news = {'text': para.text.strip(), 'link': para['href']}
            news_list.append(block_news)

        news_block['news_list'] = news_list

        news[news_block['heading']] = news_block

    return news
