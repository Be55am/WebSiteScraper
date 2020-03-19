# -*- coding: utf-8 -*-
# to generate a spider from the cli : scrapy genspider <name> <thewebsiteurl>
#using scrapy tool to scrap data from websites using paginations and following links 
#for more info https://scrapinghub.com/learn-scrapy/
#to run this file in the terminal : # scrapy runspider example_quotes.py -o scraping-results.json <== the last param is to write the result in a file

import scrapy


class ExampleQuotesSpider(scrapy.Spider):
    name = 'example-quotes'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        self.log('I just visited : ' + response.url)

        urls = response.css('div.quote > span > a::attr(href)').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_details)

        for quote in response.css('div.quote'):
            item = {
                'author_name': quote.css('small.author::text').extract_first(),
                'text': quote.css('span.text::text').extract_first(),
                'tags': quote.css('a.tag::text').extract(),
            }

            yield item
        #Move to the next page
        next_page_url = response.css('li.next > a::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            #recursive call
            yield scrapy.Request(url=next_page_url, callback=self.parse)

# an other method that returns a new object from the details page.
    def parse_details(self, response):
        yield {
            'name':  response.css('.author-title::text').extract_first(),
            'birth':  response.css('.author-born-date::text').extract_first(),
            'location':  response.css('.author-born-location::text').extract_first()

        }