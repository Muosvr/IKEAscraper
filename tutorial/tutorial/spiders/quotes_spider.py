import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://www.ikea.com/us/en/catalog/categories/departments/workspaces/16213/',
    ]

    def parse(self, response):
        for product in response.css("a.productLink img"):
            yield {
                "Product_name": product.css("img::attr(alt)").extract_first(),
                "img": response.urljoin(product.css("img::attr(src)").extract_first()),
            }

        # next_page = response.css('li.next a')
        # if next_page is not None:
        #     yield response.follow(next_page[0], callback=self.parse)
