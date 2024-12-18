from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

CHROMEDRIVER_PATH = "/opt/homebrew/bin/chromedriver"
SEARCH_URL = "https://www.humblebundle.com/games"

def print_found_items():
    # Set up Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Load webpage and allow time for JavaScript content to load
    driver.get(SEARCH_URL)
    time.sleep(5)

    # Find the <a> tags of the bundles
    bundle_elements = driver.find_elements(By.CSS_SELECTOR, 'a.full-tile-view.one-third.bundle[data-reload="1"]')

    bundles = []
    for element in bundle_elements:
        url = element.get_attribute("href")
        title = element.text.strip() or "No title available"  # Use text or fallback title
        bundles.append({"title": title, "url": url})

    # Close the WebDriver
    driver.quit()

    # Print results
    for bundle in bundles:
        print(f"Bundle Found: {bundle['title'].splitlines()[0]}")
        print(f"URL: {bundle['url']}\n")

if __name__ == "__main__":
    print("Checking for new bundles...")
    print_found_items()
