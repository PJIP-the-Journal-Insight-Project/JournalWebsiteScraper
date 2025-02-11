import scrapy
from scrapy.crawler import CrawlerProcess

class EditorialBoardSpider(scrapy.Spider):
    name = "editorial_spider"
    start_urls = [
        'https://brill.com/view/journals/ijmh/ijmh-overview.xml'
    ]

    def parse(self, response):
        # Extract the entire HTML content of the page as a string
        html_content = response.text
        # Yield the result with the URL and the HTML content
        yield {
            'url': response.url,
            'html_content': html_content
        }

# To run the spider without the need for the 'scrapy' command-line tool
if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "FEEDS": {
            "pages_html.csv": {"format": "csv"},
        },
    })

    process.crawl(EditorialBoardSpider)
    process.start()

# scrapy crawl editorial_spider -o editors.csv