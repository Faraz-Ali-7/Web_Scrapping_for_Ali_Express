
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin

# Load the saved HTML file
with open("aliexpress_products.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Each product block
product_blocks = soup.find_all("div", class_="_2FypS")

products = []
for block in product_blocks:
    # Extract title
    title_tag = block.find("h3", class_="yB6en")
    title = title_tag.get_text(strip=True) if title_tag else "N/A"

    #Extract price
    price = ""
    price_div = block.find('div', class_='_3Mpbo')
    price_parts = price_div.find_all('span')
    for pr_comp in price_parts:
        price = price + pr_comp.get_text(strip=True)
    
    #Extract Rating
    rating_blk = block.find('span', class_='_2L2Tc')
    rating = rating_blk.get_text(strip=True) if rating_blk else 'N/A'

    #Extract Description
    link_tag = block.find("a", class_="_3mPKP")
    raw_link = link_tag["href"] if link_tag and link_tag.has_attr("href") else "N/A"
    link = urljoin("https://www.aliexpress.com", raw_link)
    products.append({
        "Title": title,
        "Price": price,
        "Rating": rating,
        "Link" : link, 
    })

# Save to Excel
df = pd.DataFrame(products)
df.to_excel("aliexpress_products.xlsx", index=False)
print("Done! Saved to aliexpress_products.xlsx")
