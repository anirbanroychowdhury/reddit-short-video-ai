from selenium import webdriver
import pandas as pd


url = "https://www.google.com"

driver = webdriver.Chrome()

driver.get(url)

# Wait for the page to load completely
driver.implicitly_wait(10)  # waits for 10 seconds

# Take a screenshot
driver.save_screenshot("screenshot.png")

# Close the browser
driver.quit()
