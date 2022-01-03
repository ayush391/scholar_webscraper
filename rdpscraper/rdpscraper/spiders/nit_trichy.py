import scrapy


class NitTrichySpider(scrapy.Spider):
    name = 'nit_trichy'
    allowed_domains = ['https://www.nitt.edu/home/academics/departments/']
    start_urls = ['www.nitt.edu/home/academics/departments//']

    def parse(self, response):
        #Extracting the content using css selectors
        departmentLinks = response.css('.facitem h1 a::attr(href').extract()
        yield departmentLinks
        