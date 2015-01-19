'''
Created on Jun 13, 2014

@author: Behrooz
'''

import re
import nltk
from nltk.collocations import *
from nltk.stem import *



from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem
import urlparse
import urllib
from scrapy.selector import Selector

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors import LinkExtractor

class BlueflyTagsSpider(CrawlSpider):
  name = "blueflyTags"
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
  Rule(SgmlLinkExtractor(restrict_xpaths='//div[@class="pageNavigation"][1]'),callback='parse_item',follow=True),
  )
  
  def myParserTest(self,response):
      print '**************test********************* URL:', response.url
           
    
        
  def parse_item(self, response):
 #   print '************* URL:', response.url
    #sel = Selector(response)
    hxs = Selector(response)
    
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
  
    item['product_item_num']  = str(response.url)
 
    
    productIDs = hxs.xpath('//div[@class="productContainer"]/@id').extract()
   
    res  = hxs.xpath('(//div[@class="breadCrumbNav"]//a/text())[position()>1]').extract()
    
    
    list = []
  
    for index in range(len(res)):
        v = (res[index])
        v = v.strip()
        if v!='/':
          list.append(v)
     
            
    item['tag'] = list 
    item['tag_product_ids']  = productIDs
      
  
    return item

  def AddTags(self,item,url):  
     par = urlparse.parse_qs(urlparse.urlparse(url).query)
     
     res = par["ProductID"]
     return res[0]
 
   
 