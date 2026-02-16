import csv
import os
import re
import unicodedata

# Configuration
SOURCE_CSV = '/Users/paulomagrani/Downloads/catalog_products WIX 2025 - Página5.csv'
TARGET_DIR = '/Users/paulomagrani/Desktop/wix-18k-fev26/wix-Fev26/18k GOLD Plated'
OUTPUT_CSV = '/Users/paulomagrani/Desktop/wix-18k-fev26/Wix_Import_FINAL_READY.csv'
BASE_URL = 'https://wix-18k-fev26.pages.dev/18k%20GOLD%20Plated'

# Wix CSV Headers (Standard)
WIX_HEADERS = [
    'handleId', 'fieldType', 'name', 'description', 'productImageUrl', 'collection', 'sku', 'ribbon', 
    'price', 'surcharge', 'visible', 'discountMode', 'discountValue', 'inventory', 'weight', 'cost'
]

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    if not isinstance(value, str):
        return ""
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)

def get_images_for_ref(ref_num):
    """Finds all images in TARGET_DIR that match REF-{ref_num}"""
    prefix = f"REF-{ref_num:02d}_"
    images = []
    # Sort to ensure _1, _2, _3 order
    param_files = sorted(os.listdir(TARGET_DIR))
    for f in param_files:
        if f.startswith(prefix) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            images.append(f)
    return images

def main():
    print(f"Reading from: {SOURCE_CSV}")
    print(f"Scanning images in: {TARGET_DIR}")

    products = []

    with open(SOURCE_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader) # Skip header

        for row_idx, row in enumerate(reader, start=2):
            if not row or not row[0].strip():
                continue # Skip empty rows

            # Parse CSV Columns (Based on inspection)
            # Col 0: Title
            # Col 1: Foto X
            # Col 2: Description
            # Col 4: Quantity (Inventory)
            # Col 5: Price
            
            title = row[0].strip()
            photo_ref_str = row[1].strip()
            description = row[2].strip()
            quantity = row[4].strip() if len(row) > 4 else "0"
            price_str = row[5].strip().replace('"','').replace(',','.') if len(row) > 5 else "0"

            # Parse Ref Number
            match = re.search(r'Foto\s*(\d+)', photo_ref_str, re.IGNORECASE)
            if not match:
                print(f"Skipping row {row_idx}: No 'Foto X' found in '{photo_ref_str}'")
                continue
            
            ref_num = int(match.group(1))
            
            # Find Images
            images = get_images_for_ref(ref_num)
            if not images:
                print(f"Warning: No images found for {photo_ref_str} (Row {row_idx})")
                product_image_urls = ""
            else:
                # Construct URLs
                # encoded filename is handled by browser/wix usually, but spaces should be %20 if any?
                # Our filenames have no spaces (slugified), so straight append is safe.
                urls = [f"{BASE_URL}/{img}" for img in images]
                product_image_urls = ";".join(urls) # Wix uses semi-colon for multiple images

            # Build Wix Data
            handle_id = slugify(title)
            # SKU: GOLD-{ref_num}
            sku = f"GOLD-{ref_num:02d}"
            
            # Price cleaning
            try:
                price = float(price_str)
            except ValueError:
                price = 0.0

            # Inventory cleaning
            try:
                inventory_count = int(quantity) if quantity else 0
                inventory_status = "InStock" if inventory_count > 0 else "OutOfStock"
            except:
                inventory_status = "InStock" # Default

            product = {
                'handleId': handle_id,
                'fieldType': 'Product',
                'name': title,
                'description': description,
                'productImageUrl': product_image_urls,
                'collection': '18k GOLD Plated',
                'sku': sku,
                'ribbon': '',
                'price': price,
                'surcharge': 0,
                'visible': 'FALSE', # REQUESTED: FALSE
                'discountMode': 'PERCENT',
                'discountValue': 0,
                'inventory': inventory_status, # Wix import uses "InStock"/"OutOfStock" or numbers? 
                                             # Usually 'inventory' col is for tracking strategy, 'quantity' for count.
                                             # But based on user example line: "InStock" was present in one col?
                                             # User example cols: ...inventory,weight,cost...
                                             # User Data: "InStock"
                                             # Let's use "InStock" string.
                'weight': 0,
                'cost': 0,
                'productOptionName1': '',
                'productOptionType1': '',
                'productOptionDescription1': '',
            }
            products.append(product)

    # Write CSV
    print(f"Writing {len(products)} products to {OUTPUT_CSV}")
    with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=WIX_HEADERS, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(products)

    print("Done!")

if __name__ == "__main__":
    main()
