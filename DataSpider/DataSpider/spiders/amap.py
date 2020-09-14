import scrapy
from ..items import AmapItem


class AmapSpider(scrapy.Spider):
    name = 'amap'
    allowed_domains = ['amap.com']
    start_urls = ['https://restapi.amap.com/v3/direction/driving'
                  '?origin=121.65325999999999,31.210759&destination=121.561736,31.192605'
                  '&waypoints=121.594228,31.197206;121.576558,31.192424&extensions=all&output=xml'
                  '&key=28d06fb2be2b3693d7ee8f4b3ed14f18']

    def parse(self, response):
        item = AmapItem()
        item['time_cost'] = response.xpath('//paths[@type="list"]/path/duration/text()').get()
        item['distance'] = response.xpath('//paths[@type="list"]/path/distance/text()').get()
        item['origin'] = '家'
        item['destination'] = '公司'
        item['waypoints'] = '1'
        item['remarks'] = ''
        item['type'] = '1'
        yield item
