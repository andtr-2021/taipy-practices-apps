import os
import time
import selenium.webdriver as webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
import pandas as pd

urls = [
    'https://www.tradingview.com/markets/stocks-usa/highs-and-lows-ath/',
    'https://www.tradingview.com/markets/stocks-usa/highs-and-lows-atl/',
    'https://www.tradingview.com/markets/stocks-usa/highs-and-lows-52wk-high/',
    'https://www.tradingview.com/markets/stocks-usa/highs-and-lows-52wk-low/',
    'https://www.tradingview.com/markets/stocks-usa/highs-and-lows-monthly-high/',
    'https://www.tradingview.com/markets/stocks-usa/highs-and-lows-monthly-low/',
    'https://www.tradingview.com/markets/stocks-usa/highs-and-lows-high-dividend/'
]

## Setup chrome options
chrome_options = Options()
chrome_options.add_argument("--headless") # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")

# Set path to chrome/chromedriver as per your configuration
driverdir = os.path.expanduser("~") + "/selenium_driver"
chrome_options.binary_location = f"{driverdir}/chrome-linux64/chrome"
webdriver_service = Service(f"{driverdir}/chromedriver-linux64/chromedriver")

browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)

browser.implicitly_wait(7)
browser.maximize_window()

for url in urls:
    browser.get(url)
    file_base_name = url.split('/')[-2]

    # iterate categories
    categories = browser.find_elements(By.XPATH, '//div[starts-with(@class, "item-EE_m_Lmj")]')

    for category in categories:
        print(f'Processing Report: {category.text}')
        try:
            # click on Overview tab
            try:
                browser.find_element(By.XPATH, f'//div[text()="{category.text}"]').click()            
            except ElementNotInteractableException:
                pass
                        
            # click on load more buttons until disappears
            load_more = True
            counter = 0
            max_counter = 3
            
            while load_more:
                try:
                    browser.find_element(By.CLASS_NAME, 'tv-load-more__btn').click()
                    time.sleep(1)
                    if counter > max_counter:
                        load_more = False
                    counter += 1
                except ElementNotInteractableException:
                    load_more = False

            # Check if there are tables in the page source
            tables = pd.read_html(browser.page_source)
            if len(tables) > 1:
                df = tables[1]
                df.replace('—', '', inplace=True)
                # Save the dataframe as a CSV file
                csv_file_name = f"{file_base_name}_{category.text}.csv"
                df.to_csv(csv_file_name, index=False)
                print(f'CSV file saved at {csv_file_name}')
            else:
                print(f"No tables found for category: {category.text}")

        except (NoSuchElementException, TimeoutException):
            print(f'Report {category.text} is not found.')
            continue
    
browser.quit()
