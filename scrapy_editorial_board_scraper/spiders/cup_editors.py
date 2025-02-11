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

        # these are the urls of cambridge university press journals that were indexed in the PJIP as of Feb 2025
        
        'https://www.cambridge.org/core/journals/british-journal-for-the-history-of-science/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/bulletin-of-symbolic-logic/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/canadian-journal-of-philosophy/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/dialogue-canadian-philosophical-review-revue-canadienne-de-philosophie/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/economics-and-philosophy/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/episteme/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/hegel-bulletin/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-symbolic-logic/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-the-american-philosophical-association/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/kantian-review/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/philosophy/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/review-of-symbolic-logic/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/social-philosophy-and-policy/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/utilitas/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/historical-journal/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/anglo-saxon-england/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-british-studies/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-african-history/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-modern-african-studies/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/modern-asian-studies/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-southeast-asian-studies/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/contemporary-european-history/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/itinerario/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/slavic-review/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/central-european-history/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-latin-american-studies/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/arabic-sciences-and-philosophy/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-american-studies/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-the-gilded-age-and-progressive-era/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/american-antiquity/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/business-history-review/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/financial-history-review/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/international-labor-and-working-class-history/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-economic-history/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/british-catholic-history/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/church-history/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-ecclesiastical-history/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/acta-numerica/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/advances-in-applied-probability/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/annals-of-actuarial-science/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/combinatorics-probability-and-computing/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/compositio-mathematica/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/ergodic-theory-and-dynamical-systems/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/european-journal-of-applied-mathematics/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/forum-of-mathematics-pi/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/development-and-psychopathology/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/industrial-and-organizational-psychology/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/american-journal-of-international-law/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/asian-journal-of-international-law/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/asian-journal-of-law-and-society/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/cambridge-law-journal/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/cambridge-yearbook-of-european-legal-studies/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/canadian-journal-of-law-and-jurisprudence/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/ecclesiastical-law-journal/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/european-constitutional-law-review/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/european-law-open/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/german-law-journal/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/international-and-comparative-law-quarterly/information/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/agricultural-and-resource-economics-review/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/animal-health-research-reviews/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/disaster-medicine-and-public-health-preparedness/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/social-science-history/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/medical-history/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/austrian-history-yearbook/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-chinese-history/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/modern-intellectual-history/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-global-history/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/modern-american-history/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/studies-in-church-history/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-policy-history/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-applied-probability#/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-the-institute-of-mathematics-of-jussieu/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/mathematical-proceedings-of-the-cambridge-philosophical-society/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/nagoya-mathematical-journal/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/numerical-mathematics-theory-methods-and-applications/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/proceedings-of-the-royal-society-of-edinburgh-section-a-mathematics/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/international-journal-of-law-in-context/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/international-review-of-the-red-cross/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-african-law/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-law-and-religion/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/legal-theory/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/leiden-journal-of-international-law/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/econometric-theory/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/canadian-yearbook-of-international-law-annuaire-canadien-de-droit-international/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/transnational-environmental-law/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/world-trade-review/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-agricultural-and-applied-economics/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-demographic-economics/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-institutional-economics/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-pension-economics-and-finance/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/macroeconomic-dynamics/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-the-international-neuropsychological-society/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/psychological-medicine/information/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/spanish-journal-of-psychology/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-plasma-physics/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/quarterly-reviews-of-biophysics/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/international-psychogeriatrics/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/public-health-nutrition/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/experimental-agriculture/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/business-and-human-rights-journal/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/business-and-politics/information/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/business-ethics-quarterly/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-management-and-organization/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/american-political-science-review/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/management-and-organization-review/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/bird-conservation-international/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-agricultural-science/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-dairy-research/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-wine-economics/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/renewable-agriculture-and-food-systems/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/annals-of-glaciology/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/invasive-plant-science-and-management/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/parasitology/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/quantitative-plant-biology/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/twin-research-and-human-genetics/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/weed-science/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/weed-technology/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-glaciology/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-paleontology/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/earth-and-environmental-science-transactions-of-royal-society-of-edinburgh/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/paleobiology/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/behavioural-public-policy/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/british-journal-of-political-science/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/canadian-journal-of-political-science-revue-canadienne-de-science-politique/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/european-political-science-review/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-experimental-political-science/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-race-ethnicity-and-politics/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/perspectives-on-politics/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/political-analysis/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/political-science-research-and-methods/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/politics-and-gender#/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/ps-political-science-and-politics/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/review-of-international-studies/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/review-of-politics/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/theory-and-practice-of-logic-programming/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/dance-research-journal/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/early-music-history/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/eighteenth-century-music/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-the-royal-musical-association/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-the-society-for-american-music/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/new-theatre-quarterly/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/nineteenth-century-music-review/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/plainsong-and-medieval-music/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/popular-music/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/theatre-research-international/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/theatre-survey/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/twentieth-century-music/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/australasian-journal-of-special-and-inclusive-education/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/australian-journal-of-environmental-education/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/british-journal-of-music-education/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/annual-review-of-applied-linguistics/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/applied-psycholinguistics/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/canadian-journal-of-linguistics-revue-canadienne-de-linguistique/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/english-language-and-linguistics/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-germanic-linguistics/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/journal-of-linguistics/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/language-in-society/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/language-variation-and-change/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/nordic-journal-of-linguistics/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/phonology/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/language-teaching/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/experimental-results/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/latin-american-research-review/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/personality-neuroscience/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/visual-neuroscience/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/environmental-conservation/information/about-this-journal/editorial-board',
        'https://www.cambridge.org/core/journals/global-sustainability/information/about-this-journal/editorial-board',
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
