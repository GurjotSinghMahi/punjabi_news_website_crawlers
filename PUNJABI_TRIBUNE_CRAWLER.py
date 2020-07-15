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
import requests

workbook = ''
row = 1
col = 0
file_number = 0

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

def get_url_page_paragraph_text(url, filenumber, FolderName):
    '''
    Function generates the paragaph text from the News URL provided
    as the parameter
    :param url: URL of the page
    :return:
    '''
    #print(url)
    html = urlopen(url)
    parser = BeautifulSoup(html, features="html.parser")
    title = parser.find('div', attrs={'class': 'glb-heading'}).h1.get_text()
    #print(title)
    date_text = parser.find('div', attrs={'class': 'time-share'}).span.get_text()
    #print(date_text)
    pattern = r"([a-zA-z]+) ([0-9]+), ([0-9]+)"
    month = re.search(pattern, date_text).group(1)
    date = re.search(pattern, date_text).group(2)
    year = re.search(pattern, date_text).group(3)
    #print("Date: ", date, " Month: ", month, " Year: ", year)
    para = parser.find('div', attrs={'class': 'story-desc'})
    para_text = ''
    tags = ['strong', 'b']
    for t in tags:
        [s.extract() for s in para(t)]
    for el in para.find_all():
        para_text += ''.join(el.text)
    #print(para_text)
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
        f.write(para_text)
    row += 1
    col = 0

def extract_links(url_1, id, genre):
    global file_number
    topNews = '9193,9013,9015,9049,9042'
    under_score = 1594805443439
    url = 'https://www.punjabitribuneonline.com/Pagination/ViewAll?id=' + str(id) + "&page=" + str(page) # + "&topNews=" + topNews + "&_=" + str(under_score)
    headers = {'content-type': 'text/html', 'accept': '*/*'}
    r = requests.get(url, headers=headers)
    parser = BeautifulSoup(r.text, features="html.parser")
    soup = parser.findAll('a', attrs={'class': "card-top-align"}, href=True)
    for result in soup:
        page_url = url_1+result['href']
        #print(page_url)
        get_url_page_paragraph_text(page_url, file_number, genre)
        file_number += 1

def get_last_page_number(genre):
    url = 'https://www.punjabitribuneonline.com/news/' + genre
    html = urlopen(url)
    parser = BeautifulSoup(html, features="html.parser")
    regex = r"totalPages: ([0-9]+),"
    #print(parser)
    last_page = re.search(regex, str(parser)).group(1)
    return last_page

if __name__ == '__main__':
    while (True):
        print("Select Genre Number You want to extract (Each Page extract 18 news Articles): ")
        print("1. National\n2. World\n3. Sports\n4. Business"
              "\n5. Agriculture\n6. Features\n0. Exit Window ")
        user_input = input()
        user_input = int(user_input)
        if (user_input == 1):
            print("Data Extraction Started")
            genre = "nation"
            make_directory(genre)
            create_excel_sheet(genre)
            url = 'https://www.punjabitribuneonline.com'
            id = 42
            page = get_last_page_number(genre)
            for i in range(1, int(page) + 1):
                extract_links(url, id, genre)
            workbook.close()
            print("Data Extraction completed")
            exit()
        elif (user_input == 2):
            print("Data Extraction Started")
            genre = "world"
            make_directory(genre)
            create_excel_sheet(genre)
            url = 'https://www.punjabitribuneonline.com'
            id = 57
            page = get_last_page_number(genre)
            for i in range(1, int(page) + 1):
                extract_links(url, id, genre)
            workbook.close()
            print("Data Extraction completed")
            exit()
        elif (user_input == 3):
            print("Data Extraction Started")
            genre = "sports"
            make_directory(genre)
            create_excel_sheet(genre)
            url = 'https://www.punjabitribuneonline.com'
            id = 50
            page = get_last_page_number(genre)
            for i in range(1, int(page) + 1):
                extract_links(url, id, genre)
            workbook.close()
            print("Data Extraction completed")
            exit()
        elif (user_input == 4):
            print("Data Extraction Started")
            genre = "business"
            make_directory(genre)
            create_excel_sheet(genre)
            url = 'https://www.punjabitribuneonline.com'
            id = 0
            page = get_last_page_number(genre)
            for i in range(1, int(page) + 1):
                extract_links(url, id, genre)
            workbook.close()
            print("Data Extraction completed")
            exit()
        elif (user_input == 5):
            print("Data Extraction Started")
            genre = "agriculture"
            make_directory(genre)
            create_excel_sheet(genre)
            url = 'https://www.punjabitribuneonline.com'
            id = 279
            page = get_last_page_number(genre)
            for i in range(1, int(page) + 1):
                extract_links(url, id, genre)
            workbook.close()
            print("Data Extraction completed")
            exit()
        elif (user_input == 6):
            print("Data Extraction Started")
            genre = "features"
            make_directory(genre)
            create_excel_sheet(genre)
            url = 'https://www.punjabitribuneonline.com'
            id = 26
            page = get_last_page_number(genre)
            for i in range(1, int(page) + 1):
                extract_links(url, id, genre)
            workbook.close()
            print("Data Extraction completed")
            exit()
        elif (user_input == 0):
            exit()
        else:
            print("Enter right Value")

