'''
Created on Aug 18, 2014

@author: Vazeer
'''

import re
import urlparse

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor


from vue_crawler.items import VueCrawlerItem


class IgigiSpider(CrawlSpider):
  name = "igigi"
  allowed_domains = ['igigi.com']
  start_urls = ['http://www.igigi.com/']
  rules = (
      # Extract the different pages on the main site.
    Rule(SgmlLinkExtractor(restrict_xpaths='//div[@class="inner"]')),
    
    Rule(SgmlLinkExtractor(restrict_xpaths='//div[@id="testimonials"]')),

    Rule(SgmlLinkExtractor(restrict_xpaths='//div[@class="photo"]//a'), callback='parse_item')
  )

  def parse_item(self, response):
    print '*********************************** URL:', response.url
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
    item_num_str = sel.xpath('//input[@name="product"]/@value').extract()[0]
    item_num = re.findall(r'\d+', item_num_str)[0]
    item['source_site'] = "igigi.com"
    item['product_title'] = str(sel.xpath('//meta[@property="og:title"]/@content').extract())
    item['product_item_num'] = item_num  
    item['product_url'] = response.url
    item['description'] = sel.xpath('//p[@itemprop="description"]//text()').extract()
    item['image_urls'] = [sel.xpath('//a[@id="d1"]/@href').extract()[0]]

    return item

  def PriceExtractor(self, item, selector):
    prod_price = selector.xpath('//span[@class="price"]//text()').extract()
    for price in prod_price:
      if re.search(r"Was (\$\d*\.\d\d)", price):
        item['list_price'] = re.search(r"Was (\$\d*\.\d\d)", price).group(1)
      if re.search(r"Reg. (\$\d*\.\d\d)", price):
        item['list_price'] = re.search(r"Reg. (\$\d*\.\d\d)", price).group(1)
      elif re.search(r"Sale (\$\d*\.\d\d)", price):
        item['sale_price'] = re.search(r"Sale (\$\d*\.\d\d)", price).group(1)
      elif re.search(r"(\$\d*\.\d\d)", price):
        item['list_price'] = re.search(r"(\$\d*\.\d\d)", price).group(1)
