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

class Forever21Spider(CrawlSpider):
  name = "forever"
  allowed_domains = ['forever21.com']
  start_urls = [
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=dress_casual',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=dress_day-to-night',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=dress_night-out',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=dress_mini',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=dress_maxi',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=dress_fit-and-flare',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=top_basic',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=top_graphic-tees',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=top_crop-tops',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=top_bodysuits-bustiers',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=top_camis_tanks',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=top_t-shirts',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=top_blouses-sleeveless',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=top_blouses-short-sleeves',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=top_blouses-long-sleeves',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=top_blouses-printed',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=top_blouses-embellished',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=top_blouses-peplum',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=top_blouses-chambray',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=sweater_basic',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=sweater_cardigans',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=sweater_sweatshirts-hoodies',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=sweater_printed',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=sweater_embellished',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=outerwear_jean-jackets',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=outerwear_moto-jackets',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=outerwear_utility-jackets',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=outerwear_bomber-jackets',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=outerwear_varsity-jackets',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=outerwear_faux-leather-jackets',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=outerwear_blazers',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=outerwear_coats',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=outerwear_vests',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=bottom_jeans-basics',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=bottom_jeans-skinny',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=bottom_jeans-printed',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=bottom_jeans-distressed',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=bottom_leggings-basics',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=bottom_leggings-printed',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=bottom_leggings-embellished',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=bottom_pants-printed',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=bottom_pants-skinny',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=bottom_pants-cropped',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=bottom_pants-loose-fit',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=bottom_pants-trouser',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=bottom_shorts-denim',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=bottom_shorts-lace',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=bottom_shorts-printed',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=bottom_shorts-trouser',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=bottom_skirt-mini',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=bottom_skirt-midi',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=bottom_skirt-maxi',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=bottom_skirt-skater',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=bottom_skirt-bodycon',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=bottom_skirt-printed',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=jumpsuit_romper',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=activewear_sports-bra',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=activewear_top',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=activewear_pullover-jackets',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=activewear_bottoms',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=intimates-bras',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=intimates-panties',
    'http://www.forever21.com/IN/Product/SetCategory.aspx?br=f21&category=intim_lingeriesets',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=intimates-babydoll-slips',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=intimates-pajamas-robes',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=intimates-loungewear',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=intimates-lingerie-accessories',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=swimwear_tops',
    'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=swimwear_bottoms',
    
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_tees-tanks',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_tees-tanks-basic',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_tees-tanks-graphic',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_tees-tanks-tank',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_tees-tanks-longslv',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_shirts',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_shirts_classic',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_shirts_fitted',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_shirts_dress',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_shirts_polo',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_sweaters',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_hoodies',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_blazers-and-vests',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_jackets-and-coats',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_bottom_denim',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_bottom_denim_skinny',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_bottom_denim_slim',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_bottom_denim_straight',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_bottom_pants',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_bottom_shorts',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_swimwear',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_underwear-socks',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_hats-scarves',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_accessories',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_accessories-sunglasses',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_accessories-ties',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_accessories-belts',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_accessories-bags',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_accessories-jewelry-watches',
    'http://www.forever21.com/IN/Product/Category.aspx?br=21men&category=m_shoes' 
    
  ]
  
  rules = (
  Rule(SgmlLinkExtractor(restrict_xpaths='(//table[@class="PagerContainerTable"])[1]'),follow=True),
  Rule(SgmlLinkExtractor(restrict_xpaths='//div[@class="ItemImage"]//a[1]'),callback='parse_item'),
  )
  
      
  def parse_item(self, response):
   # print '*********************************** URL:', response.url
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
    item_num_str = sel.xpath('//input[@id="ctl00_MainContent_hdProductId"]/@value').extract()[0]
   # item_num = re.findall(r'\d+', item_num_str)[0]
    item['source_site'] = "forever21.com"
    title = str(sel.xpath('//font[@class="items_name"]/text()').extract()[0])
    item['product_title'] = title.strip()
    item['product_item_num'] = item_num_str
    item['product_url'] = response.url
   # item['description'] = sel.xpath('//span[@id="product_overview"]/ul//li/text()').extract()
    desList = [] 
    bullet_description = sel.xpath('//span[@id="product_overview"]/ul//li/text()').extract()
    for desc_bullet in bullet_description:
      if desc_bullet.strip():
        desList.append(desc_bullet.strip())
        
    item['description'] = desList
    item['image_urls'] = sel.xpath('//img[@class="ItemImage"]/@src').extract()[0]
   
    res  = sel.xpath('//a[@class="forever21"]/u/text()').extract()
    print '*************',res
    list = [];
    for index in range(len(res)):
        v = str(res[index])
        v = v.strip()
        if  v!='/':
            list.append(v)
    item['product_tags'] = list   
    sizes = sel.xpath('(//select[@id="ctl00_MainContent_ddlSize"]//option/text())[position()>1]').extract()
    
    sizesstripped = [];
    for index in range(len(sizes)):
        v = str(sizes[index])
        v = v.strip()
        if  v!='':
          sizesstripped.append(v)
    item['product_sizes'] = sizesstripped
    item['product_colors'] = sel.xpath('(//select[@id="ctl00_MainContent_ddlColor"]//option/text())[position()>1]').extract()
    
    return item

  def PriceExtractor(self, item, selector):
    price = selector.xpath('//font[@class="items_price"]/text()').extract()
    item['list_price'] = price[0]

  def AddTags(self,item,url):  
     par = urlparse.parse_qs(urlparse.urlparse(url).query)
     url=urllib.unquote(url).decode('utf8') 
     Segments = url.split('/')
     val = Segments[len(Segments)-1]
     res = val.split('?')
     return res[0]
    
 
   
 