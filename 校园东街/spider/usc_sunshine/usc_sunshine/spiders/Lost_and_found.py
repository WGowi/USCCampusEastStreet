import os

import oss2
import requests
import scrapy
from scrapy_splash import SplashRequest
from usc_sunshine.items import Lost_and_found_Item
import re

from ..settings import AccessKeyId, endpoint, bucketName, AccessKeySecret, oss_url


def ImgToOSS(id, local_img_name, oss_img_name, oss_url):
    id = str(id)

    url = 'http://nhedu.tabbyedu.com/dwr/call/plaincall/ExtAjax.downloadForLostProperty.dwr'
    payload = {
        "callCount": "1",
        "nextReverseAjaxIndex": "0",
        "c0-scriptName": "ExtAjax",
        "c0-methodName": "downloadForLostProperty",
        "c0-id": "0",
        "c0-param0": "string:" + id,
        "batchId": "1",
        "instanceId": "0",
        "page": "%2Fcolumn%2Fswzlxq%2Findex.shtml%3Fid%3D1647436117403",
        "scriptSessionId": "sA3sjWZyUndkvd3rowesyJz1eQpVvuOCB1o/g7yCB1o-jaNxkt0Tf",
    }

    r = requests.post(url, data=payload)
    resp = r.text
    img_url = "http://nhedu.tabbyedu.com" + \
              re.compile('''dwr.engine.remote.handleCallback\("\d+","\d+",'(.*?)'\);''').findall(resp)[0]

    r = requests.get(img_url)
    with open(local_img_name, 'wb') as f:
        f.write(r.content)

    auth = oss2.Auth(AccessKeyId, AccessKeySecret)
    bucket = oss2.Bucket(auth, endpoint, bucketName)
    bucket.put_object_from_file(oss_img_name, local_img_name)
    os.remove(local_img_name)
    img_oss_url = oss_url + oss_img_name
    return img_oss_url


class LostAndFoundSpider(scrapy.Spider):
    name = 'Lost_and_found'
    allowed_domains = ['nhedu.tabbyedu.com']
    start_urls = ['http://nhedu.tabbyedu.com/column/swlt/index.shtml']

    def start_requests(self):
        yield SplashRequest(
            url=self.start_urls[0],
            callback=self.parse,
            args={"wait": 10},
            endpoint="render.html",
        )

    def parse(self, response):
        item = Lost_and_found_Item()
        tr_list = response.xpath("//table[@id='list']/tr")
        for tr in tr_list:
            item['title'] = tr.xpath("./td[2]/a/text()").extract_first().replace("\n", '').strip()
            item['detail_href'] = "http://" + self.allowed_domains[0] + tr.xpath(
                ".//a[@target='_blank']/@href").extract_first()
            item['public_time'] = tr.xpath(".//td[@align='left'][2]/text()").extract_first().replace('\n', '').strip()
            condition = tr.xpath(".//a[@target='_blank']/font/text()").extract_first()
            item['id'] = re.findall(r"\d.*", item['detail_href'])[0]
            if condition == '(寻找中)':
                yield SplashRequest(
                    url=item['detail_href'],
                    callback=self.parse_detail,
                    args={"wait": 10},
                    endpoint="render.html",
                    meta={"item": item}
                )
        next_page_lua_script = """
               function main(splash, args)
                  assert(splash:go(args.url))
                  assert(splash:wait(0.5))
                  splash:runjs(args.script)
                  assert(splash:wait(0.5))
                  return splash:html()
                end
               """
        cur_page = response.xpath("//span[@class='pagebox_num_nonce']/text()").extract_first()
        page_info = \
            response.xpath("//span[@class='pagebox_pre_nolink']/text()").extract_first().split('，')[-1].split('页')[0]
        print("cur_page:" + str(cur_page))
        if int(cur_page) < int(page_info):
            next_page_js = "javascript:gotopage(" + str(int(cur_page) + 1) + ",15)"
            yield SplashRequest(
                url=response.url,
                callback=self.parse,
                endpoint='execute',
                args={'lua_source': next_page_lua_script, 'url': response.url, 'script': next_page_js}
            )

    def parse_detail(self, response):
        item = response.meta['item']
        tr_list = response.xpath("//table[@class='form-table forminner']//tr")
        item['name'] = tr_list[0].xpath("./td[2]/text()").extract_first()
        item['description'] = tr_list[1].xpath("./td[2]/text()").extract_first()
        if tr_list[2].xpath("./td[1]/text()").extract_first() == '遗失地点：':
            item['kind'] = "寻物启事"
        else:
            item['kind'] = "失物招领"
        item['find_or_lost_address'] = tr_list[2].xpath("./td[2]/text()").extract_first()
        item['find_or_lost_time'] = tr_list[3].xpath("./td[2]/text()").extract_first()
        item['black_address'] = tr_list[4].xpath("./td[2]/text()").extract_first()
        item['contact'] = tr_list[5].xpath("./td[2]/text()").extract_first()
        item['tel'] = tr_list[6].xpath("./td[2]/text()").extract_first()
        img_name = response.xpath("//a[@title='点击下载']/text()").extract_first()

        if img_name is not None:
            # print(item['id'], img_name)
            img_kind = re.findall(r".*?(.jpeg|.png|.jpg)", img_name)[-1]
            item['img_url'] = ImgToOSS(item['id'], img_name, str(item['id']) + img_kind, oss_url)
        else:
            item["img_url"] = 'https://gowi-wx-miniapp.oss-cn-guangzhou.aliyuncs.com/no_context.png'

        # print(item)
        yield item
