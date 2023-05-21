#/urs/bin/env python3
import requests
from urllib.parse import urlparse
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

ad_attributes = [
    'data-ad-slot',
    'data-ad-client',
    'data-ad-format',
    'data-ad-type',
    'data-ad-unit',
    'data-google-query-id',
    'data-page-url',
    'data-ad-width',
    'data-ad-height'
]

url=sys.argv[1]

options = webdriver.ChromeOptions()
options.add_extension("I-don-t-care-about-cookies.crx")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get(url)
wait = WebDriverWait(driver, 10)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '*')))

current_domain = urlparse(driver.current_url).netloc

time.sleep(4)
  

elements = driver.find_elements(By.CSS_SELECTOR, 'img')
for i, el in enumerate(elements):
  try:
    el.screenshot(f'{i}screenshot.png')
  except:
    pass
  # try:
  #     el.screenshot(f'{i}_screenshot.png')    
  # except:
  #     pass

    
# soup = BeautifulSoup(driver.page_source, 'html.parser')

# elements = soup.css.select(".adsbygoogle")



driver.quit()


