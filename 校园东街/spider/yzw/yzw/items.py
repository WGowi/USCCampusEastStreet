# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YzwItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    School = scrapy.Field()  # 学校名称
    Place = scrapy.Field()  # 学校所在地
    Graduate_School = scrapy.Field()  # 是否有研究生院 0表示无，1表示有
    Self_Scribing = scrapy.Field()  # 是否为自划线院校 0表示无，1表示有
    PhD = scrapy.Field()  # 是否有博士点 0表示无，1表示有
    School_985 = scrapy.Field()  # 是否为985高校 0表示无，1表示有
    School_211 = scrapy.Field()  # 是否为211高校 0表示无，1表示有
    School_First_Class = scrapy.Field()  # 是否为双一流高校 0表示无，
    School_Belong = scrapy.Field()  # 学校所属
    Disciplines = scrapy.Field()  # 学科门类
    Subject_Category = scrapy.Field()  # 学科类别
    Detail_URL = scrapy.Field()
    Major = scrapy.Field()  # 专业名称
    College = scrapy.Field()  # 院系所
    Research_Direction = scrapy.Field()  # 研究方向
    Learning_Style = scrapy.Field()  # 学习方式
    Lesson_URL = scrapy.Field()
    Instructor = scrapy.Field()  # 指导老师
    Number = scrapy.Field()  # 招生人数
    Remarks = scrapy.Field()  # 备注
    Lesson_1 = scrapy.Field()  # 课程1
    Lesson_2 = scrapy.Field()  # 课程2
    Lesson_3 = scrapy.Field()  # 课程3
    Lesson_4 = scrapy.Field()  # 课程4
    pass
