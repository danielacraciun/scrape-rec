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

# Spidermon - monitoring tool
SPIDERMON_ENABLED = True
SPIDERMON_SPIDER_CLOSE_MONITORS = (
    'scrape_rec.monitors.SpiderCloseMonitorSuite',
)
EXTENSIONS = {
    'spidermon.contrib.scrapy.extensions.Spidermon': 500,
}

# Caching - cache responses on disk to save tons of time
# Only cache product pages, not listing pages to ensure we get to all products!
HTTPCACHE_ENABLED = True

# Make sure this is set to the same value as the
# docker-compose volume 'httpcache' for persistance
HTTPCACHE_DIR = '/var/lib/httpcache/'

# Save some space
HTTPCACHE_GZIP = True