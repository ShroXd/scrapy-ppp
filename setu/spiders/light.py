# -*- coding: utf-8 -*-
import scrapy
from setu.items import LightItem
from bs4 import BeautifulSoup


class LightSpider(scrapy.Spider):
    name = 'light'
    allowed_domains = ['x23qb.com']
    start_urls = ['http://www.x23qb.com/lightnovel/']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        spins = soup.find_all('span', class_="uptime")
        item = LightItem()
        for spin in spins:
            category = spin.parent.parent.next_sibling.next_sibling.span.contents[0]
            if category != '轻小说の' and category != '轻の小说':
                item['title'] = spin.next_sibling.contents[0]
                item['uptime'] = spin.contents[0]
                item['des'] = spin.parent.parent.next_sibling.next_sibling.next_sibling.next_sibling.contents[0]
                item['category'] = category
                item['status'] = spin.parent.parent.next_sibling.next_sibling.span.next_sibling.next_sibling.contents[0]
                item['wordCount'] = spin.parent.parent.next_sibling.next_sibling.find_all('span')[
                    2].contents[0]
                yield item
