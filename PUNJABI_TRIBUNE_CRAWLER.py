#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import socket
import xlsxwriter
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import quote
from urllib.request import urlopen
from urllib.request import Request, URLError

'''Initialize Punjabi Tribune newspaper URL'''
req = Request('http://punjabitribuneonline.com/', headers={'User-Agent': 'Mozilla/5.0'})
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
punjabi_tribune_genre_dictionary = {}
workbook = ''
row = 1
col = 0

def make_directory(FolderName):
    path = r'F:\Punjabi Tribune Corpus\\' + FolderName
    if not os.path.exists(path):
        os.makedirs(path)

def create_excel_sheet(FolderName):
    FactSheet = r'F:\Punjabi Tribune Corpus\\' + FolderName + '\\' + FolderName + '_STATS.xlsx'
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

def news_genre_links():
    '''
    This function generate the Punjabi Tribune URL links and Genres
    and append it in the punjabi_tribune_genre_dictionary
    :return: NONE
    '''
    if html is None:
        print("URL is not found")
    else:
        '''
        This parts extracts all the link for in Punjabi Tribune website pages    
        '''
        bsObj = BeautifulSoup(html, "html.parser")
        div = bsObj.findAll('div', attrs={'class': 'dnk_nav'})
        for genres in div:
            links = genres.find_all('a')
            for link in links:
                punjabi_tribune_genre_dictionary[link.text] = link['href']

def get_url_page_paragraph_text(url, filenumber, FolderName, title):
    '''
    Function generates the paragaph text from the News URL provided
    as the parameter
    :param url: URL of the page
    :return:
    '''
    genre_page = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        genre_page.selector.encode('ascii')
    except UnicodeEncodeError:
        genre_page.selector = quote(genre_page.selector)
    try:
        page_response = urllib.request.urlopen(genre_page, timeout=30)
        page = page_response.read().decode('utf-8')
        parser = BeautifulSoup(page, "html.parser")
        div = parser.find('div', attrs={'class': 'font_styl'}).findAll('p')
        span = parser.find('span', attrs={'class': 'clock'})
        date_text = span.text
        regex = re.compile(r'.* .* ([^\/]*) - ([^\/]*) - ([^\/]*)')
        month = regex.sub(lambda m: m.group(1), date_text)
        date = regex.sub(lambda m: m.group(2), date_text)
        year = regex.sub(lambda m: m.group(3), date_text)
        article_text = ''
        for element in div:
            article_text += '\n' + ''.join(element.findAll(text=True))
        filename = "text_" + str(filenumber) + ".txt"
        path = r'F:\Punjabi Tribune Corpus\\' + FolderName + '\\' + filename
        global row, col
        global worksheet1
        worksheet1.write(row, col, filename)
        col += 1
        worksheet1.write(row, col, title)
        col += 1
        worksheet1.write(row, col, FolderName)
        col += 1
        worksheet1.write(row, col, month)
        col += 1
        worksheet1.write(row, col, int(date))
        col += 1
        worksheet1.write(row, col, int(year))
        col += 1
        print(title)
        with open(path, 'w', encoding='utf8') as f:
            f.write(article_text)
        row += 1
        col = 0
    except socket.timeout:
        pass
    except URLError:
        pass
    except socket.error:
        pass


file_number = 0
def get_page_title_and_link(url, FolderName):
    '''
    This function extracts the page title and URL to the news
    item and send the URL to the get_url_page_paragraph_text function
    to extract the paragraph text

    :param url: Page URL
    '''
    global file_number
    genre_page = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        genre_page.selector.encode('ascii')
    except UnicodeEncodeError:
        genre_page.selector = quote(genre_page.selector)
    try:
        page_response = urllib.request.urlopen(genre_page, timeout=30)
        page = page_response.read().decode('utf-8')
        parser = BeautifulSoup(page, "html.parser")
        div = parser.findAll('div', attrs={'class': 'taja_khabar width685'})
        for genres in div:
            links = genres.find_all('a')
            for link in links[:1]:
                title = link.text
                # print(link.text)
                page_url = link['href']
                # print(page_url)
                get_url_page_paragraph_text(page_url, file_number, FolderName, title)
                file_number += 1
    except socket.timeout:
        pass
    except URLError:
        pass
    except socket.error:
        pass

def get_page_links(url, genre_name):
    page_link = []
    #print("gurjot",url)
    genre_page = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        genre_page.selector.encode('ascii')
    except UnicodeEncodeError:
        genre_page.selector = quote(genre_page.selector)
    try:
        page_response = urllib.request.urlopen(genre_page, timeout=30)
        page1 = page_response.read().decode('utf-8')
        parser = BeautifulSoup(page1, "html.parser")
        # print(parser)
        div = parser.find('span', attrs={'class': "pages"})
        # print(div)
        page_numbering = div.text
        regex = re.compile(r'.* ([^\/]*) .* ([^\/]*)')
        start = regex.sub(lambda m: m.group(1), page_numbering)
        end = regex.sub(lambda m: m.group(2), page_numbering)
        regex = re.compile(r'([^\/]*),([^\/]*)')
        end = regex.sub(lambda m: m.group(1) + m.group(2), end)
        # print(start, end)
        div = parser.findAll('div', attrs={'class': 'wp-pagenavi'})
        for genres in div:
            links = genres.find_all('a')
            for link in links[:1]:
                all_pages = re.compile(r'([^\/]*)\/\d')
                start_link = all_pages.sub(lambda m: m.group(1), link['href'])
                page_link.append(start_link)
        # print(url)
        get_page_title_and_link(url, genre_name)
        start = int(start) + 1
        end = int(end) + 1

        for i in range(start, end):
            if len(page_link) != 0:
                url = page_link[0] + str(i)
                get_page_title_and_link(url, genre_name)
            else:
                pass
    except socket.timeout:
        pass
    except URLError:
        pass
    except socket.error:
        pass

def main():
    '''
    The main set the news_genre_links on go to extract the
    links and genres from main page of Punjabi Tribune

    It generates the dictionary of Punjabi news genres corresponding to
    its main URL
    example:
        'ਮੁੱਖ ਸਫ਼ਾ': 'http://punjabitribuneonline.com/category/%e0%a8%ae%e0%a9%81%e0%a9%b1%e0%a8%96-%e0%a8%b8%e0%a9%9e%e0%a8%be/'

    This further send the links and genres text to get_page_links
    to extract the pages links from corresponding genre links
    :return: NONE
    '''
    news_genre_links()
    path = r'F:\Punjabi Tribune Corpus\extracted_corpus.xlsx'
    workbook1 = xlsxwriter.Workbook(path)
    sheet1 = workbook1.add_worksheet()
    sheet1_row = 0
    sheet1_col = 0
    for folder in punjabi_tribune_genre_dictionary:
        make_directory(folder)
        file_name = folder + '_STATS.xlsx'
        sheet1.write(sheet1_row, sheet1_col, folder)
        sheet1_col += 1
        sheet1.write(sheet1_row, sheet1_col, file_name)
        sheet1_col += 1
        sheet1_row += 1
        sheet1_col = 0
    workbook1.close()

    global file_number
    global row, col
    for page in punjabi_tribune_genre_dictionary:
        print(page, "Data Extraction Started")
        create_excel_sheet(page)
        get_page_links(punjabi_tribune_genre_dictionary[page], page)
        file_number = 0
        workbook.close()
        row = 1
        col = 0
        print(page, "Data Extraction completed")

if __name__ == '__main__':
    main()
    '''
    create_excel_sheet('ਹਫਤਾਵਾਰੀ')
    get_page_links('http://punjabitribuneonline.com/category/%e0%a8%b9%e0%a8%ab%e0%a8%a4%e0%a8%be%e0%a8%b5%e0%a8%be%e0%a8%b0%e0%a9%80/', 'ਹਫਤਾਵਾਰੀ')
    file_number = 0
    workbook.close()
    row = 1
    col = 0
    create_excel_sheet('ਵਿਸਰਿਆ ਵਿਰਸਾ')
    get_page_links('http://punjabitribuneonline.com/category/%e0%a8%b5%e0%a8%bf%e0%a8%b8%e0%a8%b0%e0%a8%bf%e0%a8%86-%e0%a8%b5%e0%a8%bf%e0%a8%b0%e0%a8%b8%e0%a8%be/', 'ਵਿਸਰਿਆ ਵਿਰਸਾ')
    file_number = 0
    workbook.close()
    row = 1
    col = 0
    '''



