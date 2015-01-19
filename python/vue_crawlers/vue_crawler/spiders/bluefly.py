'''
Created on Aug 2, 2014

@author: Vazeer
'''

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem


class BlueflySpider(CrawlSpider):
  name = "bluefly"
  #allowed_domains = ['bluefly.com']
  #start_urls = ['http://www.bluefly.com/a/women-clothing']
  #rules = (
  #  # Extract the different pages on the main site.
  #  Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="dept-nav-section"]//ul//li'))),
  #  
  #  Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="pageNavigation"]'))),
  #    # Extract the different items on the page.
  #  Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="productShortName"]//a')),
  #       callback='parse_item'),
  #)
  
  allowed_domains = ['bluefly.com']
  start_urls = [
   
    'http://www.bluefly.com/womens/designer-activewear',
    'http://www.bluefly.com/womens/designer-blazers-jackets-vests',
    'http://www.bluefly.com/womens/designer-blouses',
    'http://www.bluefly.com/womens/designer-cashmere',
    'http://www.bluefly.com/womens/designer-coats-outerwear',
    'http://www.bluefly.com/womens/designer-denim-shop',
    'http://www.bluefly.com/womens/designer-dresses',
    'http://www.bluefly.com/womens/designer-intimates-sleepwear',
    'http://www.bluefly.com/womens/designer-pants-leggings-jumpsuits',
    'http://www.bluefly.com/womens/designer-shorts-rompers',
    'http://www.bluefly.com/womens/designer-skirts',
    'http://www.bluefly.com/womens/designer-sweaters',
    'http://www.bluefly.com/womens/designer-swimwear',
    'http://www.bluefly.com/womens/designer-tops-tees',
    
     'http://www.bluefly.com/shoes/designer-boots',
     'http://www.bluefly.com/shoes/designer-loafers-and-flats',
     'http://www.bluefly.com/shoes/designer-pumps-high-heels',
     'http://www.bluefly.com/shoes/designer-sandals',
     'http://www.bluefly.com/shoes/designer-sneakers',
     'http://www.bluefly.com/shoes/designer-wedges-espadrilles'

  ]
 
  rules = (
  Rule(SgmlLinkExtractor(restrict_xpaths='//div[@class="listNav"]')),
  Rule(SgmlLinkExtractor(restrict_xpaths='//div[@class="pageNavigation"][1]'),follow=True),
  Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="productShortName"]//a')),callback='parse_item'),
  )

  def parse_item(self, response):
#     print response.url
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
    item_num_str = sel.xpath('//input[@name="/atg/userprofiling/B2CProfileFormHandler.productId"]/@value').extract()[0]
    item_num = re.findall(r'\d+', item_num_str)[0]
    item['source_site'] = "bluefly.com"
    item['product_title'] = str((sel.xpath('//span[@class="pdpBreadCrumb product"]/text()').extract()[0]).strip())
    item['product_item_num'] = item_num
    item['product_url'] = response.url
    bullet_description = sel.xpath('//span[@class="pdpBulletContainer"]//span//text()').extract()
    listoflines = sel.xpath('(//div[@class="pdpProductInformationText"]//p/text())[1]').extract()
    item['description'] =[]
    for desc_bullet in listoflines:
      if desc_bullet.strip():
        item['description'].append(str(desc_bullet.strip()))
    
    for desc_bullet in bullet_description:
      if desc_bullet.strip():
        item['description'].append(str(desc_bullet.strip()))
      
    item['image_urls'] = [sel.xpath('//img[@class="current-product-image"]/@src').extract()[0]]
    
    
    res  = sel.xpath('(//div[@class="pdpBreadCrumbsContainer"]//a/text())[position()>1]').extract()
    list = [];
    for index in range(len(res)):
        v = str(res[index])
        v = v.strip()
        if  v!='/':
            list.append(v)
    item['product_tags'] = list
    
    
    sizes = sel.xpath('//div[@class="pdpSizeListContainer"]//span/text()').extract()
    
    sizesstripped = [];
    for index in range(len(sizes)):
        v = str(sizes[index])
        v = v.strip()
        if  v!='':
          sizesstripped.append(v)
          
    item['product_sizes'] = sizesstripped
    item['product_colors'] = sel.xpath('//div[@class="pdp-label product-variation-label"]//em/text()').extract()
    
    
    return item

  def PriceExtractor(self, item, selector):
    price = selector.xpath('//input[@name="rangeFinalPrice"]/@value').extract()
    item['list_price'] = price[0]
