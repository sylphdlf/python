from scrapy import cmdline


def amap_spider():
    cmdline.execute(["scrapy", "crawl", "amap"])


if __name__ == '__main__':
    amap_spider()
