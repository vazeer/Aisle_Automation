'''
Created on Aug 13, 2014

@author: Vazeer
'''

import re
import urlparse

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor


from vue_crawler.items import VueCrawlerItem



class TalbotsSpider(CrawlSpider):
  name = "talbots"
  allowed_domains = ['talbots.com']
  start_urls = ['http://www.talbots.com/online/browse/new-arrivals/_/N-10588',
                'http://www.talbots.com/online/browse/womens/_/N-4294966578',
                'http://www.talbots.com/online/browse/petites/_/N-4294966556',
                'http://www.talbots.com/online/browse/plus-size/_/N-4294966550',
                'http://www.talbots.com/online/browse/plus-size-petites/_/N-4294966545'
                ]
  rules = (
      # Extract the different pages on the main site.
  #  Rule(SgmlLinkExtractor(restrict_xpaths='//div[@id="catalogFilter"]')),

  #  Rule(SgmlLinkExtractor(restrict_xpaths='//div[@id="productGallery"]'), callback='parse_item')
  
  Rule(SgmlLinkExtractor(restrict_xpaths='//li[@class="nav-item"]')),
  
  Rule(SgmlLinkExtractor(restrict_xpaths='//li[@class="nav-item"]')),
  
 # Rule(SgmlLinkExtractor(restrict_xpaths='//ul')),
  
  Rule(SgmlLinkExtractor(restrict_xpaths='//h4//a'), callback='parse_item')
  
  )
 
  def parse_item(self, response):
   # print '************* URL:', response.url
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
  #  item_num_str = sel.xpath('//select/@productId').extract()[0]
   # item_num = re.findall(r'\d+', item_num_str)[0]
    item['source_site'] = "talbots.com"
   # tempnum = str(sel.xpath('//h1[@class="fn"]/test').extract())

    item['product_title'] = str(sel.xpath('//h1[@class="fn"]/text()').extract()[0])
    item['product_item_num'] = ''

    url = urlparse.urlparse(response.url)
    query = urlparse.parse_qs(url.query)

    item['product_item_num'] = [v for k, v in query.iteritems() if k == 'id'][0][0]

    item['product_url'] = response.url
    item['description'] = sel.xpath('//div[@id="bottomArea"]'
                                    '//div[@id="longDescription"]/text()').extract()
    item['image_urls'] = ['http:'+sel.xpath('//a[@class="MagicZoom"]/@href').extract()[0]]
    bullet_description = sel.xpath('//div[@class="prodLongDesc"]//li/text()').extract()
    for desc_bullet in bullet_description:
      if desc_bullet.strip():
        item['description'].append(desc_bullet.strip())

    colors = sel.xpath('(//div[@class="productColors"])[1]//li/@title').extract()
    item['product_colors'] = colors


    sizes = sel.xpath('(//div[@class="productSizes"])[1]//input/@value').extract()
    item['product_sizes'] = sizes




    return item

  def PriceExtractor(self, item, selector):
    prod_price = selector.xpath('//div[@class="price"]//strong/text()').extract()
    for price in prod_price:
      if re.search(r"Was (\$\d*\.\d\d)", price):
        item['list_price'] = re.search(r"Was (\$\d*\.\d\d)", price).group(1)
      if re.search(r"Reg. (\$\d*\.\d\d)", price):
        item['list_price'] = re.search(r"Reg. (\$\d*\.\d\d)", price).group(1)
      elif re.search(r"Sale (\$\d*\.\d\d)", price):
        item['sale_price'] = re.search(r"Sale (\$\d*\.\d\d)", price).group(1)
      elif re.search(r"(\$\d*\.\d\d)", price):
        item['list_price'] = re.search(r"(\$\d*\.\d\d)", price).group(1)
