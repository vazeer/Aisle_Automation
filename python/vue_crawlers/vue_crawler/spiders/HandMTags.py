'''
Created on July 22, 2014

@author: Vazeer
'''

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem
import urlparse
import urllib
import sys

class HandMSpiderTags(CrawlSpider):
  name = "HandMTags"
  allowed_domains = ['hm.com']
  start_urls = ['http://www.hm.com/us/department/LADIES',
  'http://www.hm.com/us/department/MEN'
  ]
  rules = (
    #Extract different categories
    Rule(SgmlLinkExtractor(restrict_xpaths=('//li[@class="folded"]'))),

    #Extract all sub categories
    Rule(SgmlLinkExtractor(restrict_xpaths=('(//ul[@class="products single"]//ul//li)[position()>1]')),callback='parse_item',follow = True),

    Rule(SgmlLinkExtractor(restrict_xpaths=('//a[@class="act leaf"] | //ul[@class="subsubtype"] | //ul[@class="pages bottom"]')),callback='parse_item'),
    #Extract all pages
  #  Rule(SgmlLinkExtractor(restrict_xpaths=('//ul[@class="pages top fixed"]'))),

      # Extract the different items on the page.
#    Rule(SgmlLinkExtractor(restrict_xpaths=('//ul[@class="pages bottom"]')),
#         callback='parse_item'),
  )



  def myParser(self,response):
      print '*********************************** URL:', response.url
      sel = Selector(response)
      res  = sel.xpath('(//ul[@class="breadcrumbs"]//li/a//text()|//ul[@class="breadcrumbs"]//li/strong//text())[position() > 1]').extract()
      print '#####################:*',res
      
  def parse_item(self, response):
   # print '*********************************** URL:', response.url
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    item['product_item_num']  = str(response.url)
    tag = sel.xpath('//meta[@name="keywords"]/@content').extract()
    print '@@@@@@@@@@@values: ',tag 
    productIDs = []
    productsurls = sel.xpath('//ul[@id="list-products"]//a/@href').extract()
    
    for producturl in productsurls:
       if producturl.strip():
         par = urlparse.parse_qs(urlparse.urlparse(producturl).query)
         try:
          temp = par['article']
         
          productIDs.append(temp[0])
         except:
          print "Unexpected error:", sys.exc_info()[0]
        

    
    print '@@@@@@@@@@@values3333: ',productIDs  
    
    
    
    res  = sel.xpath('(//ul[@class="breadcrumbs"]//li/a//text()|//ul[@class="breadcrumbs"]//li/strong//text())[position() > 1]').extract()
    print '*************',res
    list = []
    for index in range(len(res)):
        v = (res[index])
        v = v.strip()
        if v!='/':
          list.append(v)
            
    item['tag'] = list 
    item['tag_product_ids']  = productIDs
    
    return item




