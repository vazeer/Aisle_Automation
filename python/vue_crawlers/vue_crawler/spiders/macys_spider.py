'''
Created on Jun 13, 2014

@author: Behrooz
'''

import re
import nltk
from nltk.collocations import *
from nltk.stem import *


from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem
import urlparse

class MacysSpider(CrawlSpider):
  name = "macys"
  allowed_domains = ['macys.com']
  start_urls = ['http://www1.macys.com/shop/womens-clothing?id=118&edge=hybrid&cm_sp=intl_hdr-_-women-_-118_women&intnl=true'
 # ,'http://www1.macys.com/shop/mens-clothing?id=1&edge=hybrid&cm_sp=intl_hdr-_-men-_-1_men&intnl=true'
  #,'http://www1.macys.com/shop/shoes?id=13247&edge=hybrid&cm_sp=intl_hdr-_-shoes-_-13247_shoes&intnl=true'
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
    Rule(SgmlLinkExtractor(restrict_xpaths='(//ul[@class="nav_cat_sub_3"])[1]')),
#    
#    Rule(SgmlLinkExtractor(restrict_xpaths='((//h2[@id="SWIM_STYLE"]|//h2[@id="SKIRT_STYLE"]|//h2[@id="DRESS_STYLE"]|'
#                                            '//h2[@id="DENIM_FIT"]|//h2[@id="PANT_STYLE"]|//h2[@id="TOP_STYLE"]|//h2[@id="SUIT_STYLE"]|'
#                                            '//h2[@id="PRODUCT_DEPARTMENT"]|//h2[@id="SHIRT_FIT"]|//h2[@id="T_SHIRT_STYLE"]|//h2[@id="BOOT_HEIGHT"]|'
#                                            '//h2[@id="SHOE_TYPE"]|//h2[@id="FLAT_TYPE"]|//h2[@id="SANDAL_TYPE"])//following::ul[@class="defaultFacet"])[1]')),
#    
    
    Rule(SgmlLinkExtractor(restrict_xpaths='(((//h2[@id="DRESS_LENGTH"]|//h2[@id="SKIRT_STYLE"])//following::ul[@class="defaultFacet"])|(//div[@class="brand-options"]//div[@class="hidden"]))')),
    
    
    
    
    
    # Extract the different items on the pag  
 
    Rule(SgmlLinkExtractor(restrict_xpaths='//div[@class="shortDescription"]'), callback='parse_item')
  )

  def parse_item(self, response):
#     print '************* URL:', response.url
    sel = Selector(response)
    stemmer = PorterStemmer()
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
    self.AddTags(item,response.url)
    #TODO(behrooz): add logic later that parses more than one item
    rating =  sel.xpath('//div[@class="BVRRRatingNormalImage"]//img/@alt').extract()
    if rating:
      item['rating'] = rating[0]
    item_num_str = sel.xpath('//div[@id="productDescription"]'
                             '//div[@class="productID"]/text()').extract()[0]
    item_num = re.findall(r'\d+', item_num_str)[0]
    item['source_site'] = "macys.com"
    item['product_title'] = str(sel.xpath('//div[@id="productDescription"]'
                                          '//h1[@id="productTitle"]'
                                          '/text()').extract()[0])
    item['product_item_num'] = item_num
    item['product_url'] = response.url
    item['description'] = sel.xpath('//div[@id="bottomArea"]'
                                    '//div[@id="longDescription"]/text()').extract()
    item['image_urls'] = [sel.xpath('//img[@id="mainImage"]/@src').extract()[0]]
    bullet_description = sel.xpath('//div[@id="memberProductDetails"]//li/text()').extract()
    for desc_bullet in bullet_description:
      if desc_bullet.strip():
        item['description'].append(desc_bullet.strip())
    
    item['product_tags'] = sel.xpath('//a[@class="bcElement"]//text()').extract()
   
    
   
      
#    bigram_measures = nltk.collocations.BigramAssocMeasures()
#    trigram_measures = nltk.collocations.TrigramAssocMeasures()   
#    quadgram_measures = nltk.metrics.association.QuadgramAssocMeasures()   
#   
#    
#    monograms = []   
#    bigrams = []   
#    trigrams = []   
#    quadgrams = []   
#     #nltk integration
#    for desc_bullet in bullet_description:
#      if desc_bullet.strip():
#        temp = str(desc_bullet.strip()).split(' ')
#        
#        for val in temp:
#            monograms.append(val)
#            
#        finder = BigramCollocationFinder.from_words(temp) 
#        scored = finder.score_ngrams(bigram_measures.raw_freq)
#        output = sorted(bigram for bigram, score in scored)
#        for vals in output:
#            bigrams.append(vals)
#   
#        finderTr = TrigramCollocationFinder.from_words(temp)
#        scoredTr = finderTr.score_ngrams(trigram_measures.raw_freq)
#        outputTr = sorted(bigram for bigram, score in scoredTr)  
#        for vals in outputTr:
#            trigrams.append(vals)
#            
#        finderQr = QuadgramCollocationFinder.from_words(temp)
#        scoredQr = finderQr.score_ngrams(quadgram_measures.raw_freq)
#        outputQr = sorted(bigram for bigram, score in scoredQr)
#        for vals in outputQr:
#            quadgrams.append(vals)
#    
#      
#            
#     
#    print '***** MONOGRAMS: ', monograms  
#            
#    print '***** BIGRAMS: ', bigrams    
#    
#    print '***** TRIGRAMS: ', trigrams    
#    
#    print '***** QUADGRAMS: ', quadgrams  
     
  
    return item

  def PriceExtractor(self, item, selector):
    
    prod_price = selector.xpath('//div[@class="standardProdPricingGroup"]//span/text()').extract()
    for price in prod_price:
      if re.search(r"Was (\$\d*\.\d\d)", price):
        item['list_price'] = re.search(r"Was (\$\d*\.\d\d)", price).group(1)
      if re.search(r"Reg. (\$\d*\.\d\d)", price):
        item['list_price'] = re.search(r"Reg. (\$\d*\.\d\d)", price).group(1)
      elif re.search(r"Sale (\$\d*\.\d\d)", price):
        item['sale_price'] = re.search(r"Sale (\$\d*\.\d\d)", price).group(1)
      elif re.search(r"(\$\d*\.\d\d)", price):
        item['list_price'] = re.search(r"(\$\d*\.\d\d)", price).group(1)
 
  def AddTags(self,item,url):
      
    par = urlparse.parse_qs(urlparse.urlparse(url).query)
    category = par['CategoryID']
    print '********************************************************category id:',category
   
