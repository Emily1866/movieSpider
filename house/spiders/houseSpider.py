from scrapy import Selector
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor as sle

from house.items import HouseItem
from scrapy.utils.response import get_base_url


class HouseSpider(CrawlSpider):
    name = 'house'
    allowed_domains = ['hz.fang.lianjia.com']
    start_urls = ['http://hz.fang.lianjia.com/loupan']

    rules = (Rule(sle(allow=("/pg\d{0,4}")), follow = False, callback = 'parse_item'),)

    def parse_item(self,response):
        items = []
        sel = Selector(response)
        base_url = get_base_url(response)
        houses = sel.xpath('//div[@class="resblock-desc-wrapper"]')
        for house in houses:
            item = HouseItem()
            house_name = house.xpath('div[@class="resblock-name"]/a/text()').extract()
            house_address = house.xpath('div[@class="resblock-location"]/a/text()').extract()
            house_price = house.xpath('div[@class="resblock-price"]/div[@class="main-price"]/span/text()').extract()
            house_url = house.xpath('div[@class="resblock-name"]/a/@href').extract()
            url = base_url + '/'+ ''.join(house_url).split('/')[2]

            item['house_name']=house_name
            item['house_address']=house_address
            item['house_price']=house_price[0]+house_price[1].strip()
            item['house_url']=url
            items.append(item)
        return items

