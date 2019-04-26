# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class NeighborhoodFinderPipeline(object):
    neighborhoods = [
        'andrei muresanu',
        'bulgaria',
        'buna ziua',
        'centru',
        'dambul rotund',
        'gara',
        'horea'
        'gheorgheni',
        'manastur',
        'grigorescu',
        'gruia',
        'iris',
        'intre lacuri',
        'marasti',
        'someseni',
        'zorilor',
        'sopor',
        'faget',
        'borhanci',
        'becas',
        'expo transilvania',
        'iulius',
        'vivo',
        'polus',
        'floresti',
        'viteazu',
        'sigma',
        'piata unirii',
        'dorobantilor',
        'the office'
    ]

    def process_item(self, item, spider):
        for neighborhood in self.neighborhoods:
            if neighborhood in item['title'].lower():
                item['neighborhood'] = neighborhood
                return item

        for neighborhood in self.neighborhoods:
            if neighborhood in item['description'].lower():
                item['neighborhood'] = neighborhood
                return item

        item['neighborhood'] = 'not found'
        return item
