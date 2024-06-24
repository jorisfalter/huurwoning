from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Configure Selenium to use headless mode
options = Options()
options.headless = True
service = Service(executable_path='/path/to/chromedriver')  # Update the path to your ChromeDriver

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

# URL of the page to fetch
url = "https://www.pararius.nl/huurwoningen/zaandam/0-2000"

# Fetch the page
driver.get(url)

# Wait for JavaScript to execute and the content to load
time.sleep(5)  # Adjust sleep time if necessary

# Get the page source after JavaScript execution
html_content = driver.page_source

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Close the WebDriver
driver.quit()

# Find all list items with specific classes
class_list = ["search-list__item", "search-list__item--listing"]
class_selector = " ".join(["." + cls for cls in class_list])
list_items = soup.select(class_selector)

# Print the found list items
for item in list_items:
    print(item)
