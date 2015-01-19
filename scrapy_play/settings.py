# Scrapy settings for dirbot project

DEPTH_PRIORITY = 1

SPIDER_MODULES = ['scrapy_play.spiders']
NEWSPIDER_MODULE = 'scrapy_play.spiders'
DEFAULT_ITEM_CLASS = 'scrapy_play.items.Post'

ITEM_PIPELINES = {
    'scrapy_play.pipelines.JsonWriterPipeline': 300,
}
