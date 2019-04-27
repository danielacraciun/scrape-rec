BOT_NAME = 'scrape_rec'

SPIDER_MODULES = ['scrape_rec.spiders']
NEWSPIDER_MODULE = 'scrape_rec.spiders'

ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 1

ITEM_PIPELINES = {
    'scrapy_jsonschema.JsonSchemaValidatePipeline': 100,
    'scrape_rec.pipelines.NeighborhoodFinderPipeline': 300,
    'scrape_rec.pipelines.PostgresPipeline': 400
}
