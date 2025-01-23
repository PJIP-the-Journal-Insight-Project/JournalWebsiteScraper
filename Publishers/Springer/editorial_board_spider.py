import scrapy

class EditorialSpider(scrapy.Spider):
    name = "editorial_spider"

    # Replace this with the URL containing the HTML above
    start_urls = [
        'https://www.springer.com/journal/12136/editorial-board',
        'https://www.springer.com/journal/44204/editorial-board',
        'https://www.springer.com/journal/13752/editorial-board',
    ]

    def parse(self, response):
        # Extract the content of the target div
        editorial_content = response.css(
            "div.app-jflow-content-page.placeholder.placeholder-editorialBoard.u-text-sans-serif"
        ).get()

        # Yield the extracted content
        yield {
            'url': response.url,
            'editorial_content': editorial_content,
        }

# Outputs as .csv named "springer"
# scrapy runspider Springer.py -o springer.csv

