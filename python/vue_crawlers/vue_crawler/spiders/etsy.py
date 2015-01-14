'''
Created on Sep 11, 2014

@author: Vazeer
'''

import re
import urlparse

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor


from vue_crawler.items import VueCrawlerItem



class EtsySpider(CrawlSpider):
  name = "etsy"
  allowed_domains = ['etsy.com']
  start_urls = ['https://www.etsy.com/in-en/browse/women?ref=hdr',
                'https://www.etsy.com/in-en/browse/jewelry?ref=hdr',
                'https://www.etsy.com/in-en/browse/weddings?ref=hdr',
                'https://www.etsy.com/in-en/browse/men?ref=hdr',
                'https://www.etsy.com/in-en/browse/kids-category?ref=hdr']
  rules = (
      
#  Rule(SgmlLinkExtractor(restrict_xpaths='//ul[@class="browse-nav-inner hide with-pointer"]')),
  
  Rule(SgmlLinkExtractor(restrict_xpaths='//ul[@class="col col2 nav-col nav-col1"]')),
  Rule(SgmlLinkExtractor(restrict_xpaths='//ul[@class="pages"]')),
   
  Rule(SgmlLinkExtractor(restrict_xpaths='//div[@class="title"]//a'), callback='parse_item')
  
  )
 
  def parse_item(self, response):
 
    sel = Selector(response)
   
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
    item_num_str = sel.xpath('//input[@id="treasury-listing-id"]/@value').extract()[0]
    item_num = re.findall(r'\d+', item_num_str)[0]
    item['source_site'] = "etsy.com"
    item['product_title'] = str(sel.xpath('//meta[@property="og:title"]/@content').extract()[0])
    item['product_item_num'] = item_num
    item['product_url'] = response.url
    item['description']=sel.xpath('//ul[@class="properties"]//li//text()').extract()
    item['image_urls'] = [sel.xpath('//ul[@id="image-carousel"]//img/@src').extract()[0]]
#    bullet_description = sel.xpath('//div[@class="product-description"]//text()').extract()
#    for desc_bullet in bullet_description:
#      if desc_bullet.strip():
#        item['description'].append(desc_bullet.strip())

    return item

  def PriceExtractor(self, item, selector):
    prod_price = selector.xpath('//meta[@property="etsymarketplace:price"]/@content').extract()
    item['list_price'] = prod_price[0]