# from scrapy.exceptions import DropItem
#
#
# class FilterWordsPipeline(object):
#     """A pipeline for filtering out items which contain certain words in their
#     description"""
#
#     # put all words in lowercase
#     words_to_filter = ['politics', 'religion']
#
#     def process_item(self, item, spider):
#         for word in self.words_to_filter:
#             if word in unicode(item['description']).lower():
#                 raise DropItem("Contains forbidden word: %s" % word)
#         else:
#             return item

import json

class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('items_komen_rss_feedpider2.json', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
