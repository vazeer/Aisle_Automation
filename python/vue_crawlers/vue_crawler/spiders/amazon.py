'''
Created on Jun 13, 2014

@author: Behrooz
'''

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem


class AmazonSpider(CrawlSpider):
  name = "amazon"
  allowed_domains = ['amazon.com']
  start_urls = ['http://www.amazon.com/Women-Clothing/b/ref=sv_sl_fl_1040660_1?ie=UTF8&node=1040660']
  rules = (
      # Extract the different items on the page.
    Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="categoryRefinementsSection"]'))),
    Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="fg-widget"]'))),
    Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@id="mainResults"]')), callback='parse_item'),
  )

  def parse_item(self, response):
    print '************* URL:', response.url
    sel = Selector(response)
    item = VueCrawlerItem()
    item['source_site'] = "amazon.com"
    item['product_title'] = str(sel.xpath('//span[@id="productTitle"]/text()').extract()[0])
    item['product_item_num'] = 0
    item['product_url'] = response.url
    item['description'] = sel.xpath('//div[@id="featured-bullets"]'
                                    '//span[@class="a-list-item"]/text()').extract()
    return item

  def PriceExtractor(self, item, selector):
    #for now skip because we need to use something that renders javascript.
    pass
