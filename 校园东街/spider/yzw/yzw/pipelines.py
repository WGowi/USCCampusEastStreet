# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd
import pymysql
import time
from .settings import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD


class YzwPipeline:
    def __init__(self):
        self.cursor = None
        self.db = None
        self.start_time = None
        self.end_time = None
        self.mldm = None
        self.style = None

    # 对数据进行持久化存储
    def process_item(self, item, spider):
        for i in range(1, 5):
            item["Lesson_" + str(i)] = self.process_lesson(item["Lesson_" + str(i)])

        # ****************************************************
        # 存入数据库
        print("准备将数据存入数据库！！！")
        key_sql = "\"" + str(item['School']) + '\",\"' + str(item['Disciplines']) + '\",\"' + str(
            item['Subject_Category']) + '\",\"' + str(item['College']) + '\",\"' + str(item[
                                                                                           'Major']) + '\",\"' + str(
            item['Research_Direction']) + '\",\"' + str(item['Number']) + '\",\"' + str(
            item['Lesson_1']) + '\",\"' + str(item[
                                                  'Lesson_2']) + '\",\"' + str(
            item['Lesson_3']) + '\",\"' + str(item['Lesson_4']) + '\",\"' + str(item['Place']) + '\",\"' + str(item[
                                                                                                                   'Graduate_School']) + '\",\"' + str(
            item['Self_Scribing']) + '\",\"' + str(item['PhD']) + '\",\"' + str(item[
                                                                                    'Instructor']) + '\",\"' + str(
            item['Learning_Style']) + '\",\"' + str(item['Remarks']) + '\"'
        sql = 'insert into YZW (School,Disciplines,Subject_Category,College,Major,Research_Direction,Number,Lesson_1,Lesson_2,Lesson_3,Lesson_4,Place,Graduate_School,Self_Scribing,PhD,Instructor,Learning_Style,Remarks) values (' + key_sql + ')'

        self.cursor.execute(sql)
        self.db.commit()
        print("已执行完成sql语句:\n" + sql)
        # print(sql)
        self.mldm = item['Disciplines']
        self.yjxkmd = item['Subject_Category']
        self.style = item['Learning_Style']

        return item

    # 对字符串进行处理
    def process_lesson(self, lesson):
        lesson.replace('\n', '')
        lesson.replace('\r', '')
        lesson = lesson.strip()
        return lesson

    # 连接数据库
    def open_spider(self, spider):
        self.start_time = time.time()
        self.db = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        self.cursor = self.db.cursor()

    # 断开数据库连接
    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()
        self.end_time = time.time()
        print("finish!!!,用时共:%f" % (self.end_time - self.start_time) + 's')
