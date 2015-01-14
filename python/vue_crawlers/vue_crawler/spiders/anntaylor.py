'''
Created on sept 13, 2014

@author: vazeer

the web site is not only for us so prices are INR when we run from india
'''

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem


class AnntaylorSpider(CrawlSpider):
  name = "anntaylor"
  allowed_domains = ['anntaylor.com']
  start_urls = ['http://www.anntaylor.com/']
  rules = (
    # Extract the different pages on the main site.
    Rule(SgmlLinkExtractor(restrict_xpaths='//div[@id="nav-site"]')),
    
     Rule(SgmlLinkExtractor(restrict_xpaths='//a[@class="next"]')),
      # Extract the different items on the page.
    Rule(SgmlLinkExtractor(restrict_xpaths='//a[@class="clickthrough"]'), callback='parse_item')
  )

  def parse_item(self, response):
#     print response.url
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
    item_num_str = sel.xpath('//input[@name="prodId"]/@value').extract()[0]
    item_num = re.findall(r'\d+', item_num_str)[0]
    item['source_site'] = "anntaylor.com"
    item['product_title'] = str(sel.xpath('//meta[@property="og:title"]/@content').extract()[0])
    item['product_item_num'] = item_num
    item['product_url'] = response.url
    item['description'] = sel.xpath('//div[@class="gu description"]//p/text()|//div[@class="details"]//p/text()').extract()
    item['image_urls'] = [sel.xpath('//img[@id="productImage"]/@src').extract()[0]]
#    bullet_description = sel.xpath('//ul[@class="product-description"]//li/text()').extract()
#    for desc_bullet in bullet_description:
#      if desc_bullet.strip():
#        item['description'].append(desc_bullet.strip())
    return item

  def PriceExtractor(self, item, selector):
    price = selector.xpath('//span[@itemprop="price"]/text()').extract()
    item['list_price'] = price[0]
