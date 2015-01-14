'''
Created on Aug 6, 2014

@author: Vazeer
'''

import re
import urlparse

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor


from vue_crawler.items import VueCrawlerItem


class NeimanmarcusSpider(CrawlSpider):
  name = "neimanmarcus"
  allowed_domains = ['neimanmarcus.com']
  start_urls = ['http://www.neimanmarcus.com/']
  rules = (
      # Extract the different pages on the main site.
    Rule(SgmlLinkExtractor(restrict_xpaths='//div[@class="silo-column"]')),
    Rule(SgmlLinkExtractor(restrict_xpaths='//li[@class="pageOffset"]')),

    Rule(SgmlLinkExtractor(restrict_xpaths='//a[@class="recordTextLink"]'), callback='parse_item')
  )

  def parse_item(self, response):
 
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
    item_num_str = sel.xpath('//input[@name="/nm/formhandler/ProdHandler.productId"]/@value').extract()[0]
    item_num = re.findall(r'\d+', item_num_str)[0]
    item['source_site'] = "neimanmarcus.com"
    item['product_title'] = str(sel.xpath('//meta[@property="og:title"]/@content').extract()[0])
    item['product_item_num'] = item_num
    item['product_url'] = response.url
    item['description'] = sel.xpath('//div[@id="bottomArea"]'
                                    '//div[@id="longDescription"]/text()').extract()
    item['image_urls'] = [sel.xpath('//div[@class="img-wrap"]//img/@src').extract()[0]]
    bullet_description = sel.xpath('//div[@itemprop="description"]//li/text()').extract()
    for desc_bullet in bullet_description:
      if desc_bullet.strip():
        item['description'].append(desc_bullet.strip())

    return item

  def PriceExtractor(self, item, selector):
    prod_price = selector.xpath('//p[@class="product-price"]//text()').extract()
    item['list_price'] = prod_price[0]
