import requests
import scrapy
from yzw.items import YzwItem
from copy import deepcopy


class SsmlSpider(scrapy.Spider):
    name = 'ssml'
    allowed_domains = ['chsi.com.cn']
    mldm = 'zyxw'  # 学科门类代码 专业学位为zyxw
    yjxkmd = '0854'  # 学科类别代码
    xxfs = '2'  # 学习方式 1为全日制，2为非全日制
    start_urls = ['https://yz.chsi.com.cn/zsml/queryAction.do']
    start_urls[0] = start_urls[0] + "?mldm=" + mldm + "&yjxkdm=" + yjxkmd + "&xxfs=" + xxfs
    yjxkmd_post_url = 'https://yz.chsi.com.cn/zsml/pages/getZy.jsp'
    mldm_post_url = 'https://yz.chsi.com.cn/zsml/pages/getMl.jsp'
    # 分析学科门类
    yjxkmd_data = {
        'mldm': mldm
    }
    if mldm == 'zyxw':
        yjxkmd_json = requests.post(url=yjxkmd_post_url).json()
    else:
        yjxkmd_json = requests.post(url=yjxkmd_post_url, data=yjxkmd_data).json()
    mldm_json = requests.post(url=mldm_post_url).json()

    if mldm != 'zyxw':
        for mldm_data in mldm_json:
            if mldm_data['dm'] == mldm:
                cur_mldm = mldm_data['mc']
    else:
        cur_mldm = '专业学位'

    for yjxkmd_data in yjxkmd_json:
        if yjxkmd_data['dm'] == yjxkmd:
            cur_yjxkmd = yjxkmd_data['mc']

    # 进入学校页提取相关字段
    def parse(self, response):
        # print("进入学校页")
        item = YzwItem()
        tr_list = response.xpath("//tbody/tr")
        for tr in tr_list:
            item["School"] = tr.xpath(".//a/text()").extract_first()
            item["Place"] = tr.xpath("./td[2]/text()").extract_first()
            item["Graduate_School"] = "是" if tr.xpath(
                "./td[3]/i[@class='iconfont ch-table-tick']").extract_first() != None else "否"
            item["Self_Scribing"] = "是" if tr.xpath(
                "./td[4]/i[@class='iconfont ch-table-tick']").extract_first() != None else "否"
            item["PhD"] = "是" if tr.xpath("./td[5]/i[@class='iconfont ch-table-tick']").extract_first() != None else "否"
            item["Detail_URL"] = "https://yz.chsi.com.cn" + tr.xpath(".//a/@href").extract_first()
            item['Disciplines'] = self.cur_mldm
            item['Subject_Category'] = self.cur_yjxkmd

            yield scrapy.Request(
                url=str(item["Detail_URL"]),
                meta={"item": deepcopy(item)},
                callback=self.parse_detail,

            )
        # 翻页
        if len(response.xpath("//li[@class='lip unable ']")) == 0:
            next_url = self.start_urls[0] + "&pageno=" + str(int(response.xpath(
                "//li[@class='lip selected']/a/text()").extract_first()) + 1)
            yield scrapy.Request(
                url=next_url,
                meta={'item': deepcopy(item)},
                callback=self.parse,
            )

    # 对详情页进行字段提取
    def parse_detail(self, response):
        item = response.meta['item']
        tr_list = response.xpath("//tbody/tr")
        for tr in tr_list:
            item["College"] = tr.xpath("./td[2]/text()").extract_first()
            item["Major"] = tr.xpath("./td[3]/text()").extract_first()
            item["Research_Direction"] = tr.xpath("./td[4]/text()").extract_first()
            item['Learning_Style'] = tr.xpath("./td[5]/text()").extract_first()
            item['Instructor'] = "尚未确定" if tr.xpath("./td[6]//span/text()").extract_first() is None else tr.xpath(
                "./td[6]//span/text()").extract_first()
            item['Lesson_URL'] = "https://yz.chsi.com.cn" + tr.xpath("./td[8]/a/@href").extract_first()
            # 进入课程页
            yield scrapy.Request(
                url=item['Lesson_URL'],
                meta={"item": deepcopy(item)},
                callback=self.parse_lesson,
            )
        # 翻页
        if len(response.xpath("//li[@class='lip unable lip-last']")) == 0:
            next_url = item['Detail_URL'] + "&pageno=" + str(int(response.xpath(
                "//li[@class='lip selected']/a/text()").extract_first()) + 1)
            yield scrapy.Request(
                url=next_url,
                meta={'item': deepcopy(item)},
                callback=self.parse_detail,
            )

    # 对课程页进行字段提取
    def parse_lesson(self, response):
        item = response.meta['item']
        item['Number'] = response.xpath("//tbody/tr[4]/td[4]/text()").extract_first()
        item['Remarks'] = "无" if response.xpath(
            "//tbody/tr[5]/td[2]/span/text()").extract_first() is None else response.xpath(
            "//tbody/tr[5]/td[2]/span/text()").extract_first()
        tbody_list = response.xpath("//div[@class='zsml-result']/table/tbody[@class='zsml-res-items']")
        for tbody in tbody_list:
            item["Lesson_1"] = tbody.xpath(".//td[1]/text()").extract_first()
            item["Lesson_2"] = tbody.xpath(".//td[2]/text()").extract_first()
            item["Lesson_3"] = tbody.xpath(".//td[3]/text()").extract_first()
            item["Lesson_4"] = tbody.xpath(".//td[4]/text()").extract_first()
            # print(item)
            yield item
