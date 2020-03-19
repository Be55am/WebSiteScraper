# -*- coding: utf-8 -*-

#for more info https://docs.scrapy.org/en/latest/topics/request-response.html
import scrapy


class SpiderForFormsSpider(scrapy.Spider):
    name = 'spider-for-forms'
    start_urls = ['http://quotes.toscrape.com/login']

    def parse(self, response):
        #extract the csrf token
        token = response.css('input[name="csrf_token"]::attr(value)').extract_first()
        #create a python dictonary with the form values
        data = {
            'csrf_token': token,
            'username': 'abc',
            'password': 'abc'
        }
        #submit a post request
        yield scrapy.FormRequest(url=self.start_urls[0],formdata=data,callback=self.parse_quotes)

    def parse_quotes(self, response):
        #parse the main page after the spider is logged in
        for q in response.css('div.quote'):
            yield{
                'author_name': q.css('small.author::text').extract_first(),
                'author_url':q.css('small.author ~ a[href*="goodreads.com"]::attr(href)').extract_first()
            }
