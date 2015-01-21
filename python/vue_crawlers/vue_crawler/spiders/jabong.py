import re
import json
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from vue_crawler.items import VueCrawlerItem


class JabongSpider(CrawlSpider):
   name = 'jabong'
   allowed_domains = ['jabong.com']
   
   
   data = open('/home/vazeer/Desktop/ScrappersData/IndianData/jabong/jabongTags_products.jl')
   jsondata = json.load(data)
   links =[]
   for s in jsondata:
    links.append(s['product_item_num'])
   print '^^^^^^^^^^^^^^^^^^^^^^^^^^', len(links) 
   start_urls =links
   domain_depths = 3
   rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="cat-filter catTreeLvl1"]'))),
        Rule(SgmlLinkExtractor(restrict_xpaths=('(//div[@id="facet_brand"]//a)'))),
        Rule(SgmlLinkExtractor(restrict_xpaths=('//a[@unbxdattr="product"]')),callback='myParserTest')
    
        
    )
 
   def myParserTest(self,response):
    print '**************test********************* URL:', response.url,response.meta['depth']
    item = VueCrawlerItem()
    item['product_item_num'] = response.url
    return item
   def parse_item(self, response):
    print '************* URL:', response.url
    sel = Selector(response)
    
    item = VueCrawlerItem()
   
    item['source_site'] = "jabong.com"
    title = sel.xpath('//span[@itemprop="name"]/text()').extract()[0]
    item['product_title'] = str(title.strip())
    item_num_str = sel.xpath('//input[@name="configSku"]/@value').extract()[0]
    
    item['product_item_num'] = item_num_str
    
    item['product_url'] = response.url
    
    item['image_urls'] = [sel.xpath('//ul[@class="imageview-slider"]//li/img/@src').extract()[0]]
       
    item['description'] = sel.xpath('//p[@itemprop="description"]/text()').extract()  
    bullet_description = sel.xpath('//div[@id="productInfo"]//td[@class="c222"]/text()').extract()
    for desc_bullet in bullet_description:
      if desc_bullet.strip():
        item['description'].append(desc_bullet.strip())    
   
    sizes  = sel.xpath('//ul[@id="listProductSizes"]//li/text()').extract()
   
    sizesstripped = [];
    for index in range(len(sizes)):
        v = str(sizes[index])
        v = v.strip()
        if  v!='':
          sizesstripped.append(v)
          
    item['product_sizes'] = sizesstripped
    
    taglist1  = sel.xpath('(//div[@class="breadcrumbs mb8"]//a/@title)[position() > 1]').extract()
    taglist2  = sel.xpath('//div[@id="productInfo"]//td[@class="c222"]/text()').extract()
    taglist3  = sel.xpath('//span[@itemprop="brand"]/text()').extract()
   
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

    item['product_tags'] = list 
    
    
    try:
     item['currencyCode'] = sel.xpath('//span[@itemprop="priceCurrency"]/@content').extract()[0]
    
     item['sale_price']= sel.xpath('//span[@itemprop="price"]/text()').extract()[0]
    
     saleprice = sel.xpath('//span[@class="striked-price fs14 c222 d-inline mt5"]/text()').extract()[0]
     if saleprice:
        saleprice = saleprice.replace(',','')
        item['list_price'] = re.findall('\d+',saleprice)[0]
     
    except: 
     pass
        
    return item

    
