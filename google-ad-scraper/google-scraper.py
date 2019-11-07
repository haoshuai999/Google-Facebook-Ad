import pandas as pd
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

def scrape(url):
	timeout = 20
	WINDOW_SIZE = "1920,1080"
	
	chrome_options = Options()  
	chrome_options.add_argument("--headless")  
	chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
	browser = webdriver.Chrome(chrome_options=chrome_options)

	browser.get(url)
	try:
		WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.TAG_NAME, "creative-preview")))
	except TimeoutException:
		print("Timed out waiting for page to load")
		browser.quit()

	# user_agent = "Chrome/78.0.3904.97"
	# headers = {'User-Agent': user_agent}

	# page_html_text = requests.get(url, headers=headers).text
	# page_html = fromstring(page_html_text)
	# print(page_html_text)
	ad_urls = browser.find_elements_by_css_selector("creative-preview > a")
	ad_link = [ad.get_attribute("href") for ad in ad_urls]
	ad_texts = browser.find_elements_by_css_selector("creative-preview mat-card")
	text = [ad.text for ad in ad_texts]

	result = {'Url':ad_link, 'Text':text}
	df = pd.DataFrame(result)

	now = datetime.now()
	date_time = now.strftime("%m-%d-%Y_%H-%M-%S")
	df.to_csv('google_ad_' + date_time + '.csv', index=False, encoding='utf-8')

	# print(ad_link)
	# print('\n')
	# print(text)
	# print('\n')
	browser.quit()

if __name__ == '__main__':
	starttime = time.time()
	google_url = "https://transparencyreport.google.com/political-ads/advertiser/AR105500339708362752?hl=en"
	while True:
		scrape(google_url)
		time.sleep(60.0 - ((time.time() - starttime) % 60.0))