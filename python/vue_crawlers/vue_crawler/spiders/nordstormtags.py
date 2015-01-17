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


class NordStormProductTagsSpider(CrawlSpider):
  name = "nordstormProductTags"
  allowed_domains = ['shop.nordstrom.com']
  #start_urls = [
  #
  # 'http://shop.nordstrom.com/c/womens-clothing?origin=leftnav',
  #              'http://shop.nordstrom.com/c/womens-shoes',
  #              'http://shop.nordstrom.com/c/womens-handbags'
  #                 ]
  #rules = (
  #
  #  Rule(SgmlLinkExtractor(restrict_xpaths='((//h3[@class="nav-entry-clothing"])[1])//following::ul[1]//li[following-sibling::li[@class="spacer-hack"]]|//ul[@class="nav-group"][position()>1]|((//h3[@class="nav-entry-shoes"])[position()>1])//following::ul[1]//li[following-sibling::li[@class="spacer-hack"]]')),
  #  Rule(SgmlLinkExtractor(restrict_xpaths='//div[@id="leftnav"]//a'),callback='parse_item'),
  #  
  #  Rule(SgmlLinkExtractor(restrict_xpaths='(//ul[@class="numbers"])[1]//li'),callback='parse_item',follow=True),
  # 
  #
  #)
  
  
  
  start_urls = ['http://shop.nordstrom.com/c/womens-party-dresses?origin=leftnav']
  rules = (

    Rule(SgmlLinkExtractor(restrict_xpaths='//div[@class="filter category" or @class="filter standard size" or @class="filter standard color small" or @class="filter standard"]//li')),
    Rule(SgmlLinkExtractor(restrict_xpaths='(//li[@class="next"])[1]'),callback='parse_item',follow=True),
  
  )
  
  
  
  
  
  
  
  
  
  def myParserTest(self,response):
    print '*********************************** URL:', response.url
    hxs = Selector(response)
    mytags = hxs.xpath('//div[@class="container"]//ul//li[@class="selected"]//text()').extract()     
    print '*********************************** TAG:', mytags

      
  def parse_item(self, response):
 #   print '************* URL:', response.url
    #sel = Selector(response)
    hxs = Selector(response)
    
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
  
    item['product_item_num']  = str(response.url)
    tag = hxs.xpath('//meta[@name="keywords"]/@content').extract()
   # print '@@@@@@@@@@@values: ',tag 
    productIDs = []
    productsurls = hxs.xpath('//a[@class="title"]/@href').extract()
    for producturl in productsurls:
       if producturl.strip():
         par = urlparse.parse_qs(urlparse.urlparse(producturl).query)
         temp = self.AddTags(item,producturl)
        # print '&&&&&&&&&&',temp
         productIDs.append(temp)

   
    
    mytags = hxs.xpath('//div[@class="container"]//ul//li[@class="selected"]//text()').extract()
    
    res  = hxs.xpath('(//ul[@class="breadcrumbs"]//li/a//text()|  //ul[@class="breadcrumbs"]//li[@class="selected last"]//text() )[position() > 1]').extract()
    
    list = []
    for index in range(len(res)):
        v = (res[index])
        v = v.strip()
        if v!='/':
          list.append(v)
          
    
    
    for index in range(len(mytags)):
      v = (mytags[index])
      v = v.strip()
      if v!='/':
        list.append(v)
    
            
    item['tag'] = list 
    item['tag_product_ids']  = productIDs
      
  
    return item

  def AddTags(self,item,url):  
     par = urlparse.parse_qs(urlparse.urlparse(url).query)
     url=urllib.unquote(url).decode('utf8') 
     Segments = url.split('/')
     val = Segments[len(Segments)-1]
     res = val.split('?')
     return res[0]
    
 
   
 