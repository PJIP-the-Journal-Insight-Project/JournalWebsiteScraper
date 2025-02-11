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
        'https://academic.oup.com/analysis/pages/Editorial_Board',
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

        # Find all <p> elements with class "paragraph_03"
        paragraphs = soup.find_all('p', class_='paragraph_03')

        # Extract the text before the <span class="public-address"> element
        results = []
        for p in paragraphs:
            # Find the <span class="public-address"> element
            span = p.find('span', class_='public-address')
            if span:
                # Extract the text before the <span>
                text = p.get_text(strip=True).split(span.get_text(strip=True))[0].strip()
                results.append(text)

        # Join all results into a single string separated by commas
        combined_results = ', '.join(results)

        # Yield the result with the URL and the combined text
        yield {
            'url': response.url,
            'scraped_data': combined_results
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