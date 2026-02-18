import os
import csv
import shutil
import re
from pathlib import Path
import unicodedata

# Configuration
SOURCE_ROOT = "/Users/paulomagrani/Downloads/Site_002"
DEST_DIR = "/Users/paulomagrani/Desktop/wix-18k-fev26/wix-Fev26/925 Silver"
CSV_PATH = os.path.join(SOURCE_ROOT, "catalog_products WIX 2025 - Parte2-SILVER.csv")
OUTPUT_CSV = "/Users/paulomagrani/Desktop/wix-18k-fev26/Wix_Import_SILVER_READY.csv"
BASE_URL = "https://wix-18k-fev26.pages.dev/925%20Silver/"

# Ensure destination exists
os.makedirs(DEST_DIR, exist_ok=True)

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    value = re.sub(r'[-\s]+', '-', value)
    return value

def parse_price(price_str):
    if not price_str:
        return 0
    # Handle "65,0" format
    price_str = price_str.replace('"', '').replace(',', '.').strip()
    try:
        return float(price_str)
    except ValueError:
        return 0

# Step 1: Load Data Map
product_map = {}
# Reading CSV without header
try:
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row: continue
            # Assuming format: Name, Foto Ref, Description, ..., Price
            # Row index might vary, let's look at the sample:
            # "Premium Fancy Yellow Earring", "Foto 39", "Desc...", "", "1", "65,0"

            if len(row) < 2: continue
            
            raw_ref = row[1] # "Foto 39"
            match = re.search(r'(\d+)', raw_ref)
            if match:
                ref_num = int(match.group(1))
                name = row[0].strip()
                desc = row[2].strip() if len(row) > 2 else ""
                
                price = 0
                # Specific index based on visual inspection of sample
                if len(row) > 5:
                    price = parse_price(row[5])
                
                product_map[ref_num] = {
                    "name": name,
                    "description": desc,
                    "price": price
                }

except Exception as e:
    print(f"Error reading CSV: {e}")

# Step 2: Traverse and Process
csv_rows = []
processed_count = 0

# Walk specific subfolders to find foto_XX
subfolders_to_scan = ["Fotos_039_049", "Fotos_050_059"]

for sub in subfolders_to_scan:
    path = os.path.join(SOURCE_ROOT, sub)
    if not os.path.exists(path):
        continue
        
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if not os.path.isdir(item_path):
            continue
            
        # Check if it is a foto folder
        # Expecting "foto_039" or similar
        match = re.search(r'foto_?0?(\d+)', item.lower())
        if not match:
            continue
            
        ref_num = int(match.group(1))
        
        # Get Product Data

        prod_data = product_map.get(ref_num, {
            "name": f"Product {ref_num}",
            "description": "",
            "price": 0
        })

        if not prod_data:
             print(f"Skipping {item} - No data found")
             continue
        
        # Prepare for images
        images = sorted([f for f in os.listdir(item_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))])
        
        product_image_urls = []
        
        for i, img_file in enumerate(images):
            seq = i + 1
            ext = os.path.splitext(img_file)[1].lower()
            if ext == '.jpeg': ext = '.jpg'
            
            safe_name = slugify(prod_data['name'])
            new_filename = f"REF-{ref_num}_{safe_name}_{seq}{ext}"
            
            src_file = os.path.join(item_path, img_file)
            dest_file = os.path.join(DEST_DIR, new_filename)
            
            try:
                shutil.move(src_file, dest_file)
            except Exception as e:
                print(f"Error moving {src_file}: {e}")
                continue
            
            final_url = f"{BASE_URL}{new_filename}"
            product_image_urls.append(final_url)

            
        if not product_image_urls:
            continue
            
        # Prepare CSV Row
        # Columns: handleId, fieldType, name, description, productImageUrl, collection, sku, price, visible
        # First row is Product, others are Variant/Image? 
        # Wix import usually takes multiple images in one cell separated by semicolon, or multiple rows.
        # "productImageUrl": "url1;url2;..."
        
        main_image = product_image_urls[0]
        other_images = ";".join(product_image_urls) # Wix often accepts semicolon separated
        
        # If we want to be safe, we can put all images in the productImageUrl field separated by ;
        
        handle_id = slugify(prod_data['name'])
        
        row = {
            "handleId": handle_id,
            "fieldType": "Product",
            "name": prod_data['name'],
            "description": prod_data['description'],
            "productImageUrl": other_images,
            "collection": "925 Silver; New Arrivals",
            "sku": f"REF-{ref_num:02d}",
            "price": prod_data['price'],
            "visible": "FALSE"
        }
        csv_rows.append(row)
        processed_count += 1

# Step 3: Write Output CSV
fieldnames = ["handleId", "fieldType", "name", "description", "productImageUrl", "collection", "sku", "price", "visible"]

with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(csv_rows)

print(f"✅ Processed {processed_count} products.")
