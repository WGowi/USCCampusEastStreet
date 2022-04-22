# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# 提取字段
class Lost_and_found_Item(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    name = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    kind = scrapy.Field()
    contact = scrapy.Field()
    tel = scrapy.Field()
    find_or_lost_address = scrapy.Field()
    find_or_lost_time = scrapy.Field()
    black_address = scrapy.Field()
    detail_href = scrapy.Field()
    public_time = scrapy.Field()
    img_url = scrapy.Field()


class Complaint_item(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    detail_href = scrapy.Field()
    public_time = scrapy.Field()
    kind = scrapy.Field()
    department = scrapy.Field()
    content = scrapy.Field()
    condition = scrapy.Field()
    reply = scrapy.Field()
    img_url = scrapy.Field()
    identity = scrapy.Field()
