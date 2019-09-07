import requests
from bs4 import BeautifulSoup

url = "https://www.hindustantimes.com/"


def get_top_news_block(soup):
    news_list = []

    big_story_block = soup.find('div', {'class': 'big-middlenews'})

    big_story = big_story_block.find('div', {'class': 'bigstory-h2'}).find('a')
    block_news = {'text': big_story.text.strip(), 'link': big_story['href']}
    news_list.append(block_news)

    big_story = big_story_block.find('div', {'class': 'bigstory-mid-h3'}).find('a')
    block_news = {'text': big_story.text.strip(), 'link': big_story['href']}
    news_list.append(block_news)

    top_news_div = soup.find('div', {'class': 'latestnews-left'})
    top_news_heading = top_news_div.find('div', {'class': 'new-h2-head'}).text.strip().title()
    paras = soup.find('ul', {'class': 'latestnews-topblk'}).find_all('li')

    news_block = {}
    news_block['heading'] = top_news_heading
    for para in paras:
        para = para.find('a')
        block_news = {'text': para.text.strip(), 'link': para['href']}
        news_list.append(block_news)

    news_block['news_list'] = news_list
    return news_block


def return_full_news_data(logger=None):
    if logger:
        logger.info("Requesting URL")

    response = requests.get(url)

    news = {}

    if logger:
        logger.info(str(response))
        logger.info('Making Soup Object ...')

    soup = BeautifulSoup(response.content, 'html5lib')

    if logger:
        logger.info("Soup Object Made!")
        logger.info("Trying to locate the proper div(s) of news sections")

    top_news_block = get_top_news_block(soup)
    news[top_news_block['heading']] = top_news_block

    blocks = soup.find_all('div', {'class': 'random-list-sec'})

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
