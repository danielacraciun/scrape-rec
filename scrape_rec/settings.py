from os import environ

BOT_NAME = 'scrape_rec'

SPIDER_MODULES = ['scrape_rec.spiders']
NEWSPIDER_MODULE = 'scrape_rec.spiders'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'scrape_rec.pipelines.NeighborhoodFinderPipeline': 100,
    'scrapy_jsonschema.JsonSchemaValidatePipeline': 300,
    'scrape_rec.pipelines.PostgresPipeline': 400
}

# Be nice!
DOWNLOAD_DELAY = 3  # Average time between sending requests
RANDOMIZE_DOWNLOAD_DELAY = True  # Default for 0.5 to 1.5 times DOWNLOAD_DELAY
AUTOTHROTTLE_ENABLED = True  # Enable built-in autothrottle extension
AUTOTHROTTLE_TARGET_CONCURRENCY = 1  # Number of requests to send in paralel
CLOSESPIDER_ITEMCOUNT = 100  # Stop after about 100 items

# Spidermon - monitoring tool
SPIDERMON_ENABLED = True
SPIDERMON_SPIDER_CLOSE_MONITORS = (
    'scrape_rec.monitors.SpiderCloseMonitorSuite',
)

MYEXT_ENABLED = True
EXTENSIONS = {
    'scrape_rec.extensions.SpiderBotCallback': 400,
    'spidermon.contrib.scrapy.extensions.Spidermon': 500,
}

# Caching - cache responses on disk to save tons of time
# Only cache product pages, not listing pages to ensure we get to all products!
# HTTPCACHE_ENABLED = True

# Make sure this is set to the same value as the
# docker-compose volume 'httpcache' for persistance
HTTPCACHE_DIR = '/var/lib/httpcache/'

# Save some space
HTTPCACHE_GZIP = True

# Database settings
POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = environ.get('POSTGRES_PORT', 5342)
POSTGRES_DB = 'realestate'
POSTGRES_DB_STRING = 'postgres://{user}:{password}@{host}:{port}/{db}'.format(
  user=POSTGRES_USER,
  password=POSTGRES_PASSWORD,
  host=POSTGRES_HOST,
  port=POSTGRES_PORT,
  db=POSTGRES_DB
)


# Bot settings
BOT_TOKEN = environ.get('BOT_TOKEN')
