from selenium import webdriver
from PIL import Image

# URLs of the two websites
url1 = 'https://asprograms.github.io'
url2 = 'https://asprograms.great-site.net'

# Initialize a Selenium webdriver (you need to have the appropriate webdriver installed, e.g., ChromeDriver)
driver = webdriver.Chrome()

# Function to capture screenshot and save it
def capture_and_save_screenshot(url, filename):
    driver.get(url)
    driver.save_screenshot(filename)

# Capture and save screenshot for the first website
capture_and_save_screenshot(url1, 'screenshot1.png')

# Capture and save screenshot for the second website
capture_and_save_screenshot(url2, 'screenshot2.png')

# Close the webdriver
driver.quit()

print("Screenshots captured and saved as 'screenshot1.png' and 'screenshot2.png'")
