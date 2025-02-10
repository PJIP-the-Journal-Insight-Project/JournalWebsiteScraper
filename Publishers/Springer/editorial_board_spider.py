import scrapy

class EditorialSpider(scrapy.Spider):
    name = "editorial_spider"

    start_urls = [
        'https://www.springer.com/journal/12136/editorial-board',
        'https://www.springer.com/journal/44204/editorial-board',
        'https://www.springer.com/journal/13752//editorial-board',
    ]

    def parse(self, response):
        # Extract and clean the page title
        page_title = response.css("title::text").get()
        clean_title = " ".join(page_title.split()) if page_title else ""

        # Extract the content of the target div
        editorial_content = response.css(
            "div.app-jflow-content-page.placeholder.placeholder-editorialBoard.u-text-sans-serif"
        ).get()

        # Yield the extracted data
        yield {
            'title': clean_title,  # Store the cleaned title
            'url': response.url,
            'editorial_content': editorial_content,
        }


# scrapy runspider springer_scrape.py -o springer_scrape.csv
