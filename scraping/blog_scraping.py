# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from bs4 import BeautifulSoup
import sys, io
import requests

RANKING_URL = "https://official.ameba.jp/rankings/total"

driver = webdriver.Chrome()
driver.get(RANKING_URL)
html_ranking_page = driver.page_source
soup_ranking_page = BeautifulSoup(html_ranking_page, 'html.parser')
link = soup_ranking_page.find_all('a', class_="ranking-list-entry-title-link")
for i in range(len(link)):
    URL = link[i].attrs['href']
    driver.get(URL)
    resp = requests.get(URL)
    for i in range(100):
        #html_blog_page = driver.find_element_by_id("entryBody")
        #text = html_blog_page.text
        soup_blog_page = BeautifulSoup(resp.text)
        blog_content = soup_blog_page.find('div',class_="skin-entryBody")
        #print(blog_content)

        if(blog_content):
            blog_str = blog_content.strings
            f = open('data.txt','a')
            for s in blog_str:
                if s == '\xa0':
                    break;
                elif s.find('\xa0'):
                    s = s.replace(u'\xa9', u' ')
                f.write(s+"\n")
            f.close()
        if soup_blog_page.find('a', class_="skin-pagingNext"):
            blog_link = soup_blog_page.find('a', class_="skin-pagingNext")
            blog_link = blog_link.attrs['href']
            print(blog_link)
        elif soup_blog_page.find('a', class_="pagingNext"):
            blog_link = soup_blog_page.find('a', class_="pagingNext")
            blog_link = blog_link.attrs['href']
            print(blog_link)
        else:
            break;

        if blog_link.find('https://') > -1:
            BLOG_URL = blog_link
            print(BLOG_URL)
        elif blog_link.find('//ameblo.jp') > -1:
            BLOG_URL = "https:" + blog_link
        else:
            BLOG_URL = "https://ameblo.jp" + blog_link
            print(BLOG_URL)

        resp = requests.get(BLOG_URL)