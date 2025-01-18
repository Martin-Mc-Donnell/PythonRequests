from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
import re

# Constants
CHROMEDRIVER_PATH = "/opt/homebrew/bin/chromedriver"
SEARCH_URL = "https://www.humblebundle.com/games"
JSON_FILE = "bundles.json"

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

def load_json_bundles():
    """Load bundles from the JSON file or create an empty one if it doesn't exist."""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            return json.load(f)
    return []

def save_json_bundles(bundles):
    """Save updated bundles to the JSON file."""
    with open(JSON_FILE, "w") as f:
        json.dump(bundles, f, indent=4)

def print_found_items(item_url):
    """Fetch and print items from a bundle's URL."""
    driver.get(item_url)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.tier-item-view .item-details .item-title')))
        item_elements = driver.find_elements(By.CSS_SELECTOR, '.tier-item-view .item-details .item-title')
        for item in item_elements:
            print(item.text.strip())
    except Exception as e:
        print(f"Error fetching items from {item_url}: {e}")

def get_bundles_from_website():
    """get bundles from the website."""
    bundles = []
    try:
        driver.get(SEARCH_URL)
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.full-tile-view.one-third.bundle[data-reload="1"]')))
        bundle_elements = driver.find_elements(By.CSS_SELECTOR, 'a.full-tile-view.one-third.bundle[data-reload="1"]')
        for element in bundle_elements:
            url = element.get_attribute("href")
            title = element.text.strip() or "No title available"

            cleaned_title = clean_title(title)

            bundles.append({"title": cleaned_title, "url": url})
    except Exception as e:
        print(f"Error fetching bundles: {e}")
    return bundles

def clean_title(title):
    """Remove unwanted text"""
    # Remove common countdown format like "7 DAYS LEFT" or "00:08:37:47"
    cleaned_title = re.sub(r'\d{1,2} (DAYS?|MONTHS?) LEFT|[\d\s:]{7,10}|\n', ' ', title).strip()
    return cleaned_title

def main():
    # Load existing bundles from the JSON file
    JSON_bundles = load_json_bundles()

    # Get bundles from the website
    current_bundles = get_bundles_from_website()

    # Clean up titles: Make comparison case-insensitive and strip extra spaces
    existing_titles = {bundle["title"].strip().lower() for bundle in JSON_bundles}

    # Find new bundles that aren't in the existing JSON_bundles
    new_bundles = []
    for bundle in current_bundles:
        clean_title = bundle["title"].strip().lower()
        if clean_title not in existing_titles:
            print(f"New bundle found: {bundle['title']}")  # Debugging line
            new_bundles.append(bundle)

    # Print results for each new bundle and its items
    if new_bundles:
        for bundle in new_bundles:
            print(f"\n\nNew Bundle Found: {bundle['title']}")
            print(f"URL: {bundle['url']}\n")
            print_found_items(bundle['url'])
    else:
        print("\nNo new bundles found.")

    # Add new bundles to JSON_bundles
    JSON_bundles.extend(new_bundles)

    # Remove bundles from JSON_bundles that no longer exist in current_bundles
    current_titles = {bundle["title"].strip().lower() for bundle in current_bundles}
    JSON_bundles = [bundle for bundle in JSON_bundles if bundle["title"].strip().lower() in current_titles]

    # Save the updated JSON_bundles back to the JSON file
    save_json_bundles(JSON_bundles)

    # Close the WebDriver after all operations
    driver.quit()

if __name__ == "__main__":
    main()
