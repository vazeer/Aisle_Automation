# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
from scrapy.contrib.exporter import JsonLinesItemExporter
from scrapy.exceptions import DropItem

class TestScrapyPipeline(object):
    def process_item(self, item, spider):
        return item

class NordstromPipeline(object):

  def __init__(self):
    self.files = {}
    self.ids_seen = set()

  @classmethod
  def from_crawler(cls, crawler):
    pipeline = cls()
    crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
    crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
    return pipeline

  def process_item(self, item, spider):
    if item['product_item_num'] in self.ids_seen:
      raise DropItem("Duplicate item found: %s" % item)
    else:
      self.ids_seen.add(item['product_item_num'])
      self.exporter.export_item(item)
      return item

  def spider_opened(self, spider):
    out_file = open('%s_products.jl' % spider.name, 'w+b')
    self.files[spider] = out_file
    self.exporter = JsonLinesItemExporter(out_file)
    self.exporter.start_exporting()

  def spider_closed(self, spider):
    self.exporter.finish_exporting()
    out_file = self.files.pop(spider)
    out_file.close()
