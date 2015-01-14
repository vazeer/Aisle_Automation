'''
Created on Aug 2, 2014

@author: Vazeer
'''

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem


class BlueflySpider(CrawlSpider):
  name = "bluefly"
  allowed_domains = ['bluefly.com']
  start_urls = ['http://www.bluefly.com/a/women-clothing']
  rules = (
    # Extract the different pages on the main site.
    Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="dept-nav-section"]//ul//li'))),
    
    Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="pageNavigation"]'))),
      # Extract the different items on the page.
    Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="productShortName"]//a')),
         callback='parse_item'),
  )

  def parse_item(self, response):
#     print response.url
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
    item_num_str = sel.xpath('//input[@name="/atg/userprofiling/B2CProfileFormHandler.productId"]/@value').extract()[0]
    item_num = re.findall(r'\d+', item_num_str)[0]
    item['source_site'] = "bluefly.com"
    item['product_title'] = str(sel.xpath('//span[@class="pdpBreadCrumb product"]/text()').extract()[0])
    item['product_item_num'] = item_num
    item['product_url'] = response.url
    bullet_description = sel.xpath('//span[@class="pdpBulletContainer"]//span//text()').extract()
    item['description'] = bullet_description
#    for desc_bullet in bullet_description:
#      if desc_bullet.strip():
#        item['description'].append(desc_bullet.strip())
#        print'test**********: ',re.sub(r"\s+", " ", desc_bullet)
    item['image_urls'] = [sel.xpath('//img[@class="current-product-image"]/@src').extract()[0]]
    return item

  def PriceExtractor(self, item, selector):
    price = selector.xpath('//input[@name="rangeFinalPrice"]/@value').extract()
    item['list_price'] = price[0]
