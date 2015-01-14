'''
Created on Sept 12, 2014

@author: vazeer
'''

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem


class ShopbobSpider(CrawlSpider):
  name = "shopbop"
  allowed_domains = ['shopbop.com']
  start_urls = ['http://www.shopbop.com/#cs=ov=3470322056,os=16,link=shopbopDomainHeader']
  rules = (
    # Extract the different pages on the main site.
    Rule(SgmlLinkExtractor(restrict_xpaths='//ul[@class="subnav"]')),
    
    Rule(SgmlLinkExtractor(restrict_xpaths='//ul[@class="leftNavSubcategory sub-nav"]//a')),
      # Extract the different items on the page.
    Rule(SgmlLinkExtractor(restrict_xpaths='//div[@class="info clearfix"]//a'), callback='parse_item')
  )

  def parse_item(self, response):
#     print response.url
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
    item_num_str = sel.xpath('//div[@id="productId"]//text()').extract()[0]
    item_num = re.findall(r'\d+', item_num_str)[0]
    item['source_site'] = "shopbop.com"
    item['product_title'] = str(sel.xpath('//h1[@class="brand-heading"]//text()').extract()[0])
    item['product_item_num'] = item_num
    item['product_url'] = response.url
    item['description'] = sel.xpath('//div[@itemprop="description"]//text()').extract()
    item['image_urls'] = [sel.xpath('//img[@id="productImage"]/@src').extract()[0]]
#    bullet_description = sel.xpath('//ul[@class="product-description"]//li/text()').extract()
#    for desc_bullet in bullet_description:
#      if desc_bullet.strip():
#        item['description'].append(desc_bullet.strip())
    return item

  def PriceExtractor(self, item, selector):
    price = selector.xpath('//span[@class="salePrice"]//text()|(//meta[@itemprop="price" and not(//span[@class="salePrice"]//text())]/@content)[1]').extract()
    item['list_price'] = price[0]
