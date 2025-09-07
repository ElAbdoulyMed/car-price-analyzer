import scrapy

class AutoplusSpider(scrapy.Spider):
    name = "autoplus"
    collection_to_use = "cars"

    def start_requests(self):
        url = "https://www.auto-plus.tn/les-voitures-neuves.html"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        car_brands = response.xpath('//*[@id="searchbymakes_module"]/div[2]/div/div[@class="marq_listbox"]/div/a/@href').getall()
        for brand in car_brands:
            print("++++++++++++"+brand)
            yield response.follow(brand, callback=self.parse_brands)

    def parse_brands(self, response):
        car_models = response.xpath('//*[@id="searchbymodels_module"]/div[3]/div[1]/div[1]/div[1]/a/@href').getall()
        for model in car_models:
            print("++++++++"+model)
            yield response.follow(model, callback=self.parse_models)

    def parse_models(self, response):
        car_versions = response.xpath('//*[@id="searchbytrims_module"]/div[3]/div[3]/div[4]/div[2]/div[@class="fini_item"]/div[@class="infocont"]/a/@href').getall()
        for version in car_versions:
            print("++++++++++"+version)
            yield response.follow(version, callback=self.get_names)

    def get_names(self, response):
        car_names = response.xpath('//*[@id="marq_header_wrapper"]/div[1]/span[@class="label"]/text()').get()
        car_subname = response.xpath('//*[@id="marq_header_wrapper"]/div[1]/span/h5/text()').get()
        
        name = car_names if car_names else ""
        subname = car_subname if car_subname else ""
        print("++++++++"+name+subname)
        
        yield {
            "name": (name + " " + subname).strip()
        }


