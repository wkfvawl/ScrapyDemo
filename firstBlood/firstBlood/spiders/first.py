# -*- coding: utf-8 -*-
import scrapy


class FirstSpider(scrapy.Spider):
    # 三个参数 一个方法的解析
    # 爬虫文件的名称：就是爬虫源文件的一个唯一标识
    name = 'first'
    # 允许的域名：用来限定start_urls列表中哪些url可以进行请求发送 通常不会用 图片URL可能不属于被抓网站
    # allowed_domains = ['www.baidu.com']

    # 起始的url列表：该列表中存放的url会被scrapy自动进行请求的发送 可以允许有多个url
    # start_urls = ['https://www.baidu.com/', 'https://www.sogou.com']
    start_urls = ['https://www.qiushibaike.com/text/']

    # parse用作于数据解析：response参数表示的就是请求成功后对应的响应对象
    # def parse(self, response):
    #     print(response)

    def parse(self, response):
        # 解析：作者的名称+段子内容
        div_list = response.xpath('//*[@id="content"]/div/div[2]/div')
        print(div_list)
        all_data = []  # 存储所有解析到的数据
        for div in div_list:
            # xpath返回的是列表，但是列表元素一定是Selector类型的对象 取字符串要[0]
            # extract可以将Selector对象中data参数存储的字符串提取出来
            # author = div.xpath('./div[1]/a[2]/h2/text()')[0].extract()
            author = div.xpath('./div[1]/a[2]/h2/text() | ./div[1]/span/h2/text()').extract_first()
            # 使用extract_first() 需要保证返回列表中只有一个元素
            # 列表调用了extract之后，则表示将列表中每一个Selector对象中data对应的字符串提取了出来
            content = div.xpath('./a[1]/div/span//text()').extract()
            content = ''.join(content)  # 列表转字符串
            print(author)
            print(content)
        #     item = QiubaiproItem()
        #     item['author'] = author
        #     item['content'] = content
        #