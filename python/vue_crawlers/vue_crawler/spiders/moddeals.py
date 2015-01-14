'''
Created on sept 13, 2014

@author: vazeer

'''

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem


class ModdealsSpider(CrawlSpider):
  name = "moddeals"
  allowed_domains = ['moddeals.com']
  start_urls = ['http://www.moddeals.com/']
  rules = (
    # Extract the different pages on the main site.
    Rule(SgmlLinkExtractor(restrict_xpaths='//ul[@class="sub_cat_main"]')),
    
    Rule(SgmlLinkExtractor(restrict_xpaths='(//a[@class="paging_next paging_text_active"]/@href)[1]')),
      # Extract the different items on the page.
    Rule(SgmlLinkExtractor(restrict_xpaths='//li[@class="quickview"]'), callback='parse_item')
  )

  def parse_item(self, response):
#     print response.url
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
    item_num_str = sel.xpath('//a[@class="review_link write_review"]/@reviewid').extract()[0]
    item_num = re.findall(r'\d+', item_num_str)[0]
    item['source_site'] = "moddeals.com"
    item['product_title'] = str(sel.xpath('//h1[@itemprop="name"]//text()').extract()[0])
    item['product_item_num'] = item_num
    item['product_url'] = response.url
    item['description'] = sel.xpath('//div[@itemprop="description"]//p/text()').extract()
    item['image_urls'] = [sel.xpath('//img[@itemprop="image"]/@src').extract()[0]]
#    bullet_description = sel.xpath('//ul[@class="product-description"]//li/text()').extract()
#    for desc_bullet in bullet_description:
#      if desc_bullet.strip():
#        item['description'].append(desc_bullet.strip())
    return item

  def PriceExtractor(self, item, selector):
    price = selector.xpath('//span[@itemprop="price"]/text()').extract()
    item['list_price'] = price[0]
