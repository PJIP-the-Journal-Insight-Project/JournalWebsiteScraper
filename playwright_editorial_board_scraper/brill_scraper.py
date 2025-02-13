import random
import time
import csv
import re
from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

def random_delay(min_delay, max_delay):
    time.sleep(random.uniform(min_delay, max_delay))

def remove_emails(text):
    return re.sub(r'\S+@\S+', '', text)

def scrape_website(url):
    ua = UserAgent()
    user_agent = ua.random

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent=user_agent,
            viewport={"width": 375, "height": 667},
        )
        page = context.new_page()

        try:
            page.goto(url)
            random_delay(7, 18)

            page.mouse.move(random.uniform(160, 700), random.uniform(160, 900))
            page.mouse.click(random.uniform(180, 500), random.uniform(180, 750))
            random_delay(7, 14)

            container_locator = page.locator("div#container-128947-item-128955, div[aria-labelledby='ui-id-2']")
            if container_locator.count() > 0:
                raw_html = container_locator.inner_html()
            else:
                raw_html = "No content found in specified container"

            soup = BeautifulSoup(raw_html, "html.parser")
            editorial_components = soup.find_all("div", class_="component component-content-item component-editorial-content")

            cleaned_data = []
            for component in editorial_components:
                content_boxes = component.find_all("div", class_="content-box-body")
                for box in content_boxes:
                    html_content = str(box)
                    html_content = remove_emails(html_content)
                    cleaned_data.append(html_content)

            final_data = "\n".join(cleaned_data)
            print(f"Scraped Data from {url}: {final_data[:500]}...")
            return final_data

        except Exception as e:
            print(f"Error during scraping {url}:", e)
            return None
        finally:
            browser.close()

def save_to_csv(url, data, filename="output.csv"):
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([url, data])

if __name__ == "__main__":
    urls = [

        # these are the urls of brill journals that were indexed in the PJIP as of Feb 2025
      
        'https://brill.com/view/journals/dyp/dyp-overview.xml',
        'https://brill.com/view/journals/gps/gps-overview.xml',
        'https://brill.com/view/journals/hpla/hpla-overview.xml',
        'https://brill.com/view/journals/skep/skep-overview.xml',
        'https://brill.com/view/journals/jpt/jpt-overview.xml',
        'https://brill.com/view/journals/jcph/jcph-overview.xml',
        'https://brill.com/view/journals/jmp/jmp-overview.xml',
        'https://brill.com/view/journals/jph/jph-overview.xml',
        'https://brill.com/view/journals/phro/phro-overview.xml',
        'https://brill.com/view/journals/agpt/agpt-overview.xml',
        'https://brill.com/view/journals/rip/rip-overview.xml',
        'https://brill.com/view/journals/sdbs/sdbs-overview.xml',
        'https://brill.com/view/journals/aeas/aeas-overview.xml',
        'https://brill.com/view/journals/tpao/tpao-overview.xml',
        'https://brill.com/view/journals/ruhi/ruhi-overview.xml',
        'https://brill.com/view/journals/nu/nu-overview.xml',
        'https://brill.com/view/journals/ajls/ajls-overview.xml',
        'https://brill.com/view/journals/cjel/cjel-overview.xml',
        'https://brill.com/view/journals/clla/clla-overview.xml',
        'https://brill.com/view/journals/eclr/eclr-overview.xml',
        'https://brill.com/view/journals/ejcl/ejcl-overview.xml',
        'https://brill.com/view/journals/gjcl/gjcl-overview.xml',
        'https://brill.com/view/journals/amre/amre-overview.xml',
        'https://brill.com/view/journals/jemh/jemh-overview.xml',
        'https://brill.com/view/journals/me/me-overview.xml',
        'https://brill.com/view/journals/jamh/jamh-overview.xml',
        'https://brill.com/view/journals/jcmh/jcmh-overview.xml',
        'https://brill.com/view/journals/ijmh/ijmh-overview.xml',
        'https://brill.com/view/journals/hcm/hcm-overview.xml',
        'https://brill.com/view/journals/joah/joah-overview.xml',
        'https://brill.com/view/journals/lega/lega-overview.xml',
        'https://brill.com/view/journals/lhs/lhs-overview.xml',
        'https://brill.com/view/journals/jeah/jeah-overview.xml',
        'https://brill.com/view/journals/jeh/jeh-overview.xml',
        'https://brill.com/view/journals/hrlr/hrlr-overview.xml',
        'https://brill.com/view/journals/ils/ils-overview.xml',
        'https://brill.com/view/journals/jeep/jeep-overview.xml',
        'https://brill.com/view/journals/ihls/ihls-overview.xml',
        'https://brill.com/view/journals/jlrs/jlrs-overview.xml',
        'https://brill.com/view/journals/lape/lape-overview.xml',
        'https://brill.com/view/journals/melg/melg-overview.xml',
        'https://brill.com/view/journals/iawa/iawa-overview.xml',
        'https://brill.com/view/journals/jaan/jaan-overview.xml',
        'https://brill.com/view/journals/ctoz/ctoz-overview.xml',
        'https://brill.com/view/journals/cr/cr-overview.xml',
        'https://brill.com/view/journals/ise/ise-overview.xml',
        'https://brill.com/view/journals/ijps/ijps-overview.xml',
        'https://brill.com/view/journals/nemy/nemy-overview.xml',
        'https://brill.com/view/journals/msr/msr-overview.xml',
        'https://brill.com/view/journals/grms/grms-overview.xml',
        'https://brill.com/view/journals/jal/jal-overview.xml',
        'https://brill.com/view/journals/jwl/jwl-overview.xml',
        'https://brill.com/view/journals/rart/rart-overview.xml',
        'https://brill.com/view/journals/apse/apse-overview.xml',
        'https://brill.com/view/journals/bire/bire-overview.xml',
        'https://brill.com/view/journals/vjep/vjep-overview.xml',
        'https://brill.com/view/journals/aall/aall-overview.xml',
        'https://brill.com/view/journals/jocp/jocp-overview.xml',
        'https://brill.com/view/journals/ieul/ieul-overview.xml',
        'https://brill.com/view/journals/irp/irp-overview.xml',
        'https://brill.com/view/journals/jgl/jgl-overview.xml',
        'https://brill.com/view/journals/ldc/ldc-overview.xml',
        'https://brill.com/view/journals/mjcc/mjcc-overview.xml',
        'https://brill.com/view/journals/jpp/jpp-overview.xml',
        'https://brill.com/view/journals/esm/esm-overview.xml',
    ]

    with open("output.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Scraped Data"])

    for url in urls:
        scraped_data = scrape_website(url)
        if scraped_data:
            save_to_csv(url, scraped_data)
