# -*- coding: utf-8 -*-
import scrapy
from setu.items import BookChapters
import bs4
from bs4 import BeautifulSoup
from scrapy.http import Request


class BookChaptersSpider(scrapy.Spider):
    name = 'book_chapters'
    allowed_domains = ['x23qb.com']
    start_urls = ['http://x23qb.com/lightnovel/1/']

    def __init__(self):
        self.base_url = 'https://www.x23qb.com/lightnovel/'

    def parse(self, response):
        # 获取页面

        current_page = BeautifulSoup(response.text, 'lxml')
        current_page_num = current_page.find(
            'div', class_='pagelink').span.string.split('/')[0]

        # * 为测试不放开页面限制
        for item in range(1, 2):
            next_page = self.base_url + str(item) + '/'
            yield Request(next_page, callback=self.parse_page)

    def parse_page(self, response):

        # 获取书籍

        p_current_page = BeautifulSoup(response.text, 'lxml')
        books_box = p_current_page.find('div', id="sitebox").find_all('dl')
        for book in books_box:
            if type(book) is not bs4.element.NavigableString:
                book_category = book.find('span').string

                # 排除半吊子作者写的网文
                if book_category != '轻小说の' and book_category != '轻の小说':
                    current_book = book.dt.a['href']
                    yield Request(current_book, callback=self.parse_book)

    def parse_book(self, response):

        # 解析章节标题
        boks = BeautifulSoup(response.text, 'lxml')
        the_list = boks.find('ul', id='chapterList').find_all('a')
        boks_list = []
        book_chapter = BookChapters()
        for bok in the_list:
            info = {}
            info['chapter_name'] = bok.string
            info['chapter_id'] = bok['href'].split('/')[-1].split('.')[-2]
            boks_list.append(info)

        book_chapter['book_id'] = the_list[0]['href'].split('/')[-1][:-5]
        book_chapter['chapter_info'] = boks_list

        yield book_chapter
