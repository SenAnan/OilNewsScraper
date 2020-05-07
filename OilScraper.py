import requests
from bs4 import BeautifulSoup

# GENERAL SETTINGS
KEYWORDS = ['oil', 'crude', 'brent', 'wti', 'opec']
MAX_COUNT = 5

websites = ['zerohedge', 'oilprice', 'worldoil', 'theconversation']

# GET HTML FROM WEBSITE


def getSoup(url):
    markup = requests.get(url).text
    soup = BeautifulSoup(markup, 'lxml')
    return soup


# Cannot make reusable function cross site (easily) as each has different structure of html
# ZERO HEDGE
print('ZERO HEDGE')
url = 'https://www.zerohedge.com'
soup = getSoup(url)

blocks = soup.find_all('h2', class_='teaser-title')
i = 0
for block in blocks:
    headline = block.find('span').text
    for word in headline.split(' '):
        if word.lower() in KEYWORDS:
            print(headline)
            i += 1
            link = block.find('a')
            print(url+link['href'])
    if i > MAX_COUNT:
        break

print(f"{i} articles found")
print('*' * 20)

# OILPRICE
print('OILPRICE')
url = 'https://oilprice.com/'
soup = getSoup(url)

block = soup.find('a', class_="newsHero__featuredArticle")
headline = block.find('h2').text
link = block['href']
print(headline)
print(link)


def getHeadlines(className, heading):
    blocks = soup.find_all('a', class_=className)
    i = 0
    for block in blocks:
        headline = block.find(heading).text
        for word in headline.split(' '):
            if word.lower() in KEYWORDS:
                print(headline)
                print(block['href'])
                i += 1
        if i > MAX_COUNT:
            break
    return i


i = getHeadlines('newsHero__article', 'h2')
j = getHeadlines('breakingNewsBlock__article', 'h3')

print(f"{j + i} articles found")
print('*' * 20)

# WORLD OIL NEWS
print("WORLD OIL NEWS")
url = 'https://www.worldoil.com/news'
soup = getSoup(url)

blocks = soup.find_all('div', class_="article")
i = 0
for block in blocks:
    headline = block.find('a')
    for word in headline.text.split(' '):
        if word.lower() in KEYWORDS:
            print(headline.text)
            print('https://www.worldoil.com/' + headline['href'])
            i += 1
    if i > MAX_COUNT:
        break

print(f"{i} articles found")
print('*' * 20)

# THE CONVERSATION
print('THE CONVERSATION')
url = "https://theconversation.com/uk/business"
soup = getSoup(url)

blocks = soup.find_all(
    'article', class_={'clearfix', 'placed', 'analysis', 'published'})
i = 0
for block in blocks:
    headline = block.find('a')
    for word in headline.text.strip().split(' '):
        if word.lower() in KEYWORDS:
            print(headline.text)
            print('https://theconversation.com' + headline['href'])
            i += 1
    if i > MAX_COUNT:
        break

print(f"{i} articles found")
print('*' * 20)
