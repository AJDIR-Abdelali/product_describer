import os
import glob
import json
import cohere
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def call_model(prompt: str, use_real_model: bool = False) -> str:
    """Call model with option to use real LLM or simulation."""
    
    if not use_real_model:
        return f"[SIMULATED DESCRIPTION] {prompt}"
    
    # Check for API key
    api_key = os.getenv('COHERE_API_KEY')
    if not api_key:
        print("Warning: No COHERE_API_KEY found in environment. Falling back to simulation.")
        return f"[SIMULATED DESCRIPTION] {prompt}"
    
    try:
        # Initialize Cohere client
        co = cohere.Client(api_key)
        
        # Make API call
        response = co.generate(
            model='command-r-plus',
            prompt=prompt,
            max_tokens=300,
            temperature=0.7
        )
        
        return response.generations[0].text.strip()
        
    except Exception as e:
        print(f"Error calling Cohere API: {e}")
        print("Falling back to simulation...")
        return f"[SIMULATED DESCRIPTION] {prompt}"

def load_products():
    """Load products from data/raw/products_*.json files."""
    products = []
    
    # Find all product files
    product_files = glob.glob("data/raw/products_*.json")
    
    if not product_files:
        print("No product files found in data/raw/")
        return products
    
    # Use the most recent file
    latest_file = max(product_files, key=os.path.getctime)
    print(f"Loading products from: {latest_file}")
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    print(f"Loaded {len(products)} products")
    return products

def generate_product_description(product, use_real_model=False):
    """Generate a friendly, human-like description for a product."""
    title = product.get('title', 'Unknown Product')
    category = product.get('category', 'Unknown Category')
    price = product.get('price', 'Price not available')
    rating = product.get('rating', 'No rating')
    
    # Create prompt for description generation
    prompt = f"""Write a short product description for a {category} named {title} priced at ${price} with a {rating}★ rating.

Make the description friendly, engaging, and highlight key features that would appeal to customers. Keep it concise but compelling (2-3 sentences)."""
    
    # Get response from model
    description = call_model(prompt, use_real_model)
    
    return description

def process_products(use_real_model=False, category_filter=None):
    """Load products and generate descriptions for each."""
    products = load_products()
    results = []
    
    # Filter by category if specified
    if category_filter:
        products = [p for p in products if p.get('category', '').lower() == category_filter.lower()]
        print(f"Filtered to {len(products)} products in category '{category_filter}'")
    
    for product in products:
        # Generate description for each product
        description = generate_product_description(product, use_real_model)
        
        results.append({
            'product': product,
            'generated_description': description
        })
    
    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate product descriptions")
    parser.add_argument("--real-model", action="store_true", help="Use real Cohere model")
    parser.add_argument("--category", type=str, help="Filter products by category")
    args = parser.parse_args()

    results = process_products(use_real_model=args.real_model, category_filter=args.category)

    for result in results:
        product = result['product']
        print(f"Product: {product['title']}")
        print(f"Category: {product.get('category', 'N/A')}")
        print(f"Price: ${product.get('price', 'N/A')}")
        print(f"Generated Description: {result['generated_description']}")
        print("-" * 50)