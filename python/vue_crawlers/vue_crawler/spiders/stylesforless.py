'''
Created on sept 15, 2014

@author: vazeer


'''

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem


class StylesforlessSpider(CrawlSpider):
  name = "stylesforless"
  allowed_domains = ['stylesforless.com']
  start_urls = ['http://stylesforless.com/']
  rules = (
    # Extract the different pages on the main site.
    Rule(SgmlLinkExtractor(restrict_xpaths='//ul[@class="level1"]')),
    
    Rule(SgmlLinkExtractor(restrict_xpaths='(//a[@title="Next"]/@href)[1]')),
      # Extract the different items on the page.
    Rule(SgmlLinkExtractor(restrict_xpaths='//a[@class="product-image"]'), callback='parse_item')
  )

  def parse_item(self, response):
    print '************* URL:', response.url
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    
    item['source_site'] = "stylesforless.com"
    item['product_title'] = str(sel.xpath('//div[@class="product-name"]//h1/text()').extract()[0])
#     item_num_str = sel.xpath('//div[@class="product-panel four columns"]'
#                              '//div[@class="style-text"]'
#                              '//span[@class="brdcrmb-style-code"]'
#                              '/text()').extract()[0]
#     item_num = re.findall(r'\d+', item_num_str)[0]
#     item['product_item_num'] = item_num
    item_num_str = sel.xpath('//input[@name="product"]/@value').extract()[0]
    item_num = re.findall(r'\d+', item_num_str)[0]
    item['product_item_num'] = item_num
    
    item['product_url'] = response.url
    item['description'] = sel.xpath('//div[@class="std"]//text()').extract()
    item['image_urls'] = [sel.xpath('//img[@id="amasty_zoom"]/@src').extract()[0]]
    # Express dynamically loads there images so we cant easily scrap them.
#    bullet_description = sel.xpath('//div[@class="xxkkk20"]//strong/text()').extract()
#    for desc_bullet in bullet_description:
#      if desc_bullet.strip():
#        item['description'].append(desc_bullet.strip())
    price = sel.xpath('//span[@id="product-price-'+item_num+'"]/span//text()|//span[@id="product-price-'+item_num+'_clone"]//text()').extract()
   # print '##############: ',price
    item['list_price'] = price[0].strip()
    return item

 
    
     
 
