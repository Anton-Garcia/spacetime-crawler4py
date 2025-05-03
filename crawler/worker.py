from threading import Thread

from inspect import getsource
from utils.download import download
from utils import get_logger
import scraper
import time
from extraction import process_webpage_text
from analysis import report_writer

class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        # basic check for requests in scraper
        assert {getsource(scraper).find(req) for req in {"from requests import", "import requests"}} == {-1}, "Do not use requests in scraper.py"
        assert {getsource(scraper).find(req) for req in {"from urllib.request import", "import urllib.request"}} == {-1}, "Do not use urllib.request in scraper.py"
        super().__init__(daemon=True)
        
    def run(self):
        #take all blacklist urls in the blacklist file and load them
        #(used later in is_valid())
        scraper.blacklist_hasher()

        #variable for counting links crawled - hoping for no server crashes during
        #real crawl time, so we can get an accurate count
        links_crawled = 0
        while True:
            try:
                tbd_url = self.frontier.get_tbd_url()
                if not tbd_url:
                    self.logger.info("Frontier is empty. Stopping Crawler.")
                    #do the analytics and report writing after the crawler is done
                    #automation is cool B)
                    report_writer(links_crawled)
                    break
                links_crawled += 1
                resp = download(tbd_url, self.config, self.logger)
                #Additional function - grab the text from the page to be used
                #for statistics later
                process_webpage_text(resp)
                self.logger.info(
                    f"Downloaded {tbd_url}, status <{resp.status}>, "
                    f"using cache {self.config.cache_server}.")
                scraped_urls = scraper.scraper(tbd_url, resp)
                for scraped_url in scraped_urls:
                    self.frontier.add_url(scraped_url)
                self.frontier.mark_url_complete(tbd_url)
                time.sleep(self.config.time_delay)
            except ValueError:
                # IP address error
                continue
                
