# -*- coding: utf-8 -*-
import scrapy
from qiubaiPro.items import QiubaiproItem


class QiubaiSpider(scrapy.Spider):
    name = 'qiubai'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.qiushibaike.com/text/']

    # 爬取多页
    pageNum = 1  # 起始页码
    url = 'https://www.qiushibaike.com/text/page/%s/'  # 每页的url

    # 基于终端指令持久化存储
    # scrapy crawl qiubai -o ./qiubai.csv
    # def parse(self, response):
    #     #解析：作者的名称+段子内容
    #     div_list = response.xpath('//*[@id="content"]/div/div[2]/div')
    #     all_data = [] # 列表 存储所有解析到的数据 存字典
    #     for div in div_list:
    #         #xpath返回的是列表，但是列表元素一定是Selector类型的对象
    #         #extract可以将Selector对象中data参数存储的字符串提取出来
    #         # author = div.xpath('./div[1]/a[2]/h2/text()')[0].extract()
    #         author = div.xpath('./div[1]/a[2]/h2/text()').extract_first()
    #         #列表调用了extract之后，则表示将列表中每一个Selector对象中data对应的字符串提取了出来
    #         content = div.xpath('./a[1]/div/span//text()').extract()
    #         content = ''.join(content)
    #         # 定义字典
    #         dic = {
    #             'author':author,
    #             'content':content
    #         }
    #
    #         all_data.append(dic)
    #
    #
    #     return all_data

    def parse(self, response):
        # 解析：作者的名称+段子内容
        div_list = response.xpath('//*[@id="content"]/div/div[2]/div')

        for div in div_list:
            # xpath返回的是列表，但是列表元素一定是Selector类型的对象 取字符串要[0]
            # extract可以将Selector对象中data参数存储的字符串提取出来
            # author = div.xpath('./div[1]/a[2]/h2/text()')[0].extract()
            # 匿名用户的xpath./div[1]/span/h2/text()
            author = div.xpath('./div[1]/a[2]/h2/text() | ./div[1]/span/h2/text()').extract_first()
            # 使用extract_first() 需要保证返回列表中只有一个元素
            # 列表调用了extract之后，则表示将列表中每一个Selector对象中data对应的字符串提取了出来
            content = div.xpath('./a[1]/div/span//text()').extract()
            content = ''.join(content)  # 列表转字符串

            item = QiubaiproItem()
            item['author'] = author
            item['content'] = content
            print(item)
            yield item  # 将item提交给了管道

        # 爬取所有页码数据
        if self.pageNum <= 13:  # 一共爬取13页（共13页）
            self.pageNum += 1
            url = format(self.url % self.pageNum)
            # 递归爬取数据：callback参数的值为回调函数（将url请求后，得到的相应数据继续进行parse解析），递归调用parse函数
            yield scrapy.Request(url=url, callback=self.parse)
