# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.spiders import CrawlSpider, Rule


class BossSpider(CrawlSpider):
    name = 'boss'
    allowed_domains = ['www.zhipin.com']
    start_urls = ['https://www.zhipin.com/c101020100-p100101/b_%E6%B5%A6%E4%B8%9C%E6%96%B0%E5%8C%BA-a_%E5%BC%A0%E6%B1%9F/?page=1&ka=page-1']

    headers = {
        ":authority": "www.zhipin.com",
        ":method": "GET",
        ":scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        "cookie": "toUrl=/; JSESSIONID=""; lastCity=101020100; __zp_seo_uuid__=795dacbb-1359-487b-9567-3b3d30b70250; __g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1599206794,1599206815; __c=1599206791; __l=r=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DRAdenCTyKQit2EVk1SisgNk0fEeElsLgtiSAF7Pm3PWKVRwSNGmtOG-mnAV9x2T9%26wd%3D%26eqid%3Ddc36e424000070b7000000055f51f598&l=%2Fwww.zhipin.com%2Fjob_detail%2Fde9868d400ff36770XB_3dq0E1s~.html%3Fka%3Dsearch_list_jname_21_blank%26lid%3Dnlp-1kQHeB0mVID.search.21&g=&friend_source=0&friend_source=0; __a=97110935.1599206794..1599206791.38.1.38.38; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1599310096; __zp_stoken__=0b92bC1xIfDxVLmV8OkpsGgdVNRdaImxgKWdib15kBiMWUDYeBAFCP08%2BcHoseiAFR24lExgUR0REKW4aNF9GISYpdEsjJwg8ZSk%2BeHBGQSoqQS4rKjw8Th4xZiwbHVwxQT9YdVw8HE5FVVF5Pg%3D%3D"
    }

    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        print(response.url)
        item = {}
        job_list = response.xpath('//div[@id="main"]/div/div[@class="job-list"]/ul/li')
        for li in job_list:
            href = li.xpath('.//div[@class="primary-wrapper"]/div[@clas'
                            's="primary-box"]/@href').extract_first("")
            data_lid = li.xpath('.//div[@class="primary-wrapper"]/div[@class="primary-box"]/@data-lid').extract_first("")
            data_item_id = li.xpath('.//div[@class="primary-wrapper"]/div[@class="primary-box"]/@data-itemid').extract_first("")
            url_detail = "https://www.zhipin.com" + href + "?ka=search_list_jname_" + data_item_id + "_blank" + "&lid=" + data_lid
            print(url_detail)
            yield scrapy.Request(url=url_detail, callback=self.parse_detail)
        return item

    def parse_detail(self, response):
        job_info = response.xpath('//*[@id="main"]/div[3]/div/div[2]/div[2]/div[1]/div/text()').get()
        time.sleep(2000)
        print(job_info)

