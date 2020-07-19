#!/usr/bin/python3
# -*-coding:utf-8-*-
# author: Belinda Wang https://github.com/belinda1004

# Get forecast for main cities of Australia
# Query detailed forecast by postcode
# Source: https://www.weather.com.au/, https://auspost.com.au/

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


print('Australian  Forecast Summary')


def getUpdateTime(soup):
    update_str = soup.select('div > #breadcrumbs')[0].text
    return update_str.split('-')[-1]

def getTablebyId(soup, id):
    tables = soup.select('table')
    for table in tables:
        if 'id' in table.attrs and table.attrs['id'] == id:
            return table
    return None

def getTableHead(table):
    head = []
    head_index = []
    trs = table.select('tbody > tr')
    tds = trs[0].select('td')
    for i in range(len(tds)):
        if tds[i].attrs['class'][0] == 'icon':
            continue
        head.append(tds[i].attrs['class'][0].capitalize())
        head_index.append(i)
    return head, head_index

def getTableData(table, head_index):
    data = []
    trs = table.select('tbody > tr')
    for tr in trs:
        entry = []
        tds = tr.select('td')
        for idx in head_index:
            entry.append(tds[idx].text)
        data.append(entry)
    return data

def getForecastSummary(soup):
    summarytable = getTablebyId(soup,'summary')
    head, head_index = getTableHead(summarytable)
    cities = getTableData(summarytable, head_index)
    return (head,cities)

def printSummaryForecast(head, summary):
    template = '{:^20}{:^100}{:^10}{:^10}'
    print(template.format(head[0],head[1],head[2],head[3]))
    for city in summary:
        print(template.format(city[0], city[1], city[2], city[3]))

def getSurburbandStateByPostcode(postcode):
    url = 'https://auspost.com.au/postcode/' + postcode
    reponse = urlopen(url)
    bs = BeautifulSoup(reponse,'html.parser')
    table = bs.find('table', attrs={'class': re.compile(r'^resultsList')})
    trs = table.select('tbody > tr')
    result = []
    for tr in trs:
        result.append(tr.select('.second')[0].text)
    return result

def printSuburb(postcode,suburbs):
    print('Postcode : ' + postcode)
    if len(suburbs) == 1:
        print('Suburb : ' + suburbs[0])
    else:
        print('Suburbs : ' + suburbs[0])
        for i in range(1,len(suburbs)):
            print('          ' + suburbs[i])

def getForecastByPostCode(postcode):
    suburbs = getSurburbandStateByPostcode(postcode)
    printSuburb(postcode, suburbs)
    for i in range(len(suburbs)):
        suburb = suburbs[i].split(',')[0].strip()
        state = suburbs[i].split(',')[1].strip()
        url = 'https://www.weather.com.au/' + state + '/' + suburb
        response = urlopen(url)
        bs = BeautifulSoup(response, "html.parser")
        table = getTablebyId(bs, 'extended')
        if not table:
            continue
        head, head_index = getTableHead(table)
        forecast = getTableData(table, head_index)
        return head, forecast


def printForecast(head, forecast):
    template = '{:^20}{:^60}{:^20}{:^20}{:^10}{:^10}'
    print(template.format(head[0],head[1],head[2],head[3],head[4],head[5]))
    for day in forecast:
        print(template.format(day[0], day[1], day[2], day[3],day[4],day[5]))


if __name__ == '__main__':
    url = 'https://www.weather.com.au/'
    response = urlopen(url)
    bs = BeautifulSoup(response, "html.parser")
    # update time
    print(getUpdateTime(bs))
    head,summary = getForecastSummary(bs)
    printSummaryForecast(head,summary)
    while True:
        postcode = input('\r\nForecast by postcode(press q to quit):')
        if postcode in ['q','Q']:
            break
        try:
            head, forecast = getForecastByPostCode(postcode)
            printForecast(head, forecast)
        except:
            print('Can\'t get forecast for postcode ',postcode)