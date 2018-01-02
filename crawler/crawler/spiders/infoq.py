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
        links = articles.xpath("./a[@class='lt']/@href").extract()
        #authors = articles.xpath("./a[@class='editorlink f_taxonomyEditor']/text()").extract()
        authors = articles.xpath(".//span[@class='authors-list']")
        dates_y = articles.xpath("./ul[@class='ldate']/li[@class='ldate_y']/text()")
        dates_m = articles.xpath("./ul[@class='ldate']/li[@class='ldate_d']/text()")
        dates_d = articles.xpath("./ul[@class='ldate']/li[@class='ldate_m']/text()")

        #remove ads
        i = 0

        #month
        mmdict = {
            u'一月': '01',
            u'二月': '02',
            u'三月': '03',
            u'四月': '04',
            u'五月': '05',
            u'六月': '06',
            u'七月': '07',
            u'八月': '08',
            u'九月': '09',
            u'十月': '10',
            u'十一月': '11',
            u'十二月': '12',
                 }
        for idx, title in enumerate(titles):
            if title.strip() == "":
                i = i+1
                continue
            thedate = dates_y[idx-i].extract() + "/" + mmdict[dates_m[idx-i].extract()] + "/" + dates_d[idx-i].extract()

            yield {
                "title": title.strip(),
                "link": links[idx-i].strip(),
                "author": authors[idx-i].xpath(".//a[@class='editorlink f_taxonomyEditor']/text()").extract(),
                "date" : thedate,
            }

        next_page = response.css("a.btn_next::attr('href')").extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
        pass
