import scrapy
from scrapy_splash import SplashRequest
from usc_sunshine.items import Complaint_item
from ..settings import AccessKeyId, AccessKeySecret, bucketName, endpoint,oss_url
import os
import oss2
import requests
import re


# 将js逆向获得图片url地址并图片存入阿里云对象存储中并返回其链接
def ImgToOSS(id, local_img_name, oss_img_name, oss_url):
    id = str(id)

    url = "http://nhedu.tabbyedu.com/dwr/call/plaincall/ExtAjax.downloadForGuestbook.dwr"
    payload = {
        'callCount': '1',
        'nextReverseAjaxIndex': '0',
        'c0-scriptName': 'ExtAjax',
        'c0-methodName': 'downloadForGuestbook',
        'c0-id': '0',
        'c0-param0': 'string:' + id,
        'batchId': '4',
        'instanceId': '0',
        'page': '%2Fcolumn%2Fdetail%2Findex.shtml%3Fid%3D20220269',
        'scriptSessionId': 'Krosqzmzjop4CFJv9T3sjsjAa4D8oGV6u1o/XSp7u1o-WQMXTo9Fd',
    }
    resp = requests.post(url=url, data=payload).text
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


class ComplaintSpider(scrapy.Spider):
    name = 'complaint'
    allowed_domains = ['nhedu.tabbyedu.com']
    start_urls = ['http://nhedu.tabbyedu.com/column/lbqd/index.shtml']

    # 利用splash渲染界面
    def start_requests(self):
        yield SplashRequest(
            url=self.start_urls[0],
            callback=self.parse,
            args={"wait": 10},
            endpoint="render.html",
        )

    # 对列表页字段进行提取
    def parse(self, response):
        item = Complaint_item()
        tr_list = response.xpath("//tbody[@class='list']/tr")
        for tr in tr_list:
            item['id'] = tr.xpath("./td[1]/span[@class='full']/text()").extract_first()
            item['title'] = tr.xpath("./td[2]/a/text()").extract_first()
            item['detail_href'] = 'http://nhedu.tabbyedu.com' + tr.xpath("./td[2]/a/@href").extract_first()
            item['public_time'] = tr.xpath('./td[3]/span/text()').extract_first()
            item['kind'] = tr.xpath('./td[4]/span/text()').extract_first()
            item['department'] = tr.xpath('./td[5]/span/text()').extract_first()
            item['condition'] = tr.xpath('./td[6]/span/font/text()').extract_first()
            # 进入详情页
            yield SplashRequest(
                url=item['detail_href'],
                endpoint='render.html',
                args={"wait": 10},
                callback=self.parse_detail,
                meta={'item': item}
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
        # 翻页
        if int(cur_page) < int(page_info):
            next_page_js = "javascript:gotopage(" + str(int(cur_page) + 1) + ",20)"
            yield SplashRequest(
                url=response.url,
                callback=self.parse,
                endpoint='execute',
                args={'lua_source': next_page_lua_script, 'url': response.url, 'script': next_page_js}
            )

    # 对详情页进行字段提取额
    def parse_detail(self, response):
        item = response.meta['item']
        content = response.xpath("//table[@class='t-border']//tr[5]/td[2]")[0].xpath('string(.)').extract()[0].replace(
            u'\xa0', '').strip()
        item['content'] = content
        reply = response.xpath("//table[@class='t-border']//tr[7]/td[2]")[0].xpath('string(.)').extract()[0].replace(
            u'\xa0', '').strip()
        item['reply'] = reply
        item['identity'] = response.xpath("//table[@class='t-border']//tr[4]/td[4]/text()").extract_first().strip()
        img_name = response.xpath("//a[@title='点击下载']/text()").extract_first()

        # 对详情页附件为图片的进行js逆向并存储阿里云oss中
        if img_name is not None:
            # print(item['id'], img_name)
            try:
                img_kind = re.findall(r".*?(.jpeg|.png|.jpg)", img_name)[-1]
                item['img_url'] = ImgToOSS(item['id'], img_name, str(item['id']) + img_kind, oss_url)
            except:
                item["img_url"] = 'https://gowi-wx-miniapp.oss-cn-guangzhou.aliyuncs.com/no_context.png'
        else:
            item["img_url"] = 'https://gowi-wx-miniapp.oss-cn-guangzhou.aliyuncs.com/no_context.png'

        yield item
