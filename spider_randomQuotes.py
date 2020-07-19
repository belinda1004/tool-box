# !/usr/bin/python3
# -*- coding:utf-8 -*-
# author: Belinda Wang https://github.com/belinda1004

# Generate a random quote.
# Source: https://www.goodreads.com/

import random
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

MAX_PAGE = 100

def getHTMLText(url):
    try:
        kv = {'User-Agent': 'Mozilla/5.0'}  # Mozilla/5.0是一个通用浏览器代码
        request = Request(url, headers = kv)
        response = urlopen(request)
        return response.read().decode('utf-8')
    except:
        return 'Error'


url = 'https://www.goodreads.com/quotes?page=' + str(random.randint(1,MAX_PAGE))
html = getHTMLText(url)
bs = BeautifulSoup(html,'html.parser')
quotes = bs.find_all('div', attrs = {'class':'quote'})
quote = quotes[random.randint(0,len(quotes)-1)]
quote_text = quote.find('div',attrs = {'class':'quoteText'})
print(quote_text.get_text())