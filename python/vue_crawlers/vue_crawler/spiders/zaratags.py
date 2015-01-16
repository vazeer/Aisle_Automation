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

class ZaraProductTagsSpider(CrawlSpider):
  name = "zaraProductTags"
  allowed_domains = ['zara.com']
  handle_httpstatus_list = [404]
  start_urls = [
'http://www.zara.com/in/en/sale/woman/outerwear/coats-c540002.html',
#'http://www.zara.com/in/en/sale/woman/outerwear/quilted-coat-c540003.html',
#'http://www.zara.com/in/en/sale/woman/outerwear/jackets-c698564.html',
#'http://www.zara.com/in/en/sale/woman/outerwear/trf-c540005.html',
#'http://www.zara.com/in/en/sale/woman/blazers-c436097.html',
#'http://www.zara.com/in/en/sale/woman/dresses/printed-c698571.html',
#'http://www.zara.com/in/en/sale/woman/dresses/plain-c698573.html',
#'http://www.zara.com/in/en/sale/woman/dresses/trf-c540013.html',
#'http://www.zara.com/in/en/sale/woman/jumpsuits-c437707.html',
#'http://www.zara.com/in/en/sale/woman/tops/blouses-c698578.html',
#'http://www.zara.com/in/en/sale/woman/tops/shirts-c540015.html',
#'http://www.zara.com/in/en/sale/woman/tops/trf-c540016.html',
#'http://www.zara.com/in/en/sale/woman/jeans-c436109.html',
#'http://www.zara.com/in/en/sale/woman/trousers/skinny-c540018.html',
#'http://www.zara.com/in/en/sale/woman/trousers/pleats-c540019.html',
#'http://www.zara.com/in/en/sale/woman/trousers/flowing-c642008.html',
#'http://www.zara.com/in/en/sale/woman/trousers/joggers-c698579.html',
#'http://www.zara.com/in/en/sale/woman/trousers/shorts-c540021.html',
#'http://www.zara.com/in/en/sale/woman/trousers/trf-c540022.html',
#'http://www.zara.com/in/en/sale/woman/skirts/mini-c540027.html',
#'http://www.zara.com/in/en/sale/woman/skirts/midi-c540028.html',
#'http://www.zara.com/in/en/sale/woman/skirts/trf-c540030.html',
#'http://www.zara.com/in/en/sale/woman/knitwear/sweaters-c540033.html',
#'http://www.zara.com/in/en/sale/woman/knitwear/cardigans-c540032.html',
#'http://www.zara.com/in/en/sale/woman/knitwear/turtleneck-c698585.html',
#'http://www.zara.com/in/en/sale/woman/t-shirts/long-sleeve-c698588.html',
#'http://www.zara.com/in/en/sale/woman/t-shirts/short-sleeve-c698587.html',
#'http://www.zara.com/in/en/sale/woman/t-shirts/trf-c540037.html',
#'http://www.zara.com/in/en/sale/woman/studio-c540058.html',
#'http://www.zara.com/in/en/sale/woman/shoes/boots-c540038.html',
#'http://www.zara.com/in/en/sale/woman/shoes/ankle-boots-c540047.html',
#'http://www.zara.com/in/en/sale/woman/shoes/high-heels-c540044.html',
#'http://www.zara.com/in/en/sale/woman/shoes/flats-c540045.html',
#'http://www.zara.com/in/en/sale/woman/shoes/heeled-sandals-c540042.html',
#'http://www.zara.com/in/en/sale/woman/handbags/hand-bags-c540053.html',
#'http://www.zara.com/in/en/sale/woman/handbags/messenger-bags-c540054.html',
#'http://www.zara.com/in/en/sale/woman/handbags/large-handbags-c540055.html',
#'http://www.zara.com/in/en/sale/woman/accessories/scarves-c436073.html',
#'http://www.zara.com/in/en/sale/woman/accessories/accessories-c436069.html',
#'http://www.zara.com/in/en/sale/woman/accessories/jewellery-c540048.html',
 
                   ]
  rules = (
   
  Rule(SgmlLinkExtractor(restrict_xpaths='//li[@class="current selected"]'),callback='myParserTest'),
   
  )
  
  
  def myParserTest(self,response):
      print '*********************************** URL:', response.url
           
      sel = Selector(response)
      res  = sel.xpath('(//ul[@class="breadcrumbs"]//li/a//text()|  //ul[@class="breadcrumbs"]//li[@class="selected last"]//text() )[position() > 1]').extract()
      str1 = ','.join(res)
      with open('/home/vazeer/Desktop/nordstromtest.txt', "a") as myfile:
        myfile.write('URL: '+response.url+ '    TAGS:'+str1+' \n')

      
  def parse_item(self, response):
    print '************* URL:', response.url
    #sel = Selector(response)
    hxs = HtmlXPathSelector(response)
    
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
 

    item['product_item_num']  = str(response.url)
    tag = hxs.xpath('//meta[@name="keywords"]/@content').extract()
   # print '@@@@@@@@@@@values: ',tag 
    productIDs = []
    productsuidlist = hxs.xpath('//ul[@id="product-list"]//li//a/@data-item').extract()
    for productid in productsuidlist:
       if productid.strip():
         productIDs.append(productid)

    res  = hxs.xpath('//div[@class="breadcrumbs"]//li//span[@itemprop="title"]').extract()
    
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
     url=urllib.unquote(url).decode('utf8') 
     Segments = url.split('/')
     val = Segments[len(Segments)-1]
     res = val.split('?')
     return res[0]
    
 
   
 