'''
Created on July 26, 2014

@author: Vazeer
'''

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem


class ZulilySpider(CrawlSpider):
  name = "zulily"
  allowed_domains = ['zulily.com']
  start_urls = ['http://www.zulily.com/new-today/?ref=header&ns=ns_509630173|1410423082106',
 
  'http://www.zulily.com/last-day/?ref=header&ns=ns_509630173|1410423115917',
 
  ]
  
  
  rules = (
    # Extract the different pages on the main site.
   # Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="wrapper"]|//div[@class="expandable-content"]'))),
    
    Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@data-im="CategoryHomepageImage"]//a'))),
    
      # Extract the different items on the page.
    Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="product-name"]')),
         callback='parse_item'),
  )

  def parse_item(self, response):
#     print response.url
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
    item_num_str = sel.xpath('//a[@data-email-modal="modal_plaintext"]/@product_id').extract()[0]
    item_num = re.findall(r'\d+', item_num_str)[0]
    item['source_site'] = "zulily.com"
    item['product_title'] = str(sel.xpath('//h1[@itemprop="Name"]/text()').extract()[0])
    item['product_item_num'] = item_num
    item['product_url'] = response.url
    item['description'] = sel.xpath('//div[@class="description"]//text()').extract()
    item['image_urls'] = [sel.xpath('//img[@class="photo"]/@src').extract()[0]]
    # it need to work
    #item['image_urls'] = [sel.xpath('//a[@class="MagicThumb-swap tag"]/@rev,(//div[@id="product-image"]//img)[2]/@src').extract()[0]]
    return item

  def PriceExtractor(self, item, selector):
    price = selector.xpath('//div[@id="prduct-price"]/span[@class="price"]/text()').extract()
    item['list_price'] = price
      

