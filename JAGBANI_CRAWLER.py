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


def make_directory(FolderName):
    path = r'F:\jagbani Corpus\\' + str(FolderName)
    if not os.path.exists(path):
        os.makedirs(path)
def create_excel_sheet(FolderName):
    FactSheet = r'F:\jagbani Corpus\\' + str(FolderName) + '\\' + str(FolderName) + '_STATS.xlsx'
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


workbook = ''
file_number = 0
row = 1
col = 0
def text_extraction(url, genre, filenumber):
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
    # TITLE DATA
    title = parser.find('div', attrs={'id': 'ContentPlaceHolder1_dv_headline'}).h1.get_text()
    date_text = parser.find('div', attrs={'class': 'dt_time'}).span.get_text()
    #print(title, date_text)
    pattern = r"([0-9]+) ([a-zA-Z]+), ([0-9]+)"
    date = re.search(pattern, date_text).group(1)
    month = re.search(pattern, date_text).group(2)
    year = re.search(pattern, date_text).group(3)
    #print("Date: ", date, " Month: ", month, " Year: ", year)
    tags = ['center', 'strong', 'a','ul','div']
    para = parser.find('div', attrs={'id': 'ContentPlaceHolder1_dv_main_news_detail'})
    for t in tags:
        [s.extract() for s in para(t)]
    para_text = ''
    for el in para.find_all():
        para_text += ''.join(el.text)
    result = re.sub(r"ਇਹ ਵੀ ਪੜ੍ਹੋ:", "", para_text, 0, re.MULTILINE)
    #print(result)
    filename = "text_" + str(filenumber) + ".txt"
    path = r'F:\jagbani Corpus\\' + genre + '\\' + filename
    global row, col
    global worksheet1
    worksheet1.write(row, col, filename)
    col += 1
    worksheet1.write(row, col, title)
    col += 1
    worksheet1.write(row, col, genre)
    col += 1
    worksheet1.write(row, col, month)
    col += 1
    worksheet1.write(row, col, int(date))
    col += 1
    worksheet1.write(row, col, int(year))
    col += 1
    print(title)
    with open(path, 'w', encoding='utf8') as f:
        f.write(result)
    row += 1
    col = 0



def get_page_links(url, genre_name):
    global file_number
    jagran_page_link = url + genre_name
    genre_page = Request(jagran_page_link, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        genre_page.selector.encode('ascii')
    except UnicodeEncodeError:
        genre_page.selector = quote(genre_page.selector)
    try:
        page_response = urllib.request.urlopen(genre_page, timeout=30)
        page = page_response.read().decode('utf-8')
        parser = BeautifulSoup(page, "html.parser")
        for ul in parser.findAll('ul', attrs={'id': 'ContentPlaceHolder1_dv_section_middle'}):
            for li in ul.find_all('h3'):
                a = li.find('a')
                #print(a['href'])
                text_extraction(a['href'], genre_name, file_number)
                file_number += 1
    except socket.timeout:
        pass
    except URLError:
        pass
    except socket.error:
        pass

def main():
    link = "https://jagbani.punjabkesari.in/"
    genre = "punjab"
    make_directory(genre)
    create_excel_sheet(genre)
    get_page_links(link, genre)
    workbook.close()

if __name__ == '__main__':
    main()
