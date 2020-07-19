#!/usr/bin/python3
# -*-coding:utf-8-*-
# author: Belinda Wang https://github.com/belinda1004

# Electrical dictionary
# Source: https://www.dictionary.com/

from urllib.request import urlopen
from urllib.request import Request
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import re
import random

# The format of request url

'''
https://www.dictionary.com/browse/hello
'''


def translate(url, key):
    true_url = url + key
    request = Request(true_url)
    try:
        response = urlopen(request)
        bs = BeautifulSoup(response, "html.parser")
        main = bs.find('main')
        content = main.find('div',attrs = {'class':re.compile(r'^css-1urpfgu')})
    except:
        print('No result found for ', key)
        print('\r\n\r\n')
        return

    # soundmark
    pron = content.find('div',attrs = {'class':re.compile(r'^pron-spell-container')}).text
    print(pron[:pron.index(']')+1])

    # definition
    definitions = content.find_all('section',attrs = {'class':re.compile(r'^css-pnw38j')})
    index = 1
    for d in definitions:
        # part of speech
        print('\r\n' + d.find('h3').text)

        # definition
        lines = d.find_all('span',attrs = {'class':re.compile(r'^one-click-content')})
        for line in lines:
            text = line.text
             # example sentence
            example = line.find('span',attrs = {'class':re.compile(r'^luna-example')})
            if example:
                print('  ' + str(index) + '. ' + text[:text.index(':')])
                print('     example: ' + example.text)
            else:
                print('  ' + str(index) + '. ' + text)
            index += 1
    print('\r\n\r\n')


while True:
    url = "https://www.dictionary.com/browse/"
    key = input("please input your word : ")
    translate(url, key)
