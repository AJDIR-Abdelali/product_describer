import argparse
import json
import os
from datetime import datetime
from ingest_products import get_products, save_products_as_json, save_products_as_txt
from describer import call_model, load_products, generate_product_description

def save_output(results, mode="describe", category_filter=None):
    """Save the processed results to file."""
    os.makedirs("data/descriptions", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    
    # Add category to filename if filtered
    category_suffix = f"_{category_filter}" if category_filter else ""
    
    # Save as JSON
    json_filename = f"data/descriptions/pipeline_results_{mode}{category_suffix}_{timestamp}.json"
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Save as readable text
    txt_filename = f"data/descriptions/pipeline_results_{mode}{category_suffix}_{timestamp}.txt"
    with open(txt_filename, 'w', encoding='utf-8') as f:
        for i, result in enumerate(results, 1):
            product = result['product']
            f.write(f"PRODUCT {i}:\n")
            f.write(f"Title: {product['title']}\n")
            f.write(f"Category: {product.get('category', 'N/A')}\n")
            f.write(f"Price: ${product.get('price', 'N/A')}\n")
            f.write(f"Rating: {product.get('rating', 'N/A')}★\n")
            f.write(f"Original Description: {product.get('description', 'N/A')}\n")
            f.write(f"Generated Description: {result['output']}\n")
            f.write("=" * 60 + "\n")
    
    # Save as HTML for bonus styling
    html_filename = f"data/descriptions/pipeline_results_{mode}{category_suffix}_{timestamp}.html"
    save_as_html(results, html_filename)
    
    print(f"Results saved to {json_filename}, {txt_filename}, and {html_filename}")

def save_as_html(results, filename):
    """Save results as styled HTML file."""
def save_as_html(results, filename):
    """Save results as horizontally scrollable cards in HTML."""
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AI-Generated Product Descriptions</title>
  <style>
    body {
      background-color: #CBD9E6;
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 20px;
    }

    h1 {
      text-align: center;
      color: #2F4156;
      padding-bottom: 20px;
      border-bottom: 2px solid #2F4156;
    }

    h2 {
      color: #2F4156;
      margin-top: 40px;
      margin-left: 10px;
      border-bottom: 1px solid #2F4156;
      padding-bottom: 5px;
    }

    .scroll-container {
      display: flex;
      overflow-x: hidden;
      gap: 20px;
      padding: 20px 0;
    }

    .product-card {
      flex: 0 0 600px;
      display: flex;
      flex-direction: row;
      background-color: #F5EFEB;
      border-radius: 10px;
      padding: 20px;
      min-height: 300px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
      transition: transform 0.2s ease;
    }

    .product-card:hover {
      transform: translateY(-5px);
    }

    .left-column {
      flex: 1;
      margin-right: 20px;
    }

    .right-column {
      flex: 2;
    }

    .product-title {
      font-size: 20px;
      font-weight: bold;
      margin-bottom: 10px;
      color: #333;
    }

    .badges {
      display: flex;
      gap: 10px;
      margin-bottom: 15px;
    }

    .badge {
      background-color: #007bff;
      color: white;
      padding: 4px 10px;
      border-radius: 5px;
      font-size: 0.9em;
    }

    .price {
      color: #e74c3c;
      font-weight: bold;
    }

    .rating {
      color: #f39c12;
    }

    .section {
      margin-bottom: 10px;
    }

    .section-title {
      font-weight: bold;
      margin-bottom: 5px;
    }

    .original {
      background-color: #D2DCE4;
      padding: 10px;
      border-radius: 5px;
      font-style: italic;
    }

    .generated {
      background-color: #BFBFBF;
      padding: 10px;
      border-radius: 5px;
    }

  </style>
</head>
<body>
  <h1>AI-Generated Product Descriptions</h1>
"""

    # Regroupement par catégorie
    categories = {}
    for result in results:
        category = result['product'].get('category', 'Uncategorized')
        if category not in categories:
            categories[category] = []
        categories[category].append(result)

    for category, products in categories.items():
        html_content += f"<h2>{category.title()}</h2>"
        html_content += '<div class="scroll-container">'
        for result in products:
            product = result["product"]
            html_content += f"""
            
    <div class="product-card">
      <div class="left-column">
        <div class="product-title">{product['title']}</div>
        <div class="badges">
          <span class="badge">{product.get('category', 'N/A')}</span>
          <span class="price">${product.get('price', 'N/A')}</span>
          <span class="rating">{product.get('rating', 'N/A')}★</span>
        </div>
      </div>
      <div class="right-column">
        <div class="section">
          <div class="section-title">Original Description:</div>
          <div class="original">{product.get('description', 'N/A')}</div>
        </div>
        <div class="section">
          <div class="section-title">AI-Generated Description:</div>
          <div class="generated">{result['output']}</div>
        </div>
      </div>
    </div>
"""
        html_content += '</div>'  # end of scroll-container

    html_content += """
</body>
</html>
"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

def transform_data(products, mode="describe", use_real_model=False):
    """Transform products using describer with specified mode."""
    results = []
    
    for product in products:
        # Customize prompt based on mode
        if mode == "describe":
            description = generate_product_description(product, use_real_model)
        elif mode == "summarize":
            title = product.get('title', 'Unknown Product')
            prompt = f"Write a one-sentence summary for the product '{title}'"
            description = call_model(prompt, use_real_model)
        else:
            prompt = f"{mode} this product: {product.get('title', 'Unknown Product')}"
            description = call_model(prompt, use_real_model)
        
        results.append({
            'product': product,
            'output': description,
            'mode': mode
        })
    
    return results

def run_pipeline(skip_ingest=False, mode="describe", use_real_model=False, category_filter=None):
    """Run the complete pipeline."""
    print(f"Starting pipeline with mode: {mode}")
    if category_filter:
        print(f"Filtering for category: {category_filter}")
    
    # Step 1: Ingest data (unless skipped)
    if not skip_ingest:
        print("Step 1: Ingesting new product data...")
        products_data = get_products(10)
        save_products_as_json(products_data)
        save_products_as_txt(products_data)
        print("Data ingestion complete.")
    else:
        print("Step 1: Skipping data ingestion (using existing data)")
    
    # Step 2: Load products
    print("Step 2: Loading products...")
    products = load_products()
    
    if not products:
        print("Error: No products found. Please run without --skip-ingest first.")
        return
    
    # Filter by category if specified
    if category_filter:
        products = [p for p in products if p.get('category', '').lower() == category_filter.lower()]
        print(f"Filtered to {len(products)} products in category '{category_filter}'")
        
        if not products:
            print(f"No products found in category '{category_filter}'")
            return
    
    # Step 3: Transform data using describer
    print("Step 3: Generating descriptions...")
    results = transform_data(products, mode=mode, use_real_model=use_real_model)
    print(f"Processed {len(results)} products")
    
    # Step 4: Save the output
    print("Step 4: Saving output...")
    save_output(results, mode, category_filter)
    
    print("Pipeline complete!")
    
    # Print sample results
    print("\nSample results:")
    for i, result in enumerate(results[:3]):  # Show first 3
        product = result['product']
        print(f"\nProduct {i+1}: {product['title']}")
        print(f"Category: {product.get('category', 'N/A')}")
        print(f"Price: ${product.get('price', 'N/A')}")
        print(f"Generated: {result['output'][:100]}...")

def main():
    parser = argparse.ArgumentParser(description="Run the product description generation pipeline")
    
    parser.add_argument(
        "--skip-ingest", 
        action="store_true",
        help="Skip downloading new data, reuse the most recent raw file"
    )
    
    parser.add_argument(
        "--mode",
        type=str,
        default="describe",
        help='Customize the prompt mode (e.g., "describe", "summarize")'
    )

    parser.add_argument(
        "--real-model",
        action="store_true",
        help="Use the real Cohere model instead of simulation"
    )
    
    parser.add_argument(
        "--category",
        type=str,
        help="Only generate descriptions for products of a specific category (e.g., 'laptops')"
    )

    args = parser.parse_args()

    run_pipeline(
        skip_ingest=args.skip_ingest, 
        mode=args.mode, 
        use_real_model=args.real_model,
        category_filter=args.category
    )

if __name__ == "__main__":
    main()