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


### REDIS

# Enables scheduling storing requests queue in redis.
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# Ensure all spiders share same duplicates filter through redis.
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# Don't cleanup redis queues, allows to pause/resume crawls.
SCHEDULER_PERSIST = True

# Specify the host and port to use when connecting to Redis (optional).
REDIS_HOST = 'localhost'
REDIS_PORT = 6379