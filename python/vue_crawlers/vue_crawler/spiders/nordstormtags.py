'''
Created on Jun 13, 2014

@author: Behrooz
'''
from __future__ import print_function
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
  start_urls = [
 
   'http://shop.nordstrom.com/c/womens-clothing?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-shoes',
                'http://shop.nordstrom.com/c/womens-handbags'
                   ]
  rules = (
      # Extract the different items on the page.
#    Rule(SgmlLinkExtractor(
#      restrict_xpaths=('//div[@id="macysGlobalLayout"]'
#                       '//div[@class="shortDescription"]')),
#      callback='parse_item'),
#    # Extract the different pages on the main site side menu.
#    Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@id="localNavigationContainer"]'))),
#    # Extract page number links
#    Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@id="paginateTop"]'))),

 # Extract the different pages on the main site.
   
    
    Rule(SgmlLinkExtractor(restrict_xpaths='((//h3[@class="nav-entry-clothing"])[1])//following::ul[1]//li[following-sibling::li[@class="spacer-hack"]]|//ul[@class="nav-group"][position()>1]|((//h3[@class="nav-entry-shoes"])[position()>1])//following::ul[1]//li[following-sibling::li[@class="spacer-hack"]]')),
    Rule(SgmlLinkExtractor(restrict_xpaths='//div[@id="leftnav"]//a'),callback='parse_item'),
    
    Rule(SgmlLinkExtractor(restrict_xpaths='(//ul[@class="numbers"])[1]//li'),callback='parse_item',follow=True),
    
    
   # Rule(SgmlLinkExtractor(restrict_xpaths='(//li[@class="side-subnav"]/ul)[position()>1]'),callback='myParser'),
    
    
#    Rule(SgmlLinkExtractor(restrict_xpaths='((//h2[@id="SWIM_STYLE"]|//h2[@id="SKIRT_STYLE"]|//h2[@id="DRESS_STYLE"]|'
#                                            '//h2[@id="DENIM_FIT"]|//h2[@id="PANT_STYLE"]|//h2[@id="TOP_STYLE"]|//h2[@id="SUIT_STYLE"]|'
#                                            '//h2[@id="PRODUCT_DEPARTMENT"]|//h2[@id="SHIRT_FIT"]|//h2[@id="T_SHIRT_STYLE"]|//h2[@id="BOOT_HEIGHT"]|'
#                                            '//h2[@id="SHOE_TYPE"]|//h2[@id="FLAT_TYPE"]|//h2[@id="SANDAL_TYPE"])//following::ul[@class="defaultFacet"])[1]'),callback='parse_item')
#                                            
#                                            
#                                            
                                            
    #Rule(SgmlLinkExtractor(restrict_xpaths='(((//h2[@id="DRESS_LENGTH"]|//h2[@id="SKIRT_STYLE"])//following::ul[@class="defaultFacet"]))'),callback='parse_item')                                        
                                           
                                            
    # Extract the different items on the pag  
  #  Rule(SgmlLinkExtractor(restrict_xpaths='//div[@id="paginateBottom"]'), callback='parse_item')
  )
  
  def myParserTest(self,response):
     # print '*********************************** URL:', response.url
           
      sel = Selector(response)
      res  = sel.xpath('(//ul[@class="breadcrumbs"]//li/a//text()|  //ul[@class="breadcrumbs"]//li[@class="selected last"]//text() )[position() > 1]').extract()
      str1 = ','.join(res)
      with open('/home/vazeer/Desktop/nordstromtest.txt', "a") as myfile:
        myfile.write('URL: '+response.url+ '    TAGS:'+str1+' \n')

      
  def parse_item(self, response):
 #   print '************* URL:', response.url
    #sel = Selector(response)
    hxs = HtmlXPathSelector(response)
    
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

    
    tmp = self.AddTags(item,str(response.url))
    
    tagtemp = tmp.replace("-", " ");
    
    
    res  = hxs.xpath('(//ul[@class="breadcrumbs"]//li/a//text()|  //ul[@class="breadcrumbs"]//li[@class="selected last"]//text() )[position() > 1]').extract()
    
    list = []
    for index in range(len(res)):
        v = (res[index])
        v = v.strip()
        if v!='/':
          list.append(v)
          
    list.append(tagtemp)     
            
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
    
 
   
 