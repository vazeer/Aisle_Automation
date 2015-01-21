
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem
import urlparse
import urllib
from scrapy.selector import Selector

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors import LinkExtractor

class FlipkartTagsSpider(CrawlSpider):
  name = "flipkartTags"
  allowed_domains = ['flipkart.com']
  start_urls = [
       
    'http://www.flipkart.com/womens-clothing/shirts-tops-tunics/pr?sid=2oq%2Cc1r%2Ccck',
    'http://www.flipkart.com/womens-clothing/dresses-skirts/pr?sid=2oq%2Cc1r%2Cxzt',
    'http://www.flipkart.com/womens-clothing/ethnic-wear/pr?sid=2oq%2Cc1r%2C3pj',
    'http://www.flipkart.com/womens-clothing/polos-t-shirts/pr?sid=2oq%2Cc1r%2Cfpt',
    'http://www.flipkart.com/womens-clothing/jeans-shorts/pr?sid=2oq%2Cc1r%2Cuuk',
    'http://www.flipkart.com/womens-clothing/leggings-jeggings/pr?sid=2oq%2Cc1r%2Cq7g',
    'http://www.flipkart.com/womens-clothing/trousers-capris/pr?sid=2oq%2Cc1r%2Cuo8',
    'http://www.flipkart.com/womens-clothing/shrugs-jackets/pr?sid=2oq%2Cc1r%2Cpyo',
    'http://www.flipkart.com/womens-clothing/formal-wear/pr?sid=2oq%2Cc1r%2Cf4y',
    'http://www.flipkart.com/womens-clothing/sports-gym-wear/pr?sid=2oq%2Cc1r%2C6p8',
    'http://www.flipkart.com/womens-clothing/fabrics/pr?sid=2oq%2Cc1r%2C9tg',
    'http://www.flipkart.com/womens-clothing/lingerie-sleepwear/pr?sid=2oq%2Cc1r%2Ctbt',
    'http://www.flipkart.com/womens-clothing/accessories/pr?sid=2oq%2Cc1r%2C3gz',
    'http://www.flipkart.com/womens-clothing/winter-seasonal-wear/pr?sid=2oq%2Cc1r%2C67x',
    
    'http://www.flipkart.com/womens-footwear/flats/pr?sid=osp%2Ciko%2C9d5&ref=1db1a86a-b74e-4f49-b7c0-1953a8c7d35f',
    'http://www.flipkart.com/womens-footwear/bellies/pr?sid=osp%2Ciko%2C974&ref=02e71cc0-bc86-44d8-ad1d-7efff79491cb',
    'http://www.flipkart.com/womens-footwear/heels/pr?sid=osp%2Ciko%2C6q1&ref=0f9209b5-f2cf-41c5-a587-e3a0fce0b561',
    'http://www.flipkart.com/womens-footwear/wedges/pr?sid=osp%2Ciko%2Cjpm&ref=28549bfe-e1a0-4c89-9a89-e58646e1272c',
    'http://www.flipkart.com/womens-footwear/formals/pr?sid=osp%2Ciko%2C2ox&ref=8336d188-6b28-4f34-ac2f-6c84d521976b',
    'http://www.flipkart.com/womens-footwear/casual-shoes/pr?sid=osp%2Ciko%2Csx7&ref=eed61bc9-b17b-419c-b5b6-3d2d613fe885',
    'http://www.flipkart.com/womens-footwear/sports-shoes/pr?sid=osp%2Ciko%2Cd20&ref=73943004-33f2-42d0-9438-e8d8c43c3964',
    'http://www.flipkart.com/womens-footwear/sports-sandals/pr?sid=osp%2Ciko%2Cojy&ref=e5529cfc-d7dd-4bb8-ab7b-8b76e65ddd72',
    'http://www.flipkart.com/womens-footwear/slippers-flip-flops/pr?sid=osp%2Ciko%2Ciz7&ref=53e1ce66-b6d4-4fcb-9b46-59dbd55a2842',
    'http://www.flipkart.com/womens-footwear/sandals/pr?sid=osp%2Ciko%2Criq&ref=31b84331-f811-4499-ada1-8c7d209315b7',
    
    'http://www.flipkart.com/bags-wallets-belts/bags/hand-bags/~women/pr?sid=reh%2Cihu%2Cm08&ref=38b6fd05-d060-4959-8691-cbee3f021de3',
    'http://www.flipkart.com/bags-wallets-belts/bags/totes/~women/pr?sid=reh%2Cihu%2Cv57&ref=93f8fb83-d459-416f-ae07-39e1993e467f',
    
  ]
  
  rules = (
  Rule(SgmlLinkExtractor(restrict_xpaths='//li[@class="store"]')),
  Rule(SgmlLinkExtractor(restrict_xpaths='//ul[@id="length" or @id="brand" or @id="ocassion" or @id="sleeves" or @id="occasion" or @id="type" or @id="pattern" or @id="ideal_for"]//li'),callback='parse_item'),
  
  
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
 
    
   
    productIDs = []
    productsurls = hxs.xpath('//div[@class="unit size1of3"]//a[@data-tracking-id="prd_img"]/@href').extract()
    for producturl in productsurls:
       if producturl.strip():
         par = urlparse.parse_qs(urlparse.urlparse(producturl).query)
         temp = self.AddTags(item,producturl)
         productIDs.append(temp)
   
    taglist1  = hxs.xpath('(//div[@id="breadcrumb"]//a/text())[position()>1]').extract()  
    taglist2  = hxs.xpath('(//a[@class="parent current active"]//text())').extract() 
    taglist3  = hxs.xpath('(//a[@class="active selected"]//text())').extract() 
    list = []
  
    for index in range(len(taglist1)):
        v = (taglist1[index])
        v = v.strip()
        if v!='/' and  v:
          list.append(v)
    for index in range(len(taglist2)):
        v = (taglist2[index])
        v = v.strip()
        if v!='/' and  v:
          list.append(v)
    for index in range(len(taglist3)):
        v = (taglist3[index])
        v = v.strip()
        if v!='/' and  v:
          list.append(v)      
     
     
            
    item['tag'] = list 
    item['tag_product_ids']  = productIDs
      
  
    return item

  def AddTags(self,item,url):  
     par = urlparse.parse_qs(urlparse.urlparse(url).query)
     res = par["pid"]
     return res[0]
 
   
 