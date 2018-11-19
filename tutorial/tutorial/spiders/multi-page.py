import scrapy

class MultipageSpider (scrapy.Spider):
    name = "multipage"
    start_urls = ["https://www.ikea.com/us/en/catalog/allproducts/department/"]
    pageLimit = 0
    pageCount = 0

    def parse(self, response):
        for container in response.css("div.productCategoryContainer"):
            if self.pageCount >= self.pageLimit and self.pageLimit != 0:
                break
            main_category = container.css("h2.header::text").re(r'[A-Z].*')[0][:-1]
            for product in container.css("a"):
                if self.pageCount >= self.pageLimit and self.pageLimit != 0:
                    break
                sub_category = product.css("a::text").re(r'[A-Z].*')[0][:-1]
                href = response.urljoin(product.css("a::attr(href)").extract_first())
                request = scrapy.Request(href, callback = self.parseImage)
                request.meta['main_category'] = main_category
                request.meta['sub_category'] = sub_category
                self.pageCount += 1
                yield request

    def parseImage(self, response):
        main_category = response.meta['main_category']
        sub_category = response.meta['sub_category']
        for product in response.css("a.productLink img"):
            yield{
                "product_name":product.css("img::attr(alt)").extract_first(),
                "main_category": main_category,
                "sub_category": sub_category,
                "image_name": product.css("img::attr(src)").re(r'\d+.*.JPG')[0],
                "img_url": response.urljoin(product.css("img::attr(src)").extract_first())
            }
