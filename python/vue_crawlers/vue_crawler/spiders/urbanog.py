'''
Created on sept 13, 2014

@author: vazeer

'''

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem


class UrbanogSpider(CrawlSpider):
  name = "urbanog"
  allowed_domains = ['urbanog.com']
  start_urls = ['http://www.urbanog.com/index.html']
  rules = (
    # Extract the different pages on the main site.
    Rule(SgmlLinkExtractor(restrict_xpaths='//span[@class="span2"]')),
    
     Rule(SgmlLinkExtractor(restrict_xpaths='//a[preceding-sibling::span[@class="sp1"]]/@href')),
      # Extract the different items on the page.
    Rule(SgmlLinkExtractor(restrict_xpaths='//p[@class="title"]'), callback='parse_item')
  )

  def parse_item(self, response):
#     print response.url
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
    item_num_str = sel.xpath('//input[@name="pid"]/@value').extract()[0]
    item_num = re.findall(r'\d+', item_num_str)[0]
    item['source_site'] = "urbanog.com"
    item['product_title'] = str(sel.xpath('//title/text()').extract()[0])
    item['product_item_num'] = item_num
    item['product_url'] = response.url
    item['description'] = sel.xpath('//h2[@class="prod-sec1"]//p/text()').extract()
    item['image_urls'] = [sel.xpath('//ul[@id="image_list"]//img/@src').extract()[0]]
#    bullet_description = sel.xpath('//h2[@class="prod-sec1"]//p/text()').extract()
#    for desc_bullet in bullet_description:
#      if desc_bullet.strip():
#        item['description'].append(desc_bullet.strip())
    return item

  def PriceExtractor(self, item, selector):
    price = selector.xpath('//div[@class="product-price"]//text()').extract()
    item['list_price'] = price[0]
