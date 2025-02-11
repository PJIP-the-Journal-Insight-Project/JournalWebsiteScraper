import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
import time
import random

# List of user agents to rotate
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 10; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
]


class EditorialBoardSpider(scrapy.Spider):
    name = "editorial_spider"
    start_urls = [

        # these are the urls of de gruyter journals that were indexed in the PJIP as of Feb 2025
        
        'https://www.degruyter.com/journal/key/auk/html',
        'https://www.degruyter.com/journal/key/apeiron/html',
        'https://www.degruyter.com/journal/key/agph/html',
        'https://www.degruyter.com/journal/key/kant/html',
        'https://www.degruyter.com/journal/key/mp/html',
        'https://www.degruyter.com/journal/key/mopp/html',
        'https://www.degruyter.com/journal/key/sats/html',
        'https://www.degruyter.com/journal/key/hzhz/html',
        'https://www.degruyter.com/journal/key/ans/html',
        'https://www.degruyter.com/journal/key/agms/html',
        'https://www.degruyter.com/journal/key/ajle/html',
        'https://www.degruyter.com/journal/key/ercl/html',
        'https://www.degruyter.com/journal/key/ami/html',
        'https://www.degruyter.com/journal/key/iph/html',
        'https://www.degruyter.com/journal/key/math/html',
        'https://www.degruyter.com/journal/key/taa/html',
        'https://www.degruyter.com/journal/key/ijld/html',
        'https://www.degruyter.com/journal/key/roe/html',
        'https://www.degruyter.com/journal/key/phys/html',
        'https://www.degruyter.com/journal/key/iss/html',
        'https://www.degruyter.com/journal/key/CHEM/html',
        'https://www.degruyter.com/journal/key/itit/html',
        'https://www.degruyter.com/journal/key/nanoph/html',
        'https://www.degruyter.com/journal/key/eng/html',
        'https://www.degruyter.com/journal/key/cogsem/html',
        'https://www.degruyter.com/journal/key/eujal/html',
        'https://www.degruyter.com/journal/key/jhsl/html',
        'https://www.degruyter.com/journal/key/jjl/html',
        'https://www.degruyter.com/journal/key/jwl/html',
        'https://www.degruyter.com/journal/key/lass/html',
        'https://www.degruyter.com/journal/key/lexi/html',
        'https://www.degruyter.com/journal/key/ling/html',
        'https://www.degruyter.com/journal/key/mc/html',
        'https://www.degruyter.com/journal/key/opli/html',
        'https://www.degruyter.com/journal/key/stuf/html',
        'https://www.degruyter.com/journal/key/niet/html',
        'https://www.degruyter.com/journal/key/cmam/html',
        'https://www.degruyter.com/journal/key/dma/html',
        'https://www.degruyter.com/journal/key/ael/html',
        'https://www.degruyter.com/journal/key/cmb/html',
        'https://www.degruyter.com/journal/key/bejeap/html',
        'https://www.degruyter.com/journal/key/znth/html',
        'https://www.degruyter.com/journal/key/jnma/html',
        'https://www.degruyter.com/journal/key/snde/html',
        'https://www.degruyter.com/journal/key/lehr/html',
        'https://www.degruyter.com/journal/key/rle/html',
        'https://www.degruyter.com/journal/key/bejte/html',
        'https://www.degruyter.com/journal/key/bejm/html',
        'https://www.degruyter.com/journal/key/jnet/html',
        'https://www.degruyter.com/journal/key/zna/html',
        'https://www.degruyter.com/journal/key/pubhef/html',
        'https://www.degruyter.com/journal/key/roms/html',
        'https://www.degruyter.com/journal/key/eqc/html',
        'https://www.degruyter.com/journal/key/npprj/html',
        'https://www.degruyter.com/journal/key/bchm/html',
        'https://www.degruyter.com/journal/key/cclm/html',
        'https://www.degruyter.com/journal/key/pac/html',
        'https://www.degruyter.com/journal/key/revac/html',
        'https://www.degruyter.com/journal/key/revic/html',
        'https://www.degruyter.com/journal/key/helia/html',
        'https://www.degruyter.com/journal/key/mamm/html',
        'https://www.degruyter.com/journal/key/sagmb/html',
        'https://www.degruyter.com/journal/key/jag/html',
        'https://www.degruyter.com/journal/key/znb/html',
        'https://www.degruyter.com/journal/key/corrrev/html',
        'https://www.degruyter.com/journal/key/polyeng/html',
        'https://www.degruyter.com/journal/key/revce/html',
        'https://www.degruyter.com/journal/key/rams/html',
        'https://www.degruyter.com/journal/key/ncrs/html',
        'https://www.degruyter.com/journal/key/ijnes/html',
        'https://www.degruyter.com/journal/key/cercles/html',
        'https://www.degruyter.com/journal/key/alr/html',
        'https://www.degruyter.com/journal/key/css/html',
        'https://www.degruyter.com/journal/key/comm/html',
        'https://www.degruyter.com/journal/key/cllt/html',
        'https://www.degruyter.com/journal/key/iral/html',
        'https://www.degruyter.com/journal/key/lpp/html',
        'https://www.degruyter.com/journal/key/psicl/html',
        'https://www.degruyter.com/journal/key/semi/html',
    ]

    # Custom settings for anti-detection
    custom_settings = {
        'DOWNLOAD_DELAY': random.uniform(1, 5),  # Random delay between 1 and 5 seconds
        'USER_AGENT': random.choice(USER_AGENTS),  # Randomly select a user agent
        'AUTOTHROTTLE_ENABLED': True,  # Automatically throttle request rate
        'AUTOTHROTTLE_START_DELAY': 1,  # Initial delay before starting to throttle
        'AUTOTHROTTLE_MAX_DELAY': 10,  # Maximum delay between requests
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,  # Target concurrency for throttling
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,  # Limit concurrent requests to the same domain
        'ROBOTSTXT_OBEY': True,  # Respect robots.txt rules
        'RANDOMIZE_DOWNLOAD_DELAY': True,  # Randomize the delay between requests
    }

    def start_requests(self):
        # Randomize the order of URLs to mimic human behavior
        random.shuffle(self.start_urls)
        for url in self.start_urls:
            # Random delay before starting the next request
            time.sleep(random.uniform(1, 5))
            # Rotate user agent for each request
            headers = {'User-Agent': random.choice(USER_AGENTS)}
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        # Extract the entire HTML content of the page as a string
        html_content = response.text
        # Use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the <h3> element with the text "Editorial"
        editorial_heading = soup.find('h3', text='Editorial')

        if editorial_heading:
            # Find the next sibling <div> with class "metadataInfoFont"
            metadata_div = editorial_heading.find_next('div', class_='metadataInfoFont')

            if metadata_div:
                # Replace <br> tags with dashes
                for br in metadata_div.find_all('br'):
                    br.replace_with(' - ')

                # Extract all HTML content inside the <div>
                editorial_html = str(metadata_div)

                # Yield the result with the URL and the modified HTML
                yield {
                    'url': response.url,
                    'scraped_data': editorial_html
                }


# To run the spider without the need for the 'scrapy' command-line tool
if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "FEEDS": {
            "parsed_data.csv": {"format": "csv"},
        },
    })

    process.crawl(EditorialBoardSpider)
    process.start()
