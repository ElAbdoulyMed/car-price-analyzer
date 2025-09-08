# Scrapy settings for carcompare project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os
from dotenv import load_dotenv
load_dotenv()
BOT_NAME = "carcompare"

SPIDER_MODULES = ["carcompare.spiders"]
NEWSPIDER_MODULE = "carcompare.spiders"

ADDONS = {}

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DATABASE = os.getenv("MONGO_DATABASE")
ITEM_PIPELINES = {
    "carcompare.pipelines.MongoDBPipeline": 300,
}
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_LAUNCH_OPTIONS = {   # ADDED
    "headless": True,           # Run browser without a GUI (faster, less memory)
    "timeout": 30 * 1000,       # Max time (ms) to start the browser = 30s
}
# Configures how the Playwright browser is launched


PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 30 * 1000  # ADDED
# Max time (ms) Playwright waits for a page to load = 30s

PLAYWRIGHT_MAX_CONTEXTS = 8  # ADDED - allow parallel browser contexts
# How many browser contexts can exist at the same time (like isolated sessions)

PLAYWRIGHT_MAX_PAGES_PER_CONTEXT = 8  # ADDED - reuse tabs
# How many tabs each context can open before rotating to a new one

# Optional: block unnecessary resources (images, fonts, ads) to speed up
PLAYWRIGHT_PROCESS_REQUEST_HEADERS = None  # ADDED
# Keeps original request headers (don’t override them)

PLAYWRIGHT_ABORT_REQUEST = lambda req: req.resource_type in [  # ADDED
    "image", "media", "font", "stylesheet", "other"
]
# Prevents Playwright from downloading unnecessary resources
# This makes scraping faster by skipping images, ads, fonts, videos, etc.

# Crawl responsibly
#USER_AGENT = "carcompare (+http://www.yourdomain.com)"
# (Optional) Set a custom User-Agent to identify your scraper



# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "carcompare (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Concurrency and throttling settings
CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS_PER_DOMAIN = 8
DOWNLOAD_DELAY = 0.15

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "carcompare.middlewares.CarcompareSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "carcompare.middlewares.CarcompareDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "carcompare.pipelines.CarcomparePipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 0.1
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 1.0
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 6.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"
