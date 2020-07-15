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
import requests
import json
from requests.exceptions import HTTPError
from json.decoder import JSONDecoder


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
    # print("Date: ", date, " Month: ", month, " Year: ", year)
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

def api_content_extraction(web_url, cat_id, page_no):
    try:
        url = 'https://jagbani.punjabkesari.in/section.aspx/loadmore_section_news'
        data = { 'cat_id': str(cat_id), 'pageno':page_no, 'page_size':18, 'type':''}
        headers = {'content-type': 'application/json', 'accept': 'application/json', 'referer':web_url}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        return JSONDecoder().decode(r.text)['d']
    except HTTPError:
        return None
    except Exception:
        return None

def get_page_links(url, genre_name, cat, end):
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
        #print("getting into this ")
        for i in range(2, end+1):
            content = api_content_extraction('https://jagbani.punjabkesari.in/punjab', cat, i)
            if content != None:
                soup = BeautifulSoup(content, features="html.parser")
                for ul in soup.findAll('div', attrs={'class': 'techlist'}):
                    for li in ul.find_all('h3'):
                        a = li.find('a')
                        #print(a['href'])
                        text_extraction(a['href'], genre_name, file_number)
                        file_number += 1
            else:
                print("Ended")
    except socket.timeout:
        pass
    except URLError:
        pass
    except socket.error:
        pass

def main():
    link = "https://jagbani.punjabkesari.in/"
    print('How many Pages You want to Extract: ')
    ending = input()
    end = int(ending)
    while(True):
        print("Select Genre Number You want to extract (Each Page extract 18 news Articles): ")
        print("1. Punjab\n2. National\n3. International\n4. Sports"
              "\n5. Business\n6. Doaba\n7. Majha\n8. Malwa\n9. Gadgets\n0. Exit Window ")
        user_input = input()
        user_input = int(user_input)
        if (user_input == 1):
            genre = "punjab"
            cat = 1
            make_directory(genre)
            create_excel_sheet(genre)
            get_page_links(link, genre, cat, end)
            workbook.close()
            exit()
        elif (user_input == 2):
            genre = "national"
            cat = 2
            make_directory(genre)
            create_excel_sheet(genre)
            get_page_links(link, genre, cat, end)
            workbook.close()
            exit()
        elif (user_input == 3):
            genre = "international"
            cat = 3
            make_directory(genre)
            create_excel_sheet(genre)
            get_page_links(link, genre, cat, end)
            workbook.close()
            exit()
        elif (user_input == 4):
            genre = "sports"
            cat =4
            make_directory(genre)
            create_excel_sheet(genre)
            get_page_links(link, genre, cat, end)
            workbook.close()
            exit()
        elif (user_input == 5):
            genre = "business"
            cat = 5
            make_directory(genre)
            create_excel_sheet(genre)
            get_page_links(link, genre, cat, end)
            workbook.close()
            exit()
        elif (user_input == 6):
            genre = "doaba"
            cat = 7
            make_directory(genre)
            create_excel_sheet(genre)
            get_page_links(link, genre, cat, end)
            workbook.close()
            exit()
        elif (user_input == 7):
            genre = "majha"
            cat = 9
            make_directory(genre)
            create_excel_sheet(genre)
            get_page_links(link, genre, cat, end)
            workbook.close()
            exit()
        elif (user_input == 8):
            genre = "malwa"
            cat = 10
            make_directory(genre)
            create_excel_sheet(genre)
            get_page_links(link, genre, cat, end)
            workbook.close()
            exit()
        elif (user_input == 9):
            genre = "gadgets"
            cat = 47
            make_directory(genre)
            create_excel_sheet(genre)
            get_page_links(link, genre, cat, end)
            workbook.close()
            exit()
        elif (user_input == 0):
            exit()
        else:
            print("Enter right Value")



if __name__ == '__main__':
    main()
