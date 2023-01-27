import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

url = "https://quotes.toscrape.com/"

driver = webdriver.Chrome()
driver.get(url)

scraped_data = []

while (True):
    quotes = driver.find_elements(By.XPATH, "//div[@class='quote']")
    for i in range(len(quotes)):
        quote = quotes[i].find_element(By.CLASS_NAME, 'text').text
        author = quotes[i].find_element(By.CLASS_NAME, 'author').text
        temp_tags = quotes[i].find_elements(By.CLASS_NAME, 'tag')
        tags = {}
        for j in temp_tags:
            tags[j.text] = j.get_attribute('href')
        scrap = {
            'Author': author,
            'Quote': quote,
            'Tags': tags
        }
        scraped_data.append(scrap)
    try:
        nexButton = driver.find_element(By.XPATH,"//li[@class='next']/a")
        nexButton.click()
    except:
        driver.quit()
        break

df = pd.DataFrame(scraped_data)
df.sort_values(by=['Author'], inplace=True)
df.reset_index(drop=True, inplace=True)
df.to_csv('QuotesToScrapUsingSelenium.csv', encoding='utf-8-sig', index=False)
time.sleep(3)
driver.quit()