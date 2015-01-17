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

class ModdealsTagsSpider(CrawlSpider):
  name = "moddealsTags"
  allowed_domains = ['moddeals.com']
  start_urls = [
    'http://www.moddeals.com/list/womens-cheap-tops',
    'http://www.moddeals.com/list/womens-cheap-dresses',
    'http://www.moddeals.com/list/womens-bottoms',
    'http://www.moddeals.com/list/womens-activewear',
    'http://www.moddeals.com/list/womens-coats-jackets',
    'http://www.moddeals.com/list/basics',
    'http://www.moddeals.com/list/cheap-swimwear-women',
    'http://www.moddeals.com/list/workwear',
    'http://www.moddeals.com/list/cheap-intimate-apparel',
    'http://www.moddeals.com/list/trends',
    
    
    'http://www.moddeals.com/list/cheap-shoes-womens-flats',
    'http://www.moddeals.com/list/womens-cheap-sandals',
    'http://www.moddeals.com/list/cheap-wedges-shoes',
    'http://www.moddeals.com/list/womens-cheap-sneakers',
    'http://www.moddeals.com/list/womens-shoes-cheap-heels-pumps',
    'http://www.moddeals.com/list/womens-cheap-boots',
    'http://www.moddeals.com/list/cheap-athletic-shoes-for-women',
    
    
    'http://www.moddeals.com/list/cheap-womens-sunglasses',
    'http://www.moddeals.com/list/womens-scarves',
    'http://www.moddeals.com/list/cheap-womens-watches',
    'http://www.moddeals.com/list/belts',
    'http://www.moddeals.com/list/womens-hair-accessories',
    'http://www.moddeals.com/list/hats',
    
    
    'http://www.moddeals.com/list/cheap-womens-jewelry',
    'http://www.moddeals.com/list/cheap-premium-jewelry',
    'http://www.moddeals.com/list/womens-rings',
    'http://www.moddeals.com/list/womens-earrings',
    'http://www.moddeals.com/list/womens-necklaces',
    'http://www.moddeals.com/list/womens-bracelets',
    
    'http://www.moddeals.com/list/cheap-womens-handbags',
    'http://www.moddeals.com/list/womens-clutches',
    'http://www.moddeals.com/list/womens-wallets'
      
    
  ]
  
  rules = (
  Rule(SgmlLinkExtractor(restrict_xpaths='//ul[@class="product_filter_scroll"]//li[@class="sub_categories"]')),
  Rule(SgmlLinkExtractor(restrict_xpaths='//div[@class="paging paging-product-list-1"]//a'),callback='parse_item',follow=True),
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
 
    
    productIDs = hxs.xpath('//li[@class="quickview" ]/@pid').extract()
   
    res  = hxs.xpath('(//div[@id="breadcrumbs"]//a/text())[position()>1]').extract()
        
    list = []
    list.append('Women') 
    for index in range(len(res)):
        v = (res[index])
        v = v.strip()
        if v!='/':
          list.append(v)
    
    # moddeals is all about women      
    
            
    item['tag'] = list 
    item['tag_product_ids']  = productIDs
      
  
    return item

  def AddTags(self,item,url):  
     par = urlparse.parse_qs(urlparse.urlparse(url).query)
     
     res = par["ProductID"]
     return res[0]
 
   
 