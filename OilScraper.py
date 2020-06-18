import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json

# GENERAL SETTINGS
KEYWORDS = ['oil', 'crude', 'brent', 'wti', 'opec']
MAX_COUNT = 5

# Global list to store all collected articles
articles = []

# Load config variables
EMAIL = ""
PASSWORD = ""
RECIPIENTS = []

with open('config.json', 'r') as f:
    config = json.load(f)
    EMAIL = config['email']
    PASSWORD = config['password']
    RECIPIENTS = config['recipients']


def getSoup(url):
    # GET HTML FROM WEBSITE
    markup = requests.get(url).text
    soup = BeautifulSoup(markup, 'lxml')
    return soup


def getZeroHedge():
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
                i += 1
                print(headline)
                link = block.find('a')
                article = {}
                article['headline'] = headline
                article['link'] = url + link['href']
                article['source'] = '(Zero Hedge)'
                articles.append(article)
        if i >= MAX_COUNT:
            break

    print(f"{i} articles found")
    print('*' * 20)


def getOilPrice():
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
                    article = {}
                    article['headline'] = headline
                    article['link'] = block['href']
                    article['source'] = '(Oil Price)'
                    articles.append(article)
                    i += 1
            if i >= MAX_COUNT:
                break
        return i

    i = getHeadlines('newsHero__article', 'h2')
    j = getHeadlines('breakingNewsBlock__article', 'h3')

    print(f"{j + i} articles found")
    print('*' * 20)


def getWorldOilNews():
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
                article = {}
                print(headline.text)
                article['headline'] = headline.text
                article['link'] = 'https://www.worldoil.com/' + \
                    headline['href']
                article['source'] = '(World Oil News)'
                articles.append(article)
                i += 1
        if i >= MAX_COUNT:
            break

    print(f"{i} articles found")
    print('*' * 20)


def getConversation():
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
                article = {}
                print(headline.text)
                article['headline'] = headline.text
                article['link'] = 'https://theconversation.com' + \
                    headline['href']
                article['source'] = '(The Conversation)'
                articles.append(article)
                i += 1
        if i >= MAX_COUNT:
            break

    print(f"{i} articles found")
    print('*' * 20)


def generateHTML():
    # Function to transform list of articles into list items within html document
    content = []
    for article in articles:
        bullet = '<li><a href="'
        bullet += article['link'] + '" target="_blank">' + \
            article['headline'] + '</a>' + '<p>'+article['source']+'</p></li>'
        content.append(bullet)

    starting_html = '''
    <html>
        <head>
            <style>
                body {
                    font-family: sans-serif;

                }
                ul {
                    list-style: none;
                    width: 100%;
                }
                li {
                    width: 100%;
                }
                p {
                    display: inline;
                    margin-left: 20px;
                }
                li {
                    padding-top: 5px;
                }
            </style>
        </head>
        <body>
            <h1>News Headlines</h1>
            <ul>
                $LIST
            </ul>
        </body>
    </html>
    '''
    html = starting_html.replace('$LIST', ('').join(content))
    return html


def testHTML(html):
    # Save to sample html for testing
    with open('sample.html', 'w') as f:
        print(html, file=f)
        print('HTML generated')


def sendMail(html):
    # EMAIL

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL, PASSWORD)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Oil News Headlines"
        msg['From'] = EMAIL
        msg['To'] = ", ".join(RECIPIENTS)
        plain = "Here are some headlines"
        part1 = MIMEText(plain, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        smtp.send_message(msg)
        print('Mail sent')


if __name__ == '__main__':
    getZeroHedge()
    getOilPrice()
    getWorldOilNews()
    getConversation()
    print(f"Total articles found: {len(articles)}")

    html = generateHTML()

    # Uncomment below for debug of email template
    # testHTML(html)
    sendMail(html)
