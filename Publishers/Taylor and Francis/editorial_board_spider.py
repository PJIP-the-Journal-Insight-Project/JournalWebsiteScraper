"""
Note: Only partially works at present. Using <strong> tags not viable to identify 'Speed Data' as this is not standarised across Taylor and Francis Journals.
Instead, should just take whole div content and parse from there.

Also, Taylor and Francis uses cloudflare that blocks crawlers hence the need for proxy (ScrapeOps has free but limited API). Must use 'cloudflare_level_1'.

"""

import scrapy
from urllib.parse import urlencode

API_KEY = 'xxxx-xxxxx-xxxx-xx'  # Replace with ScrapeOps API key


def get_scrapeops_url(url):
    """
    Constructs the proxy URL using ScrapeOps with the provided API key and target URL.
    """
    payload = {'api_key': API_KEY, 'url': url, 'bypass': 'cloudflare_level_1'}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url


class EditorialBoardSpider(scrapy.Spider):
    name = "editorial_board"

    # Define the list of URLs to scrape
    start_urls = [
        'https://www.tandfonline.com/journals/cang20/about-this-journal',
        'https://www.tandfonline.com/journals/casp20/about-this-journal',
        'https://www.tandfonline.com/journals/rajp20/about-this-journal',
    ]

    def start_requests(self):
        """
        Generates Scrapy requests for each URL, routed through ScrapeOps proxy.
        """
        for url in self.start_urls:
            yield scrapy.Request(url=get_scrapeops_url(url), callback=self.parse)

    def parse(self, response):
        """
        Extracts the required data from the page and yields it as a dictionary.
        """
        # Extract the full HTML content of the <div> under the specified <h2>
        editorial_html = response.xpath('//h2[@id="editorial-board"]/following-sibling::div[1]').get()

        # Extract speed/acceptance information
        speed_data = response.xpath('//div[@class="speed"]//li')

        # Parse the speed/acceptance data
        speed_info = {}
        for item in speed_data:
            # Extract the value inside <strong> and the label after it
            value = item.xpath('./strong/text()').get()  # Value inside <strong>
            label = item.xpath('text()').getall()  # Text after <strong>
            label = ' '.join([text.strip() for text in label if text.strip()])  # Clean and join text
            if value and label:
                speed_info[label] = value

        yield {
            'Editorial Board Content': editorial_html,
            **speed_info,  # Add speed/acceptance data dynamically as columns
        }

# Outputs as .csv named "taylorandfrancis"
# scrapy runspider editorial_board_spider.py -o taylorandfrancis.csv
