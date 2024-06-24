from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Set up Chrome options
options = Options()
options.add_argument("--disable-notifications")  # Disable all notifications

# Initialize the browser
driver = webdriver.Chrome(options=options)

# Open Facebook and login
driver.get("https://www.pararius.nl/huurwoningen/zaandam/0-2000")
time.sleep(2)  # Wait for the page to load

# Wait for JavaScript to execute and the content to load
time.sleep(5)  # Adjust sleep time if necessary

# Get the page source after JavaScript execution
html_content = driver.page_source

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')