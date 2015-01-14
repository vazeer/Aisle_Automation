'''
Created on sept 15, 2014

@author: vazeer

images are wrritten in script...i.e loading dynamically it is not possible to read images for thi web site 
'''

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem


class SammydressSpider(CrawlSpider):
  name = "charlotterusse"
  allowed_domains = ['charlotterusse.com']
  start_urls = ['http://www.charlotterusse.com/']
  rules = (
    # Extract the different pages on the main site.
    Rule(SgmlLinkExtractor(restrict_xpaths='//div[@class="subNavLinks_col byCat"]')),
    
    Rule(SgmlLinkExtractor(restrict_xpaths='//span[@class="showAll"]')),
      # Extract the different items on the page.
    Rule(SgmlLinkExtractor(restrict_xpaths='//div[@class="prodTitle"]'), callback='parse_item')
  )

  def parse_item(self, response):
    print '************* URL:', response.url
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
    item['source_site'] = "charlotterusse.com"
    item['product_title'] = str(sel.xpath('//div[@itemprop="name"]//text()').extract()[0])
#     item_num_str = sel.xpath('//div[@class="product-panel four columns"]'
#                              '//div[@class="style-text"]'
#                              '//span[@class="brdcrmb-style-code"]'
#                              '/text()').extract()[0]
#     item_num = re.findall(r'\d+', item_num_str)[0]
#     item['product_item_num'] = item_num
    item_num_str = sel.xpath('//input[@name="productId"]/@value').extract()[0]
    item_num = re.findall(r'\d+', item_num_str)[0]
    item['product_item_num'] = item_num
    
    item['product_url'] = response.url
    item['description'] = sel.xpath('//div[@class="richtext"]//p/text()').extract()
    item['image_urls'] = [sel.xpath('//span[@class="jqzoom"]//img/@src').extract()[0]]
    # Express dynamically loads there images so we cant easily scrap them.
#    bullet_description = sel.xpath('//div[@class="xxkkk20"]//strong/text()').extract()
#    for desc_bullet in bullet_description:
#      if desc_bullet.strip():
#        item['description'].append(desc_bullet.strip())
    return item

  def PriceExtractor(self, item, selector):
    prod_price = selector.xpath('//span[@itemprop="price"]/text()').extract()
    item['list_price'] = prod_price[0]
     
 
