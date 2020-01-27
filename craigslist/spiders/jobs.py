# -*- coding: utf-8 -*-
import scrapy
# from _cffi_backend import callback
from scrapy import Request


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
            address = job.xpath('span[@class = "result-meta"]/span[@class = "result-hood"]/text()').extract_first("")[
                      2:-1]
            relative_url = job.xpath('a/@href').extract_first()
            absolute_url = response.urljoin(relative_url)
            yield Request(absolute_url, callback=self.parse_page,
                          meta={'Title': title, 'Address': address, 'Link': absolute_url})

            # yield {'Title': title, 'Address': address, 'Link': absolute_url}
        relative_next_url = response.xpath('//a[@class = "button next"]/@href').extract_first()
        absolute_next_url = response.urljoin(relative_next_url)
        yield Request(absolute_next_url, callback=self.parse)

    def parse_page(self, response):
        url = response.meta.get('Link')
        title = response.meta.get('Title')
        address = response.meta.get('Address')
        description = "".join(line for line in response.xpath('//*[@id= "postingbody"]/text()').extract())
        compensation = response.xpath('//p[@class="attrgroup"]/span/b/text()')[0].extract()
        employment_type = response.xpath('//p[@class="attrgroup"]/span/b/text()')[1].extract()

        yield {'Titles ': title, 'Addresses': address,'Links ': url, 'Descriptions': description,'Compensation':compensation,'employment type':employment_type}

    # yield Request(absolute_next_url, callback=self.parse_page,
    #meta={'Title': title, 'Address': address, 'Link': absolute_url})

    # titles = response.xpath('//a[@class="result-title hdrlnk"]/text()').extract()
    # print(titles)
    # for title in titles:
    #     yield {"Title": title}
