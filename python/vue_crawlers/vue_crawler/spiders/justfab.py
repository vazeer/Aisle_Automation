'''
Created on Sept 12, 2014

@author: vazeer
'''

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem


class JustfabSpider(CrawlSpider):
  name = "justfab"
  allowed_domains = ['justfab.com']
  start_urls = ['http://www.justfab.com/boot-shop-flats.htm','http://www.justfab.com/exclusive-collections.htm']
  rules = (
    # Extract the different pages on the main site.
    Rule(SgmlLinkExtractor(restrict_xpaths='//div[@class="sidenav collection"]|ul[@class="sub_menu"]')),
    
    Rule(SgmlLinkExtractor(restrict_xpaths='//div[@id="sublinks"]//a')),
      # Extract the different items on the page.
    Rule(SgmlLinkExtractor(restrict_xpaths='//div[@class="item"]//a'), callback='parse_item')
  )

  def parse_item(self, response):
#     print response.url
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
    item_num_str = sel.xpath('//div[@id="selectProductID"]//text()').extract()[0]
    item_num = re.findall(r'\d+', item_num_str)[0]
    item['source_site'] = "justfab.com"
    item['product_title'] = str(sel.xpath('//meta[@property="og:title"]/@content').extract()[0])
    item['product_item_num'] = item_num
    item['product_url'] = response.url
    item['description'] = sel.xpath('//div[@class="info"]//li/text()|//div[@class="info"]//p/text()').extract()
    item['image_urls'] = [sel.xpath('//a[@class="MagicZoomPlus"]/@href').extract()[0]]
#    bullet_description = sel.xpath('//ul[@class="product-description"]//li/text()').extract()
#    for desc_bullet in bullet_description:
#      if desc_bullet.strip():
#        item['description'].append(desc_bullet.strip())
    return item

  def PriceExtractor(self, item, selector):
    price = selector.xpath('(//span[following-sibling::em]//text())[1]').extract()
    item['list_price'] = price[0]
