'''
Created on Jun 13, 2014

@author: Behrooz
'''

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem


class MacysSpider(CrawlSpider):
  name = "express"
  allowed_domains = ['express.com']
#   start_urls = ['http://www.express.com/clothing/Women/sec/womenCategory']
  start_urls = ['http://www.express.com/clothing/Tops/All+Tops/cat/cat430028?p=1',
                'http://www.express.com/clothing/Women/New+-+Shops/cat/cat120002',
                'http://www.express.com/clothing/Women/Dresses/cat/cat550007',
                'http://www.express.com/clothing/Women/Tops/cat/cat430028',
                'http://www.express.com/clothing/Women/Sweaters+-+Cardigans/cat/cat2012',
                'http://www.express.com/clothing/Women/Bottoms/cat/cat1500001',
                'http://www.express.com/clothing/Women/Jeans/cat/cat2005',
                'http://www.express.com/clothing/Women/Suits/cat/cat760006',
                'http://www.express.com/clothing/Women/Jackets+-+Coats/cat/cat450004',
                'http://www.express.com/clothing/Women/Lounge+-+Active/cat/cat860001',
                'http://www.express.com/clothing/Women/Swim/cat/cat1320026',
                'http://www.express.com/clothing/Women/Shoes+-+Accessories/cat/cat740011'
               ]
  rules = (
      # Extract the different items on the page.
    Rule(SgmlLinkExtractor(
      restrict_xpaths=('//ul[@class="product-info"]')),
      callback='parse_item'),
    # Extract the different pages on the main site side menu.
    Rule(SgmlLinkExtractor(restrict_xpaths=('//ul[@class="link-list"]'))),
#     # Extract page number links
#     Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="twelve columns"]'))),
  )

  def parse_item(self, response):
    print '************* URL:', response.url
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
    item['source_site'] = "express.com"
    item['product_title'] = str(sel.xpath('//div[@class="product-panel four columns"]'
                                          '//h2/text()').extract()[0])
#     item_num_str = sel.xpath('//div[@class="product-panel four columns"]'
#                              '//div[@class="style-text"]'
#                              '//span[@class="brdcrmb-style-code"]'
#                              '/text()').extract()[0]
#     item_num = re.findall(r'\d+', item_num_str)[0]
#     item['product_item_num'] = item_num
    self.ProductNumExtract(item, response.url)
    item['product_url'] = response.url
    item['description'] = sel.xpath('//div[@class="product-panel four columns"]'
                                    '//div[@class="product-description"]'
                                    '//p/text()').extract()
    # Express dynamically loads there images so we cant easily scrap them.
    bullet_description = sel.xpath('//div[@class="product-panel four columns"]'
                                   '//div[@class="product-description"]'
                                   '//div[@class="fabric-care"]'
                                   '//li/text()').extract()
    for desc_bullet in bullet_description:
      if desc_bullet.strip():
        item['description'].append(desc_bullet.strip())
    return item

  def PriceExtractor(self, item, selector):
    prod_price = selector.xpath('//div[@class="product-panel four columns"]//h4//span/text()').extract()
    for price in prod_price:
      if re.search(r"(\$\d*\.\d\d)", price):
        item['list_price'] = re.search(r"(\$\d*\.\d\d)", price).group(1)
      if re.search(r"Reg. (\$\d*\.\d\d)", price):
        item['list_price'] = re.search(r"Reg. (\$\d*\.\d\d)", price).group(1)
      elif re.search(r"Sale (\$\d*\.\d\d)", price):
        item['sale_price'] = re.search(r"Sale (\$\d*\.\d\d)", price).group(1)
      elif re.search(r"(\$\d*\.\d\d)", price):
        item['list_price'] = re.search(r"(\$\d*\.\d\d)", price).group(1)

  def ProductNumExtract(self, item, response_url):
    if re.search(r"(/\d+/)", response_url):
      item['product_item_num'] = re.search(r"/(\d+)/", response_url).group(1)