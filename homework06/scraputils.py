import requests
from bs4 import BeautifulSoup
import time


def extract_news(soup)->list:
    """ Extract news from a given web page """

    news_list = []
    rows = soup.findAll('tr', attrs={'class': 'athing'})

    for i in range(len(rows)):
        title_row = soup.findAll('tr', attrs={'class': 'athing'})
        number = title_row[i].find('td').text
        title = title_row[i].find('a', attrs={'class': 'storylink'}).text
        url = title_row[i].find('a', attrs={'class': 'storylink'})['href']

        subtext_row = soup.findAll('td', attrs={'class': 'subtext'})
        author = subtext_row[i].find('a', attrs={'class': 'hnuser'})
        if author:
            author = author.text
        else:
            author = None
        points = subtext_row[i].find('span').text
        points = int(points.split()[0])
        comments = subtext_row[i].findAll('a')[5].text
        if comments == 'discuss':
            comments = 0
        else:
            comments = int(comments.split()[0])

        news = {
        'author': author,
        'comment': comments,
        'point': points,
        'title': title,
        'url': url
        }
        news_list.append(news)

    return news_list


def extract_next_page(soup)->str:
    """ Extract next page URL """
    next_page = soup.find('a', attrs={'class': 'morelink'})
    return next_page['href']


def get_news(url='https://news.ycombinator.com/', n_pages=1)->list:
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        if n_pages>1:
            print('sleep for 30 seconds...')
            time.sleep(30)
        n_pages -= 1    
    return news
