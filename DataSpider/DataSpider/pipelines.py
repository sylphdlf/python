# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from ..Utils.MysqlUtils import MysqlUtils


class DataspiderPipeline(object):

    @staticmethod
    def process_item(item, spider):
        return item


class AmapPipeline(object):

    @staticmethod
    def process_item(item, spider):
        # 将爬取的信息保存到mysql
        sql = ["insert into p_amap(type, origin, destination, waypoints, time_cost, distance) "
               "value ({}, '{}', '{}', '{}', '{}', '{}')"
                   .format(item['type'], item['origin'], item['destination'], item['waypoints'], item['time_cost'], item['distance'])]
        MysqlUtils.insert(sql)
        return item
