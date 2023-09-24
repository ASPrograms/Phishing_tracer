import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from PIL import Image
from js import document

def compareWebsites() :
    def compare_website_screenshot():

        # Load the captured screenshots as images
        img1 = cv2.imread("screenshot1.png")
        img2 = cv2.imread("screenshot2.png")

        # Convert images to grayscale
        img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # Calculate histograms and normalize them
        hist1 = cv2.calcHist([img1_gray], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([img2_gray], [0], None, [256], [0, 256])
        cv2.normalize(hist1, hist1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
        cv2.normalize(hist2, hist2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

        # Compare histograms using correlation method
        correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

        return correlation

    def open_sites_and_capture_screenshots() :
        # Initialize a Selenium webdriver (you need to have the appropriate webdriver installed, e.g., ChromeDriver)
        driver = webdriver.Chrome()

        url1 = document.querySelector("#url1")
        url2 = document.querySelector("#url2")

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


    similarity_score = open_sites_and_capture_screenshots()
    similarity_score = compare_website_screenshot()
    print("\n"*20 + f'The similarity score between both websites is {int(similarity_score*100)}%.')
    output_div = document.querySelector("#output")
    output_div.innerText =  f'The similarity score between both websites is {int(similarity_score*100)}%.'