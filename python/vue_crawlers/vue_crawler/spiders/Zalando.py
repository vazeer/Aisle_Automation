'''
Created on July 22, 2014

@author: Vazeer
'''

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem


class ZalandoSpider(CrawlSpider):
  name = "zalando"
  allowed_domains = ['zalando.co.uk']
  start_urls = ['http://www.zalando.co.uk/womens-clothing/']
  rules = (

   #Extract all pages
    Rule(SgmlLinkExtractor(restrict_xpaths=('//li[@class="parentCat"]'))),

    #Extract all pages
    Rule(SgmlLinkExtractor(restrict_xpaths=('//li[@class="siblingCat"]'))),

      # Extract the different items on the page.
    Rule(SgmlLinkExtractor(restrict_xpaths=('//li[@class="gItem"]')),
         callback='parse_item'),
  )

  def parse_item(self, response):
#     print response.url
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
    item_num_str = sel.xpath('//span[@itemprop="identifier"]/text()').extract()[0]
    item_num = re.findall(r'\d+', item_num_str)[0]
    item['source_site'] = "zalando.co.uk"
    item['product_title'] = str(sel.xpath('//span[@itemprop="name"]/text()').extract()[0])
    item['product_item_num'] = item_num
    item['product_url'] = response.url
    item['description'] = sel.xpath('//div[@class="content"]//text()').extract()
    item['image_urls'] = [sel.xpath('//ul[@id="moreImagesList"]//a/@href').extract()]
    bullet_description = sel.xpath('//div[@id="productDetails"]/text()').extract()
    for desc_bullet in bullet_description:
      if desc_bullet.strip():
        item['description'].append(desc_bullet.strip())

    return item

  def PriceExtractor(self, item, selector):
    price = selector.xpath('//span[@itemprop="price"]/text()').extract()
    item['list_price'] = price[0]
