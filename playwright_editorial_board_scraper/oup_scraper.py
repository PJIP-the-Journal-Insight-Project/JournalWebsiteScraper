import random
import time
import csv
import re 
from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent  
from bs4 import BeautifulSoup 

# Function to simulate human-like delays
def random_delay(min_delay, max_delay):
    time.sleep(random.uniform(min_delay, max_delay))

def remove_emails(text):
    # Regex to match and remove email addresses
    return re.sub(r'\S+@\S+', '', text)

def scrape_website(url):
    # Initialize a random user agent
    ua = UserAgent()
    user_agent = ua.random

    with sync_playwright() as p:
        # Launch the browser in non-headless mode
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent=user_agent,  # Rotate user-agent
            viewport={"width": 1024, "height": 1366},  # Set a realistic viewport size
        )
        page = context.new_page()

        try:
            # Navigate to the target website
            page.goto(url)
            random_delay(6, 22)  # Random delay after page load

            # Simulate human-like mouse movements
            page.mouse.move(random.uniform(150, 700), random.uniform(160, 1000))
            page.mouse.click(random.uniform(200, 600), random.uniform(120, 850))

            # Random delay before interacting with elements
            random_delay(7, 14)

            # Extract content from the div with class "secondaryContent"
            content_locator = page.locator("div.secondaryContent")
            if content_locator.count() > 0:
                raw_html = content_locator.inner_html()
            else:
                raw_html = "No content found in div.secondaryContent"

            # Use BeautifulSoup to parse the HTML and filter the required tags
            soup = BeautifulSoup(raw_html, "html.parser")

            # Find all <p>, <h2>, <h3>, and <h4> tags
            filtered_tags = soup.find_all(['p', 'h2', 'h3', 'h4'])

            # Initialize an empty string to store the final scraped data
            cleaned_data = []

            for tag in filtered_tags:
                if tag.name == 'p':
                    # Remove content after <br> tag in <p> tags
                    br_tag = tag.find('br')
                    if br_tag:
                        # Get everything before the <br> tag
                        tag_content_before_br = ''.join(str(t) for t in tag.contents[:tag.contents.index(br_tag)])
                        text = ' '.join(BeautifulSoup(tag_content_before_br, 'html.parser').stripped_strings)
                    else:
                        text = ' '.join(tag.stripped_strings)

                elif tag.name in ['h2', 'h3', 'h4']:
                    text = tag.get_text().strip()

                # Remove any email addresses
                text = remove_emails(text)

                # Replace <p> with a dash, and <h2>, <h3>, <h4> with a colon
                if tag.name == 'p':
                    cleaned_data.append(f"- {text}")
                else:
                    cleaned_data.append(f"{text}:")

            # Join all the cleaned content into a single string
            final_data = "\n".join(cleaned_data)
            print(f"Scraped Data from {url}: {final_data[:500]}...")  # Print first 500 chars for readability
            return final_data

        except Exception as e:
            print(f"Error during scraping {url}:", e)
            return None
        finally:
            browser.close()

def save_to_csv(url, data, filename="output.csv"):
    # Save the URL and scraped data to a CSV file
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([url, data])  # Write URL and data as a row

if __name__ == "__main__":
    urls = [

        # these are the urls of oxford university press journals that were indexed in the PJIP as of Feb 2025
      
        'https://academic.oup.com/restud/pages/Editorial_Board',
        'https://academic.oup.com/wber/pages/Editorial_Board',
        'https://academic.oup.com/jpepsy/pages/Editorial_Board',
        'https://academic.oup.com/jrr/pages/Editorial_Board',
        'https://academic.oup.com/mnras/pages/Editorial_Board',
        'https://academic.oup.com/mnrasl/pages/Editorial_Board',
        'https://academic.oup.com/ptep/pages/Editorial_Board',
        'https://academic.oup.com/jncics/pages/Editorial_Board',
        'https://academic.oup.com/jid/pages/Editorial_Board',
        'https://academic.oup.com/jnen/pages/Editorial_Board',
        'https://academic.oup.com/bioinformaticsadvances/pages/Editorial_Board',
        'https://academic.oup.com/jpubhealth/pages/Editorial_Board',
        'https://academic.oup.com/jpids/pages/Editorial_Board',
        'https://academic.oup.com/tropej/pages/Editorial_Board',
        'https://academic.oup.com/lifemeta/pages/Editorial_Board',
        'https://academic.oup.com/mrcr/pages/Editorial_Board',
        'https://academic.oup.com/narcancer/pages/Editorial_Board',
        'https://academic.oup.com/neuro-oncology/pages/Editorial_Board',
        'https://academic.oup.com/noa/pages/Editorial_Board',
        'https://academic.oup.com/nop/pages/Editorial_Board',
        'https://academic.oup.com/occmed/pages/Editorial_Board',
        'https://academic.oup.com/ofid/pages/Editorial_Board',
        'https://academic.oup.com/ooim/pages/Editorial_Board',
        'https://academic.oup.com/ptj/pages/Editorial_Board',
        'https://academic.oup.com/phe/pages/Editorial_Board',
        'https://academic.oup.com/rheumatology/pages/Editorial_Board',
        'https://academic.oup.com/rheumap/pages/Editorial_Board',
        'https://academic.oup.com/biomedgerontology/pages/Editorial_Board',
        'https://academic.oup.com/toxres/pages/Editorial_Board',
        'https://academic.oup.com/trstmh/pages/Editorial_Board',
        'https://academic.oup.com/ndt/pages/Editorial_Board',
        'https://academic.oup.com/jscr/pages/Editorial_Board',
        'https://academic.oup.com/asj/pages/Editorial_Board',
        'https://academic.oup.com/jme/pages/Editorial_Board',
        'https://academic.oup.com/rcfs/pages/Editorial_Board',
        'https://academic.oup.com/rof/pages/Editorial_Board',
        'https://academic.oup.com/forestscience/pages/Editorial_Board',
        'https://academic.oup.com/forestry/pages/Editorial_Board',
        'https://academic.oup.com/biomethods/pages/Editorial_Board',
        'https://academic.oup.com/bib/pages/Editorial_Board',
        'https://academic.oup.com/cz/pages/Editorial_Board',
        'https://academic.oup.com/ee/pages/Editorial_Board',
        'https://academic.oup.com/eep/pages/Editorial_Board',
        'https://academic.oup.com/clinchem/pages/Editorial_Board',
        'https://academic.oup.com/jb/pages/Editorial_Board',
        'https://academic.oup.com/evlett/pages/Editorial_Board',
        'https://academic.oup.com/femsle/pages/Editorial_Board',
        'https://academic.oup.com/femsre/pages/Editorial_Board',
        'https://academic.oup.com/g3journal/pages/Editorial_Board',
        'https://academic.oup.com/gbe/pages/Editorial_Board',
        'https://academic.oup.com/hmg/pages/Editorial_Board',
        'https://academic.oup.com/isd/pages/Editorial_Board',
        'https://academic.oup.com/jas/pages/Editorial_Board',
        'https://academic.oup.com/jee/pages/Editorial_Board',
        'https://academic.oup.com/jxb/pages/Editorial_Board',
        'https://academic.oup.com/jinsectscience/pages/Editorial_Board',
        'https://academic.oup.com/jmammal/pages/Editorial_Board',
        'https://academic.oup.com/jmcb/pages/Editorial_Board',
        'https://academic.oup.com/mollus/pages/Editorial_Board',
        'https://academic.oup.com/mspecies/pages/Editorial_Board',
        'https://academic.oup.com/mbe/pages/Editorial_Board',
        'https://academic.oup.com/nargab/pages/Editorial_Board',
        'https://academic.oup.com/sysbio/pages/Editorial_Board',
        'https://academic.oup.com/tas/pages/Editorial_Board',
        'https://academic.oup.com/zoolinnean/pages/Editorial_Board',
        'https://academic.oup.com/petrology/pages/Editorial_Board',
        'https://academic.oup.com/joeg/pages/Editorial_Board',
        'https://academic.oup.com/cjip/pages/Editorial_Board',
        'https://academic.oup.com/fpa/pages/Editorial_Board',
        'https://academic.oup.com/isagsq/pages/Editorial_Board',
        'https://academic.oup.com/irap/pages/Editorial_Board',
        'https://academic.oup.com/isq/pages/Editorial_Board',
        'https://academic.oup.com/jogss/pages/Editorial_Board',
        'https://academic.oup.com/jpart/pages/Editorial_Board',
        'https://academic.oup.com/ppmg/pages/Editorial_Board',
        'https://academic.oup.com/spp/pages/Editorial_Board',
        'https://academic.oup.com/sp/pages/Editorial_Board',
        'https://academic.oup.com/ooms/pages/Editorial_Board',
        'https://academic.oup.com/rb/pages/Editorial_Board',
        'https://academic.oup.com/em/pages/Editorial_Board',
        'https://academic.oup.com/jdh/pages/Editorial_Board',
        'https://academic.oup.com/litthe/pages/Editorial_Board',
        'https://academic.oup.com/ml/pages/Editorial_Board',
        'https://academic.oup.com/mts/pages/Editorial_Board',
        'https://academic.oup.com/mq/pages/Editorial_Board',
        'https://academic.oup.com/her/pages/Editorial_Board',
        'https://academic.oup.com/jdsde/pages/Editorial_Board',
        'https://academic.oup.com/applij/pages/Editorial_Board',
        'https://academic.oup.com/ijl/pages/Editorial_Board',
        'https://academic.oup.com/jcmc/pages/Editorial_Board',
        'https://academic.oup.com/nsr/pages/Editorial_Board',
        'https://academic.oup.com/nc/pages/Editorial_Board',
        'https://academic.oup.com/scan/pages/Editorial_Board',
        'https://academic.oup.com/jpe/pages/Editorial_Board',
        'https://academic.oup.com/jue/pages/Editorial_Board',
    ]

    # Create or overwrite the CSV file with headers
    with open("output.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Scraped Data"])  # Write header row

    # Scrape each URL and save the results to the CSV file
    for url in urls:
        scraped_data = scrape_website(url)
        if scraped_data:
            save_to_csv(url, scraped_data)
