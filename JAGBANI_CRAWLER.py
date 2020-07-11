#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import xlsxwriter
import socket
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import quote
from urllib.request import urlopen, Request, URLError

'''
initialize file name for news data management

FactSheet = 'C:\\Users\\PycharmProjects\\web_scrapper\\data_files\\statistics.xlsx'
workbook = xlsxwriter.Workbook(FactSheet)
worksheet1 = workbook.add_worksheet()
worksheet1.write(0, 0, "Text_File_No")
worksheet1.write(0, 1, "Title")
worksheet1.write(0, 2, "Genre")
worksheet1.write(0, 3, "Time")
worksheet1.write(0, 4, "Unique Words")
'''

'''initialze jagbani newspaper URL'''
#html = urllib.request.urlopen("https://jagbani.punjabkesari.in/", timeout=30)
jagbani_pages= []
req = Request('https://jagbani.punjabkesari.in/', headers={'User-Agent': 'Mozilla/5.0'})
try:
    req.selector.encode('ascii')
except UnicodeEncodeError:
    req.selector = quote(req.selector)
try:
    response = urllib.request.urlopen(req, timeout=30)
    html = response.read().decode('utf-8')
except socket.timeout:
    pass
except URLError:
    pass

workbook = ''
def make_directory(FolderName):
    path = r'F:\jagbani Corpus\\' + FolderName
    if not os.path.exists(path):
        os.makedirs(path)
def create_excel_sheet(FolderName):
    FactSheet = r'F:\jagbani Corpus\\' + FolderName + '\\' + FolderName + '_STATS.xlsx'
    global workbook
    workbook = xlsxwriter.Workbook(FactSheet)
    global worksheet1
    worksheet1 = workbook.add_worksheet()
    worksheet1.write(0, 0, "Text_File_No")
    worksheet1.write(0, 1, "Title")
    worksheet1.write(0, 2, "Genre")
    worksheet1.write(0, 3, "Month")
    worksheet1.write(0, 4, "Date")
    worksheet1.write(0, 5, "Year")

def initialize():
    if html is None:
        print("URL is not found")
    else:
        '''
        This parts extracts all the link for in jagbani website pages    
        '''
        bsObj = BeautifulSoup(html, "html.parser")
        front_url = "http://jagbani.punjabkesari.in"
        div = bsObj.findAll('div', attrs={'class': 'kjpage'})
        for page_no in div:
            links = page_no.find_all('a')
            for link in links:
                jagbani_pages.append(front_url+link['href'])

file_no = 0
row = 1
col = 0
def text_extraction(url):
    '''
    :param url: The page url from which we want to extract the text
    :return:
    '''
    global file_no
    global row
    global col
    # Set Row and Column sequence
    allurls = []
    html = urlopen(url)
    parser = BeautifulSoup(html, "html.parser")
    spans = parser.findAll('span', attrs={'class': lambda class_: class_ in ("story", "midle")})
    for span in spans:
        #print(span.get_text())
        links = span.find_all('a')
        for link in links[:1]:
            allurls.append(link['href'])
        for url in allurls:
            filename = "text_" + str(file_no) + ".txt"
            print(url)
            print(filename)
            print(col)
            print(row)
            worksheet1.write(row, col, filename)
            col += 1
            worksheet1.write(row, col, span.get_text())
            col += 1
            regex = re.compile(r'.*//.*\.in/([^\/]*)/.*')
            news_genre = regex.sub(lambda m: m.group(1), url)
            worksheet1.write(row, col, news_genre)
            col += 1
            req = urllib.request.Request(url)
            try:
                req.selector.encode('ascii')
            except UnicodeEncodeError:
                req.selector = quote(req.selector)
            response = urllib.request.urlopen(req, timeout=30)
            news_url = response.read().decode('utf-8')
            particular_news_parser = BeautifulSoup(news_url, "html.parser")
            for time in particular_news_parser.findAll('div', attrs={'class': 'time2'}):
                worksheet1.write(row, col, time.text)
                col += 1
            div = particular_news_parser.findAll('div', attrs={'class': 'desc'})
            '''
            Location of the filename, where you want to save your data_files
            '''
            file = "D:\\data_files\\" + filename
            with open(file, 'w', encoding='utf8') as f:
                for x in div:
                    f.write(x.find('p').text)
            file_no += 1
            col = 0
            row += 1
            allurls = []

def get_page_links(url, genre_name, start_num, end_num):
    website_url = "https://punjabi.jagran.com/"
    jagran_page_link = website_url + genre_name +"-news-punjabi-page"
    for i in range(start_num, end_num):
        link = jagran_page_link + str(i) + ".html"
        get_page_title_and_link(link, genre_name)
        print(link)



def main():
    make_directory("sports")
    create_excel_sheet("sports")
    #initialize()
    get_page_links(link, genre, start, end)
    for url in jagbani_pages:
        print("URL: ", url)
        text_extraction(url)
    workbook.close()

if __name__ == '__main__':
    main()
