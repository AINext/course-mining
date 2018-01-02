# -*- coding: utf-8 -*-
import scrapy

class InfoqSpider(scrapy.Spider):
    name = 'infoq'
    allowed_domains = ['infoq.com']
    start_urls = [
                    'http://infoq.com/cn/AI/articles'
                 ]

    def parse(self, response):
        articles = response.xpath("//ul[@class='l l_large']/li")

        titles = articles.xpath("./a[@class='lt']/text()").extract()

        for idx, title in enumerate(titles):
            if title.strip() == "":
                continue
            yield {
                "title": title.strip(),
            }

        next_page = response.css("a.btn_next::attr('href')").extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
        pass
