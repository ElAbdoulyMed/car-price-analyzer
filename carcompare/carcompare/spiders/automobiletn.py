from cherrypy import response
import scrapy
from transformation.normalization.cars import normalize_name
from scrapy_playwright.page import PageMethod

class AutomobileTnSpider(scrapy.Spider):
    name="automobiletn"
    collection_to_use = "cars"
    def start_requests(self):
        start_url= "https://www.automobile.tn/fr/neuf"
        yield scrapy.Request(url=start_url,callback=self.parse, meta={
            "playwright": True,
            "playwright_page_methods": [
                PageMethod("wait_for_selector", "div.brands-list"),
                PageMethod("wait_for_load_state", "networkidle")
            ]
        })
        
    def parse(self,response) :
        brands_list=response.css("div.brands-list>a::attr(href)").extract()
        for brand in brands_list :
            brand_name = normalize_name(brand.split('/')[-1])
            yield {
                "collection":"manufacturers",
                "name":brand_name
            }
            yield response.follow(brand,callback=self.parse_brand, meta={
            "playwright": True,
            "playwright_page_methods": [
                PageMethod("wait_for_selector", "div.articles"),
                PageMethod("wait_for_load_state", "networkidle")
            ]
        })
            
    def parse_brand(self,response):
        cars_list=response.xpath('//div[@class="articles"]/span/div/a/@href').extract()
        for car in cars_list:
            yield response.follow(car, callback=self.parse_car, meta={
            "playwright": True,
            "playwright_page_methods": [
                PageMethod("wait_for_selector", "#content_container"),
                PageMethod("wait_for_load_state", "networkidle") 
            ]
        })

    def parse_car(self,response):
        if (response.xpath('name(//*[@id="detail_content"]/div[1]/*[2])').extract_first()!='table'):            
            cars_names_list = response.css('h3.page-title')
            car_price = response.xpath('//*[@id="detail_content"]/div[1]/div[2]/div/span/text()').extract_first()
            for car_name in cars_names_list:
                car_full_name = " ".join(car_name.css('*::text').getall())
            brand = response.xpath('//*[@id="content_container"]/div[3]/ul/li[2]/a/text()').extract_first()
            fuel_type = response.xpath('//th[text()="Energie "]/following-sibling::*[1]/text()').get()
            nb_cylinders = response.xpath('//th[text()="Nombre de cylindres"]/following-sibling::*[1]/text()').get()
            capacity = response.xpath('//th[text()="Cylindrée"]/following-sibling::*[1]/text()').get()
            power=response.xpath('//th[text()="Puissance (ch.din)"]/following-sibling::*[1]/text()').get()
            gear=response.xpath('//th[text()="Boîte"]/following-sibling::*[1]/text()').get()
            battery=response.xpath('//th[text()="Batterie"]/following-sibling::*[1]/text()').get()
            doors = response.xpath('//th[text()="Nombre de portes"]/following-sibling::*[1]/text()').get()
            body_type = response.xpath('//th[text()="Carrosserie"]/following-sibling::*[1]/text()').get()
            print("DEBUG :",car_full_name,car_price,brand,fuel_type,nb_cylinders,capacity,power,gear,battery,doors,body_type)
            yield{
                "collection" : "cars",
                "manufacturer_id" : normalize_name(brand),
                "manufacturer_name" :normalize_name(brand),
                "seller_name" : self.name,
                "name": car_full_name,
                "price":car_price,
                "energy":fuel_type,
                "cylinder_count":nb_cylinders,
                "capacity_(CC)":capacity,
                "power_(HP)":power,
                "gearbox":gear,
                "battery_(KWh)":battery,
                "door_count":doors,
                "body_type":body_type
            }
        else:
            cars_versions_list = response.xpath('//*[@id="detail_content"]/div[1]/table/tbody/tr/td[1]/a/@href').extract()
            for car_version in cars_versions_list:
                yield response.follow(car_version,callback=self.parse_car, meta={
            "playwright": True,
            "playwright_page_methods": [
                PageMethod("wait_for_selector", "#content_container"),
                PageMethod("wait_for_load_state", "networkidle")
            ]
        })


