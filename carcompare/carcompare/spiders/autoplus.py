import scrapy
from transformation.normalization.cars import normalize_name
class AutoplusSpider(scrapy.Spider):
    name = "autoplus"
    collection_to_use = "cars"

    def start_requests(self):
        url = "https://www.auto-plus.tn/les-voitures-neuves.html"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        car_brands = response.xpath('//*[@id="searchbymakes_module"]/div[2]/div/div[@class="marq_listbox"]/div/a/@href').getall()
        for brand in car_brands:
            car_name = normalize_name(brand.split('/')[-1])
            yield response.follow(brand, callback=self.parse_brands,meta={'playwright' : True})
            yield{
                "collection" : "manufacturers",
                "name" : car_name
            }

    def parse_brands(self, response):
        if (response.xpath('name(//*[@id="tUtilitaire"]/*[1])').get()) == 'h4':
            car_uts = response.xpath('//*[@id="searchbymodels_module"]/div[3]/div[3]/div/div[1]/div[2]/a/@href').getall()
            for car_ut in car_uts :
                yield response.follow(car_ut,callback=self.parse_models,meta={'playwright' : True})
        car_models = response.xpath('//*[@id="searchbymodels_module"]/div[3]/div[1]/div[@class="model_listbox"]/div[@class="content"]/a/@href').getall()
        for model in car_models:
            yield response.follow(model, callback=self.parse_models,meta={'playwright' : True})

    def parse_models(self, response):
        car_versions = response.xpath('//*[@id="searchbytrims_module"]/div[3]/div[3]/div[4]/div[2]/div[@class="fini_item"]/div[@class="infocont"]/a/@href').getall()
        for version in car_versions:
            yield response.follow(version, callback=self.get_info,meta={'playwright' : True})

    def get_info(self, response):
        car_names = response.xpath('//*[@id="marq_header_wrapper"]/div[1]/span[@class="label"]/text()').get()
        car_subname = response.xpath('//*[@id="marq_header_wrapper"]/div[1]/span/h5/text()').get()
        name = car_names if car_names else ""
        subname = car_subname if car_subname else ""
        car_brand = response.xpath('//*[@id="breadcrumb"]/li[3]/a/text()').extract_first()
        car_energie = response.xpath('//li[span/b[text()="Energie "]]/*[2]/text()').get()            
        car_prices = response.xpath('//*[@id="searchbytrims_module"]/div[3]/div[2]/div[2]/b/text()').get()
        car_cylindre = response.xpath('//li[span/b[text()="Cylindrée"]]/*[2]/text()').get()
        car_nb_cylindre = response.xpath('//li[span/b[text()="Nombre de cylindres"]]/*[2]/text()').get()
        car_puiss = response.xpath('//li[span/b[text()="Puissance (ch.din)"]]/*[2]/text()').get()
        car_boite = response.xpath('//li[span/b[text()="Boîte"]]/*[2]/text()').get()
        car_batterie = response.xpath('//li[span/b[text()="Batterie"]]/*[2]/text()').get()
        car_portes = response.xpath('//li[span/b[text()="Nombre de portes"]]/*[2]/text()').get()
        car_caros = response.xpath('//li[span/b[text()="Carrosserie"]]/*[2]/text()').get()
        
        yield {
            "collection" : "cars",
            "manufacturer_id" : normalize_name(car_brand),
            "manufacturer_name" : normalize_name(car_brand),
            "name": (name + " " + subname).strip(),
            "price" : (car_prices),
            "energy" : (car_energie),
            "cylinder_count" : (car_nb_cylindre),
            "capacity_(CC)" : (car_cylindre[:-4] if car_cylindre else None),
            "power_(HP)" : (car_puiss),
            "gearbox" : (car_boite),
            "battery_(kWh)" : (car_batterie),
            "door_count" : (car_portes),
            "body_type" : (car_caros)
        }
                
    


