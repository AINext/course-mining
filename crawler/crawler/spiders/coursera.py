# -*- coding: utf-8 -*-
import scrapy

class CourseraSpider(scrapy.Spider):
    name = 'coursera'
    allowed_domains = ['coursera.org']
    start_urls = [
                  # 'http://coursera.org/browse/computer-science',
                  'https://www.coursera.org/browse/computer-science/software-development',
                 ]

    def parse(self, response):

        # title
        #element = response.css(".rc-BrowseSummary")
        #yield {
        #    'title' :  element.xpath("//h1/text()").extract_first(),
        #}

        courses = response.xpath("//div[contains(@class,main_container)]/a[@name='offering_card']")

        links = courses.xpath("./@href").extract()
        names = courses.xpath("./div[@class='offering-content']//h2/text()").extract()

        for idx, link in enumerate(links):
            yield {
                "link":link,
                "name":names[idx]
            }

        next_page = response.css("a[data='right-arrow']::attr('href')").extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
        pass
