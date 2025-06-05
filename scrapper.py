import requests
from bs4 import BeautifulSoup
import csv
import json

base_url = "https://books.toscrape.com/"
response = requests.get(base_url)
soup = BeautifulSoup(response.text, "html.parser")

# Extract categories
categories = soup.select(".side_categories ul li ul li a")
category_data = []
for cat in categories:
    name = cat.text.strip()
    url = base_url + cat['href']
    category_data.append({"name": name, "url": url})

# Extract products from each category (example for one category)
products = []
for cat in category_data:
    cat_response = requests.get(cat['url'])
    cat_soup = BeautifulSoup(cat_response.text, "html.parser")
    product_list = cat_soup.select(".product_pod")
    for product in product_list:
        title = product.h3.a['title']
        price = product.select_one(".price_color").text
        img_url = base_url + product.img['src'].replace("../", "")
        products.append({
            "category": cat['name'],
            "title": title,
            "price": price,
            "image_url": img_url
        })

# Save as CSV
keys = products[1].keys()
with open('products.csv', 'w', newline='', encoding='utf-8') as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(products)

# Save as JSON
with open('products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, indent=2)
