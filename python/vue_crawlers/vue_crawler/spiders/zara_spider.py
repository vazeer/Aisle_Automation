'''
Created on Jun 13, 2014

@author: Behrooz
'''

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem


class ZaraSpider(CrawlSpider):
  name = "zara"
  allowed_domains = ['zara.com']
  start_urls = ['http://www.zara.com/in/en/sale/woman-c434501.html']
  rules = (
      # Extract the different items on the page.
    Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@id="container-nav"]'
                                             '//div[@class="fixed"]'))),
    Rule(SgmlLinkExtractor(
      restrict_xpaths=('//section[@class="category-content"]')),
      callback='parse_item'),
    # Extract the different pages on the main site side menu.

  )
  def parse_item(self, response):
    print response.url
    sel = Selector(response)

    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
    #TODO(behrooz): add logic later that parses more than one item
    item_num_str = sel.xpath('//input[@id="f_itemId"]/@value').extract()[0]
    item_num = re.findall(r'\d+', item_num_str)[0]
    item['source_site'] = "zara.com"
    item['product_title'] = str(sel.xpath('//h1/text()').extract()[0])
    item['product_item_num'] = item_num
    item['product_url'] = response.url
    item['description'] = sel.xpath('//div[@class="hidden-content"]/text()').extract()
    item['image_urls'] = [sel.xpath('//img[@class="image-big gaViewEvent gaColorInfo sbdraggable draggableMain"]/@src').extract()[0]]
    return item

  def PriceExtractor(self, item, selector):
    price = selector.xpath('//p[@class="price"]/text()').extract()
    item['list_price'] = price[0]

