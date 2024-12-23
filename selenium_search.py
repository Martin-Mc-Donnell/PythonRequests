from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

CHROMEDRIVER_PATH = "/opt/homebrew/bin/chromedriver"
SEARCH_URL = "https://www.humblebundle.com/games"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

def print_found_items(game_url):
    # Load webpage and allow time for JavaScript content to load
    driver.get(game_url)

    try:
        # Wait for the game titles to be present on the page
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.tier-item-view .item-details .item-title')))
        
        # Find the game titles
        game_elements = driver.find_elements(By.CSS_SELECTOR, '.tier-item-view .item-details .item-title')

        for game in game_elements:
            print(game.text.strip())  # Print the text of each game

    except Exception as e:
        print(f"Error fetching game titles from {game_url}: {e}")

def get_games_from_bundle():
    bundles = []

    try:
        # Load the main page and wait for the elements to be loaded on the page
        driver.get(SEARCH_URL)
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.full-tile-view.one-third.bundle[data-reload="1"]')))
        
        # Find the bundles on the page
        bundle_elements = driver.find_elements(By.CSS_SELECTOR, 'a.full-tile-view.one-third.bundle[data-reload="1"]')
        for element in bundle_elements:
            url = element.get_attribute("href")
            title = element.text.strip() or "No title available"
            bundles.append({"title": title, "url": url})

    except Exception as e:
        print(f"Error fetching bundles: {e}")

    # Print results
    for bundle in bundles:
        print(f"\n\nBundle Found: {bundle['title'].splitlines()[0]}")
        print(f"URL: {bundle['url']}\n")
        print_found_items(bundle['url'])

    # Close the WebDriver after all operations
    driver.quit()

if __name__ == "__main__":
    print("Fetching game names from the bundle...")
    get_games_from_bundle()
