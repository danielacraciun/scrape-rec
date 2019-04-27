BOT_NAME = 'scrape_rec'

SPIDER_MODULES = ['scrape_rec.spiders']
NEWSPIDER_MODULE = 'scrape_rec.spiders'

ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 1

ITEM_PIPELINES = {
    'scrape_rec.pipelines.NeighborhoodFinderPipeline': 100,
    'scrapy_jsonschema.JsonSchemaValidatePipeline': 300,
    'scrape_rec.pipelines.PostgresPipeline': 400
}