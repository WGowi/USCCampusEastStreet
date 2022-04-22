# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import time

# useful for handling different item types with a single interface
import pymysql

from usc_sunshine.settings import DB_host, DB_username, DB_password, DB_name


class UscSunshinePipeline:
    def process_item(self, item, spider):
        return item


class DataSavePipeline:
    def __init__(self):
        self.cursor = None
        self.db = None
        self.start_time = None
        self.end_time = None

    def open_spider(self, spider):  # 连接数据库
        self.start_time = time.time()
        self.db = pymysql.connect(host=DB_host, user=DB_username, password=DB_password, database=DB_name)
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):  # 对数据进行持久化存储
        if spider.name == 'Lost_and_found':
            if item['kind'] == '寻物启事':
                sql = "insert into Lost (id,title, description, contact, tel, find_or_lost_address, find_or_lost_time, black_address, public_time,img_url) VALUE ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                    item['id'], item['title'], item['description'], item['contact'], item['tel'],
                    item['find_or_lost_address'], item['find_or_lost_time'], item['black_address'], item['public_time'],
                    item['img_url'])
            else:
                sql = "insert into Found (id,title, description, contact, tel, find_or_lost_address, find_or_lost_time, black_address, public_time,img_url) VALUE ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                    item['id'], item['title'], item['description'], item['contact'], item['tel'],
                    item['find_or_lost_address'], item['find_or_lost_time'], item['black_address'], item['public_time'],
                    item['img_url'])

        if spider.name == 'complaint':
            sql = "insert into Info(id,title, kind, department, public_time, content, reply,img_url,identity) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (
                repr(item['id']), repr(item['title']), repr(item['kind']), repr(item['department']),
                repr(item['public_time']), repr(item['content']),
                repr(item['reply']), repr(item['img_url']), repr(item['identity']))

        print(sql)
        self.cursor.execute(sql)
        self.db.commit()

    def close_spider(self, spider):  # 关闭数据库连接
        self.cursor.close()
        self.db.close()
        self.end_time = time.time()
        print("用时:" + str(self.end_time - self.start_time) + 's')
