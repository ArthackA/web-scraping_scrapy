# -*- coding: utf-8 -*-
import scrapy


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['craigslist.org']
    start_urls = ['https://newyork.craigslist.org/search/egr/']

    def parse(self, response):
        # Here is to extract all wrappers
        jobs = response.xpath('//p[@class = "result-info"]')
        # We dont use extract() because this is the wrapper from which we extract other HTML nodes
        # Extracting job titles
        for job in jobs:
            title = job.xpath('a/text()').extract_first()
            address = job.xpath('span[@class = "result-meta"]/span[@class = "result-hood"]/text()')
            relative_url = job.xpath('a/@href').extract_first()
            absolute_url = response.urljoin(relative_url)

            yield {'Title': title, 'Address': address, 'Link': absolute_url}

        # titles = response.xpath('//a[@class="result-title hdrlnk"]/text()').extract()
        # print(titles)
        # for title in titles:
        #     yield {"Title": title}
