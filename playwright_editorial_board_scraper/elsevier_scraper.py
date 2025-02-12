import random
import time
import csv
from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent  # For generating random user agents

# Function to simulate human-like delays
def random_delay(min_delay, max_delay):
    time.sleep(random.uniform(min_delay, max_delay))

def scrape_website(url):
    # Initialize a random user agent
    ua = UserAgent()
    user_agent = ua.random

    with sync_playwright() as p:
        # Launch the browser in non-headless mode
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent=user_agent,  # Rotate user-agent
            viewport={"width": 412, "height": 915},  # Set a realistic viewport size
        )
        page = context.new_page()

        try:
            # Navigate to the target website
            page.goto(url)
            random_delay(4, 20)  # Random delay after page load

            # Simulate human-like mouse movements
            page.mouse.move(random.uniform(100, 600), random.uniform(100, 800))
            page.mouse.click(random.uniform(100, 800), random.uniform(100, 800))

            # Random delay before interacting with elements
            random_delay(5, 10)

            # Extract text from elements with the "js-editor-name" class
            scraped_data = page.evaluate("""() => {
                const elements = document.querySelectorAll('.js-editor-name');
                const texts = [];
                elements.forEach(element => {
                    texts.push(element.innerText.trim());
                });
                return texts.join(' - ');  // Join texts with a dash
            }""")

            print(f"Scraped Data from {url}: {scraped_data}")
            return scraped_data

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
        'https://www.sciencedirect.com/journal/annals-of-pure-and-applied-logic/pages/Editorial_Board',
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
