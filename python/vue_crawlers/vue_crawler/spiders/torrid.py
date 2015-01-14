'''
Created on Aug 21, 2014

@author: Vazeer

'''

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem


class TorridSpider(CrawlSpider):
  name = "torrid"
  allowed_domains = ['www.torrid.com']
  start_urls = [                'http://www.torrid.com/torrid/Dresses.jsp'           ]
  rules = (
    # Extract the different pages on the main site.
    Rule(SgmlLinkExtractor(restrict_xpaths=('//ul[@class="lvl-2"]'))),
      # Extract the different items on the page.
    Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@role="main"]''//div[@class="fashion-item"]')),
         callback='parse_item'),
  )

  def parse_item(self, response):
#     print response.url
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
    item_num_str = sel.xpath('//div[@class="item-number-wrapper"]/text()').extract()[0]
    item_num = re.findall(r'\d+', item_num_str)[0]
    item['source_site'] = "shop.nordstrom.com"
    item['product_title'] = str(sel.xpath('//section[@id="product-title"]//h1/text()').extract()[0])
    item['product_item_num'] = item_num
    item['product_url'] = response.url
    item['description'] = sel.xpath('//section[@id="details-and-care"]//ul[@class="style-features"]//li/text()').extract()
    item['image_urls'] = [sel.xpath('//div[@id="product-image"]//img/@src').extract()[0]]
    return item

  def PriceExtractor(self, item, selector):
    price = selector.xpath('//section[@id="price"]//td[@class="item-price heading-2"]//span/text()').extract()
    if not price:
      sale_text = selector.xpath('//section[@id="price"]//span[@class="sale-price"]/text()').extract()[0]
      item['sale_price'] = re.search(r"Now: (\$\d*\.\d\d)", sale_text).group(1)
      list_text = selector.xpath('//section[@id="price"]//span[@class="regular-price"]/text()').extract()[0]
      item['list_price'] = re.search(r"Was: (\$\d*\.\d\d)", list_text).group(1)
    else:
      item['list_price'] = price[0]
