'''
Created on sept 15, 2014

@author: vazeer

'''

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem


class SammydressSpider(CrawlSpider):
  name = "sammydress"
  allowed_domains = ['sammydress.com']
  start_urls = ['http://www.sammydress.com/']
  rules = (
    # Extract the different pages on the main site.
    Rule(SgmlLinkExtractor(restrict_xpaths='//div[@class="sub_menu"]')),
    
    Rule(SgmlLinkExtractor(restrict_xpaths='//div[@class="pages tc"]')),
      # Extract the different items on the page.
    Rule(SgmlLinkExtractor(restrict_xpaths='//p[@class="proName"]'), callback='parse_item')
  )

  def parse_item(self, response):
    print '************* URL:', response.url
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
    item['source_site'] = "sammydress.com"
    item['product_title'] = str(sel.xpath('//h1[@itemprop="name"]//text()').extract()[0])
#     item_num_str = sel.xpath('//div[@class="product-panel four columns"]'
#                              '//div[@class="style-text"]'
#                              '//span[@class="brdcrmb-style-code"]'
#                              '/text()').extract()[0]
#     item_num = re.findall(r'\d+', item_num_str)[0]
#     item['product_item_num'] = item_num
    item_num_str = sel.xpath('//input[@name="goods_id"]/@value').extract()[0]
    item_num = re.findall(r'\d+', item_num_str)[0]
    item['product_item_num'] = item_num
    
    item['product_url'] = response.url
    item['description'] = sel.xpath('//div[@class="xxkkk20"]//strong/text()').extract()
    item['image_urls'] = [sel.xpath('//span[@class="jqzoom"]//img/@src').extract()[0]]
    # Express dynamically loads there images so we cant easily scrap them.
#    bullet_description = sel.xpath('//div[@class="xxkkk20"]//strong/text()').extract()
#    for desc_bullet in bullet_description:
#      if desc_bullet.strip():
#        item['description'].append(desc_bullet.strip())
    return item

  def PriceExtractor(self, item, selector):
    prod_price = selector.xpath('//span[@itemprop="price"]/@content').extract()
    item['list_price'] = prod_price[0]
      

 
