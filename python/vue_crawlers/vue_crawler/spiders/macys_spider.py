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
  name = "macys"
  allowed_domains = ['macys.com']
  start_urls = ['http://www1.macys.com/shop/womens-clothing?id=118&edge=hybrid']
  rules = (
      # Extract the different items on the page.
    Rule(SgmlLinkExtractor(
      restrict_xpaths=('//div[@id="macysGlobalLayout"]'
                       '//div[@class="shortDescription"]')),
      callback='parse_item'),
    # Extract the different pages on the main site side menu.
    Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@id="localNavigationContainer"]'))),
    # Extract page number links
    Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@id="paginateTop"]'))),
  )

  def parse_item(self, response):
#     print '************* URL:', response.url
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
    #TODO(behrooz): add logic later that parses more than one item
    rating =  sel.xpath('//div[@class="BVRRRatingNormalImage"]//img/@alt').extract()
    if rating:
      item['rating'] = rating[0]
    item_num_str = sel.xpath('//div[@id="productDescription"]'
                             '//div[@class="productID"]/text()').extract()[0]
    item_num = re.findall(r'\d+', item_num_str)[0]
    item['source_site'] = "macys.com"
    item['product_title'] = str(sel.xpath('//div[@id="productDescription"]'
                                          '//h1[@id="productTitle"]'
                                          '/text()').extract()[0])
    item['product_item_num'] = item_num
    item['product_url'] = response.url
    item['description'] = sel.xpath('//div[@id="bottomArea"]'
                                    '//div[@id="longDescription"]/text()').extract()
    item['image_urls'] = [sel.xpath('//img[@id="mainImage"]/@src').extract()[0]]
    bullet_description = sel.xpath('//div[@id="memberProductDetails"]//li/text()').extract()
    for desc_bullet in bullet_description:
      if desc_bullet.strip():
        item['description'].append(desc_bullet.strip())
    return item

  def PriceExtractor(self, item, selector):
    prod_price = selector.xpath('//div[@class="standardProdPricingGroup"]//span/text()').extract()
    for price in prod_price:
      if re.search(r"Was (\$\d*\.\d\d)", price):
        item['list_price'] = re.search(r"Was (\$\d*\.\d\d)", price).group(1)
      if re.search(r"Reg. (\$\d*\.\d\d)", price):
        item['list_price'] = re.search(r"Reg. (\$\d*\.\d\d)", price).group(1)
      elif re.search(r"Sale (\$\d*\.\d\d)", price):
        item['sale_price'] = re.search(r"Sale (\$\d*\.\d\d)", price).group(1)
      elif re.search(r"(\$\d*\.\d\d)", price):
        item['list_price'] = re.search(r"(\$\d*\.\d\d)", price).group(1)
