import requests
import os
import json
from datetime import datetime

def get_products(n=10):
    products = []
    for i in range(n):
        try:
            response = requests.get("https://dummyjson.com/products")
            response.raise_for_status()
            data = response.json()
            products.append(data)
        except requests.RequestException as e:
            print(f"Error fetching product {i + 1}: {e}")
    return products

def save_products(products):
    if not products:
        print("No data to save.")
        return

    os.makedirs("data/raw", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M")
    filename = f"data/raw/products_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(products, f, indent=4)

    if os.path.getsize(filename) > 0:
        print(f"Ingestion successful: {len(products)} products saved.")
    else:
        print("File was created but is empty.")
    

if __name__ == '__main__':
    products_data = get_products(10)
    save_products(products_data)
