import scrapy

class AutomobileTnSpider(scrapy.Spider):
    name="automobiletn"
    collection_to_use = "cars"
    def start_requests(self):
        start_url= "https://www.automobile.tn/fr/neuf"
        yield scrapy.Request(url=start_url,callback=self.parse)
        
    def parse(self,response) :
        brands_list=response.css("div.brands-list>a::attr(href)").extract()
        for brand in brands_list : 
            print(brand)
            yield response.follow(brand,callback=self.parse_brand)
            
    def parse_brand(self,response):
        cars_list=response.xpath('//div[@class="articles"]/span/div/a/@href').extract()
        #car_price = response.xpath('//*[@id="w1"]/div[4]/span[1]/div/a/div/span/text()').extract_first().strip()
        for car in cars_list:
            yield response.follow(car,
                                  callback=self.parse_car,
                                  #meta={'price':car_price}
                        )
                 
    def parse_car(self,response):
        if (response.xpath('name(//*[@id="detail_content"]/div[1]/*[2])').extract_first()!='table'):
            cars_names_list = response.css('h3.page-title')
            #car_price=response.meta.get('price')
            car_price = response.xpath('//*[@id="detail_content"]/div[1]/div[2]/div/span/text()').extract_first()
            for car_name in cars_names_list:
                car_full_name = " ".join(car_name.css('*::text').getall())
            fuel_type = response.xpath('//th[text()="Energie "]/following-sibling::*[1]/text()').get()
            nb_cylinders = response.xpath('//th[text()="Nombre de cylindres"]/following-sibling::*[1]/text()').get()
            capacity = response.xpath('//th[text()="Cylindrée"]/following-sibling::*[1]/text()').get()
            power=response.xpath('//th[text()="Puissance (ch.din)"]/following-sibling::*[1]/text()').get()
            gear=response.xpath('//th[text()="Boîte"]/following-sibling::*[1]/text()').get()
            battery=response.xpath('//th[text()="Batterie"]/following-sibling::*[1]/text()').get()
            doors = response.xpath('//th[text()="Nombre de portes"]/following-sibling::*[1]/text()').get()
            body_type = response.xpath('//th[text()="Carrosserie"]/following-sibling::*[1]/text()').get()
            print("DEBUG:", car_full_name, car_price, fuel_type)
            yield{  
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
                yield response.follow(car_version,callback=self.parse_car)


