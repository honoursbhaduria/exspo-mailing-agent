import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import argparse
from scrapy.crawler import CrawlerProcess
from src.discovery.spider import MicroInfluencerSpider

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--niche", default="Fashion & Beauty")
    parser.add_argument("--limit", default=70, type=int)
    args = parser.parse_args()

    process = CrawlerProcess(settings={
        "DOWNLOADER_MIDDLEWARES": {
            "src.discovery.middlewares.CollabstrRequestsMiddleware": 543,
        },
        "ITEM_PIPELINES": {
            "src.discovery.pipelines.InfluencerCleaningPipeline": 300,
        },
        "LOG_LEVEL": "INFO",
        "ROBOTSTXT_OBEY": False,
        "CONCURRENT_REQUESTS": 4,
        "DOWNLOAD_DELAY": 0.2,
    })

    process.crawl(MicroInfluencerSpider, target_niche=args.niche, limit=args.limit)
    process.start()

if __name__ == "__main__":
    main()
