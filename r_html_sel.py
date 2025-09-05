from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Setup Chrome options
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

# Setup driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Target URL
url = 'https://www.aliexpress.com/p/calp-plus/index.html?spm=a2g0o.home.allcategoriespc.11.39b46278PHBwOx&categoryTab=home_appliances'
driver.get(url)
time.sleep(5)  # allow page to load
last_height = 0
# Scroll to load more products
for i in range(350):  # increase this if you want more content
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print(i)
    time.sleep(3)  # wait for loading

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        print(f"No more content after {i+1} scrolls. Stopping.")
        break
    last_height = new_height

# Now get the updated page source
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# Save HTML locally
with open("aliexpress_products.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())

driver.quit()
print("Page loaded, scrolled, and saved successfully!")
