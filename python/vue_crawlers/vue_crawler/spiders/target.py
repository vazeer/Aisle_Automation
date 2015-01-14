'''
Created on Sept 12, 2014

@author: vazeer
'''

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem


class TargetSpider(CrawlSpider):
  name = "target"
  allowed_domains = ['target.com']
  start_urls = ['http://www.target.com/c/women/-/N-5xtd3#?lnk=ct_menu_01_1&intc=1865087|null']
  rules = (
    # Extract the different pages on the main site.
    Rule(SgmlLinkExtractor(restrict_xpaths='//div[@id="leftNavShopLinks"]')),
    
     Rule(SgmlLinkExtractor(restrict_xpaths='//ul[@class="pagination1"]')),
      # Extract the different items on the page.
    Rule(SgmlLinkExtractor(restrict_xpaths='//div[@class="productTitle"]//a'), callback='parse_item')
  )

  def parse_item(self, response):
#     print response.url
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
    item_num_str = sel.xpath('//input[@class="zoomItemPartNum"]/@value').extract()[0]
    item_num = re.findall(r'\d+', item_num_str)[0]
    item['source_site'] = "target.com"
    item['product_title'] = str(sel.xpath('//meta[@property="og:title"]/@content').extract()[0])
    item['product_item_num'] = item_num
    item['product_url'] = response.url
    item['description'] = sel.xpath('//span[@itemprop="description"]/text()|//ul[@class="context-buttom-gap innerlistings"]//li/text()').extract()
    item['image_urls'] = [sel.xpath('//img[@itemprop="image"]/@src').extract()[0]]
#    bullet_description = sel.xpath('//ul[@class="product-description"]//li/text()').extract()
#    for desc_bullet in bullet_description:
#      if desc_bullet.strip():
#        item['description'].append(desc_bullet.strip())
    return item

  def PriceExtractor(self, item, selector):
    price = selector.xpath('//span[@itemprop="price"]/text()').extract()
    item['list_price'] = price[0]
