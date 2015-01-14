'''
Created on Sept 29, 2014

@author: Vazeer
'''

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem


class FoxgownSpider(CrawlSpider):
  name = "foxgown"
  allowed_domains = ['foxgown.com']
  start_urls = ['http://www.foxgown.com/']
  
  
  rules = (
    # Extract the different pages on the main site.
   # Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="wrapper"]|//div[@class="expandable-content"]'))),
    
    Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="f_left sub_nav"]'))),
    Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="pager"]'))),
      # Extract the different items on the page.
    Rule(SgmlLinkExtractor(restrict_xpaths=('//dl[@class="product_item"]')),
         callback='parse_item')
  )

  def parse_item(self, response):
#     print response.url
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
    item_num_str = sel.xpath('//input[@name="iid"]/@value').extract()[0]
    item_num = re.findall(r'\d+', item_num_str)[0]
    item['source_site'] = "foxgown.com"
    item['product_title'] = str(sel.xpath('//h1[@class="f1"]/text()').extract()[0])
    item['product_item_num'] = item_num
    item['product_url'] = response.url
    item['description'] = sel.xpath('//div[@class="desc"]//text()').extract()
    item['image_urls'] = ["http://www.foxgown.com"+sel.xpath('//img[@class="cloudzoom"]/@src').extract()[0]]
    # it need to work
    #item['image_urls'] = [sel.xpath('//a[@class="MagicThumb-swap tag"]/@rev,(//div[@id="product-image"]//img)[2]/@src').extract()[0]]
    return item

  def PriceExtractor(self, item, selector):
    price = selector.xpath('//div[@class="price clearfix"]//span[@class="amount"]/span/text()').extract()
    item['list_price'] = price
      

