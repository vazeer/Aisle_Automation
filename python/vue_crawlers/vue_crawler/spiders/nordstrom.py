'''
Created on Jun 13, 2014

@author: Behrooz
'''

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem

import urlparse
import urllib
class NordstromSpider(CrawlSpider):
  name = "nordy"
  allowed_domains = ['shop.nordstrom.com']
  start_urls = ['http://shop.nordstrom.com/c/womens-clothing?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-shoes',
                'http://shop.nordstrom.com/c/womens-handbags',
#                'http://shop.nordstrom.com/c/accessories-handbags']
  ]
  rules = (
  # //div[@id="women-panel"]//ul[1]|(//ul[@class="nav-group"])[2]
  
  #(//h3[text()='Category']//following::ul[1])|//a[@manual_cm_sp="Top Navigation-_-Shoes-_-Women"]//following::ul[1]
  
  
  
    Rule(SgmlLinkExtractor(restrict_xpaths='((//h3[@class="nav-entry-clothing"])[1])//following::ul[1]//li[following-sibling::li[@class="spacer-hack"]]|//ul[@class="nav-group"][position()>1]|((//h3[@class="nav-entry-shoes"])[position()>1])//following::ul[1]//li[following-sibling::li[@class="spacer-hack"]]')),
    Rule(SgmlLinkExtractor(restrict_xpaths='//div[@id="leftnav"]//a'), callback='parse_item',follow=True),
    
    Rule(SgmlLinkExtractor(restrict_xpaths='(//ul[@class="numbers"])[1]//li'), callback='parse_item',follow=True),
    
  
       
    Rule(SgmlLinkExtractor(restrict_xpaths=('//a[@class="title"]')),
         callback='parse_item'),
         
         
         
#             # Extract the different pages on the main site.
#    Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="fashion-results-pager"]'))),
#      # Extract the different items on the page.
#    Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@role="main"]'
#                                            '//div[@class="fashion-item"]')),
#         callback='parse_item'),
  )

  def parse_item(self, response):
#     print response.url
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
   # item_num_str = sel.xpath('//div[@class="item-number-wrapper"]/text()').extract()[0]
  #  item_num = re.findall(r'\d+', item_num_str)[0]
    item['source_site'] = "shop.nordstrom.com"
    item['product_title'] = str(sel.xpath('//section[@id="product-title"]//h1/text()').extract()[0])
    
    value = self.AddTags(item,response.url)
    item['product_item_num'] = value
    
    
    item['product_url'] = response.url
    item['description'] = sel.xpath('//section[@id="details-and-care"]//ul[@class="style-features"]//li/text()').extract()
    item['image_urls'] = [sel.xpath('//div[@id="product-image"]//img/@src').extract()[0]]
    res  = sel.xpath('//nav[@id="breadcrumb-nav"]/ul//li//text()').extract()
    
    print '*************',res
    
    list = [];
    for index in range(len(res)):
        v = str(res[index])
        if index!=0 and v!='/':
            list.append(v)
    
    item['product_tags'] = list   
    
    
    
    item['product_sizes'] = sel.xpath('//div[@id="size-buttons"]//button[@class="option-label"]/@value').extract()
    item['product_colors'] = sel.xpath('(//select[@id="color-selector"]//option/text())[position()>1]').extract()
    
    
    sale_text = sel.xpath('(//section[@id="price"]//span[@class="sale-price"]/text()|//section[@id="price"]//span[@class="sale-price long-price"]/text())[1]').extract()
    list_text = sel.xpath('(//section[@id="price"]//span[@class="regular-price"]/text())[1]').extract()
    print 'KKKKKKKKKK111111 ' ,sale_text  
    print 'KKKKKKKKKK222222' ,list_text 
    
    print '',
    
    return item

  def PriceExtractor(self, item, selector):
    price = selector.xpath('//section[@id="price"]//td[@class="item-price heading-2"]//span/text()').extract()
    if not price:
      sale_text = selector.xpath('(//section[@id="price"]//span[@class="sale-price"]/text())[1]').extract()
      if sale_text:
        sale_text = str(sale_text[0])  
        print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%sale ' ,sale_text  
        item['sale_price'] = re.search(r"Now: (\INR \d*\.\d\d)", sale_text).group(1)
      list_text = selector.xpath('(//section[@id="price"]//span[@class="regular-price"]/text())[1]').extract()
      if list_text:
        list_text = str(list_text[0])  
        print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%regular' ,list_text  
        item['list_price'] = re.search(r"Was: (\INR \d*\.\d\d)", list_text).group(1)
    else:
      item['list_price'] = price[0]  
        
  def AddTags(self,item,url):  
     par = urlparse.parse_qs(urlparse.urlparse(url).query)
     url=urllib.unquote(url).decode('utf8') 
     Segments = url.split('/')
     val = Segments[len(Segments)-1]
     res = val.split('?')
     return res[0]
