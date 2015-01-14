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



class AsosSpider(CrawlSpider):
  name = "asos"
  allowed_domains = ['asos.com']
  start_urls = ['http://us.asos.com/?hrd=1' ]
  rules = (
      
  Rule(SgmlLinkExtractor(restrict_xpaths='//ul[@class="items"]')),
  
  Rule(SgmlLinkExtractor(restrict_xpaths='//div[@class="paging-wrapper"]')),
   
  Rule(SgmlLinkExtractor(restrict_xpaths='//div[@class="categoryImageDiv"]/a'), callback='parse_item')
  
  )
 
  def parse_item(self, response):
 
    sel = Selector(response)
   
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
    item_num_str = sel.xpath('//input[@id="CatwalkInventoryId"]/@value').extract()[0]
    item_num = re.findall(r'\d+', item_num_str)[0]
    item['source_site'] = "asos.com"
    item['product_title'] = str(sel.xpath('//span[@id="ctl00_ContentMainPage_ctlSeparateProduct_lblProductTitle"]/text()').extract()[0])
    item['product_item_num'] = item_num
    item['product_url'] = response.url
    item['description']=sel.xpath('//div[@class="product-description"]//text()').extract()
    item['image_urls'] = [sel.xpath('//div[@id="productImages"]//img/@src').extract()[0]]
#    bullet_description = sel.xpath('//div[@class="product-description"]//text()').extract()
#    for desc_bullet in bullet_description:
#      if desc_bullet.strip():
#        item['description'].append(desc_bullet.strip())

    return item

  def PriceExtractor(self, item, selector):
    prod_price = selector.xpath('//meta[@itemprop="price"]/@content').extract()
    item['list_price'] = prod_price[0]