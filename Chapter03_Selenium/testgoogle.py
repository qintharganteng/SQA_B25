import time
from selenium import webdriver

driver = webdriver.Edge()
driver.get('https://google.co.id')
time.sleep(10)
driver.quit()