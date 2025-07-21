import requests
import os
import json
from datetime import datetime

def get_products(limit=10):
    """Fetch products from DummyJSON API."""
    products = []
    try:
        response = requests.get(f"https://dummyjson.com/products?limit={limit}")
        response.raise_for_status()
        data = response.json()
        products = data['products']
        print(f"Successfully fetched {len(products)} products")
    except requests.RequestException as e:
        print(f"Error fetching products: {e}")
    
    return products

def save_products_as_json(products):
    """Save products to JSON file."""
    if not products:
        print("No data to save.")
        return

    os.makedirs("data/raw", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"data/raw/products_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    print(f"{len(products)} products saved to {filename}")

def save_products_as_txt(products):
    """Save products to readable text file."""
    if not products:
        print("No data to save.")
        return

    os.makedirs("data/raw", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"data/raw/products_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        for i, product in enumerate(products, 1):
            f.write(f"Product {i}:\n")
            f.write(f"ID: {product['id']}\n")
            f.write(f"Title: {product['title']}\n")
            f.write(f"Category: {product['category']}\n")
            f.write(f"Price: ${product['price']}\n")
            f.write(f"Rating: {product.get('rating', 'N/A')}\n")
            f.write(f"Brand: {product.get('brand', 'N/A')}\n")
            f.write(f"Description: {product.get('description', 'N/A')}\n")
            f.write(f"Stock: {product.get('stock', 'N/A')}\n")
            f.write("-" * 60 + "\n")

    print(f"{len(products)} products saved to {filename}")

if __name__ == '__main__':
    products_data = get_products(10)
    save_products_as_json(products_data)
    save_products_as_txt(products_data)