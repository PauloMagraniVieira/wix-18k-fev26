import csv
import os
import shutil
import re

# Configuration
SOURCE_DIR = '/Users/paulomagrani/Desktop/Fotos_037_038_088_089'
TARGET_DIR = '/Users/paulomagrani/Desktop/wix-18k-fev26/wix-Fev26/18k GOLD Plated'
OUTPUT_CSV = '/Users/paulomagrani/Desktop/wix-18k-fev26/Wix_Import_FINAL_READY.csv'
BASE_URL = 'https://wix-18k-fev26.pages.dev/18k%20GOLD%20Plated'

# New Products Data (Manual Entry from Prompt)
NEW_PRODUCTS = [
    {
        'ref': 37,
        'title': 'Modern Grace Earring',
        'price': 100.0,
        'type': 'Earring',
        'desc_header': "Product Description :   *Designer : ✨ Contemporary and striking design.\n*Versatile and elegant neutral tone.\n*Ideal for sophisticated looks or refined everyday wear .\n*Dimensions : 0.98 x 0.78 inches \n*Material: Plated Gold 18k      \n*Stones: Porcelain\n",
        'collection_desc': "Jardim de Luz Collection\nA collection that expresses delicacy and sophistication in every detail. Inspired by the lightness of flowers and the softness of light, Jardim de Luz features jewelry in subtle pastel tones, with elegant designs created to illuminate the look with grace and understated beauty.",
        'material_desc': "*Material: Made of high quality brass base metal with your choice of luxurious 18k gold or rhodium plating for long lasting shine. It is highly durable and designed for everyday use. \n\n*Hypoallergenic: Nickel-free, making them gentle on sensitive skin.\n\n* Stones : As it is a 100% natural product, there may be variations in the colors and shape of the stones.\n* All parts are sold separately. \n\nJewelry with 6 months warranty bath and manufacturing defects.\nWe do not guarantee: Broken  stones or cracked due to misuse, scratches, stains characterized by contact with creams, chemicals, medicines or opaque pieces due to the accumulation of residues.",
        'sizes': None
    },
    {
        'ref': 38,
        'title': 'Modern Grace Ring',
        'price': 100.0,
        'type': 'Ring',
        'desc_header': "Product Description :   *Designer : ✨ Contemporary and striking design.\n*Versatile and elegant neutral tone.\n*Ideal for sophisticated looks or refined everyday wear .\n*Dimensions :  1.18 x 0.98 inches \n*Material: Plated Gold 18k      \n*Stones: Porcelain",
        'collection_desc': "Jardim de Luz Collection\nA collection that expresses delicacy and sophistication in every detail. Inspired by the lightness of flowers and the softness of light, Jardim de Luz features jewelry in subtle pastel tones, with elegant designs created to illuminate the look with grace and understated beauty.",
        'material_desc': "*Material: Made of high quality brass base metal with your choice of luxurious 18k gold or rhodium plating for long lasting shine. It is highly durable and designed for everyday use. \n\n*Hypoallergenic: Nickel-free, making them gentle on sensitive skin.\n\n* Stones : As it is a 100% natural product, there may be variations in the colors and shape of the stones.\n* All parts are sold separately. \n\nJewelry with 6 months warranty bath and manufacturing defects.\nWe do not guarantee: Broken  stones or cracked due to misuse, scratches, stains characterized by contact with creams, chemicals, medicines or opaque pieces due to the accumulation of residues.",
        'sizes': "Size 6 , 9"
    },
    {
        'ref': 88,
        'title': 'Golden Infinity Earrings',
        'price': 120.0,
        'type': 'Earring',
        'desc_header': "Product Description :   *Designer : Stunning earring! The intertwined organic shape adorned with zirconia stones creates movement, brilliance, and an ultra-elegant effect — a true statement piece.\n*Dimensions :   2.55 x 0.39inches \n*Material: Plated Gold 18k      \n*Stones: zirconia ",
        'collection_desc': "Jardim de Luz Collection\nA collection that expresses delicacy and sophistication in every detail. Inspired by the lightness of flowers and the softness of light, Jardim de Luz features jewelry in subtle pastel tones, with elegant designs created to illuminate the look with grace and understated beauty.",
        'material_desc': "*Material: Made of high quality brass base metal with your choice of luxurious 18k gold or rhodium plating for long lasting shine. It is highly durable and designed for everyday use. \n\n*Hypoallergenic: Nickel-free, making them gentle on sensitive skin.\n\n* Stones : As it is a 100% natural product, there may be variations in the colors and shape of the stones.\n* All parts are sold separately. \n\nJewelry with 6 months warranty bath and manufacturing defects.\nWe do not guarantee: Broken  stones or cracked due to misuse, scratches, stains characterized by contact with creams, chemicals, medicines or opaque pieces due to the accumulation of residues.",
        'sizes': None
    },
    {
        'ref': 89,
        'title': 'Golden Infinity Ring',
        'price': 80.0,
        'type': 'Ring',
        'desc_header': "Product Description :   *Designer : Stunning earring! The intertwined organic shape adorned with zirconia stones creates movement, brilliance, and an ultra-elegant effect — a true statement piece.\n*Dimensions :    0.51 inches \n*Material: Plated Gold 18k      \n*Stones: zirconia ",
        'collection_desc': "Jardim de Luz Collection\nA collection that expresses delicacy and sophistication in every detail. Inspired by the lightness of flowers and the softness of light, Jardim de Luz features jewelry in subtle pastel tones, with elegant designs created to illuminate the look with grace and understated beauty.",
        'material_desc': "*Material: Made of high quality brass base metal with your choice of luxurious 18k gold or rhodium plating for long lasting shine. It is highly durable and designed for everyday use. \n\n*Hypoallergenic: Nickel-free, making them gentle on sensitive skin.\n\n* Stones : As it is a 100% natural product, there may be variations in the colors and shape of the stones.\n* All parts are sold separately. \n\nJewelry with 6 months warranty bath and manufacturing defects.\nWe do not guarantee: Broken  stones or cracked due to misuse, scratches, stains characterized by contact with creams, chemicals, medicines or opaque pieces due to the accumulation of residues.",
        'sizes': "Size 6, 8"
    }
]

def slugify(value):
    value = str(value).lower()
    value = re.sub(r'[^\w\s-]', '', value).strip()
    value = re.sub(r'[-\s]+', '-', value)
    return value

def find_images_for_ref(ref_num):
    """
    Looks for a folder matching ref_num in SOURCE_DIR and returns list of copiable files.
    """
    # Pattern: 'foto_037' or 'Foto 37' or similar
    # We will search broadly
    
    found_folder = None
    for item in os.listdir(SOURCE_DIR):
        if str(ref_num) in item and os.path.isdir(os.path.join(SOURCE_DIR, item)):
            found_folder = os.path.join(SOURCE_DIR, item)
            break
            
    if not found_folder:
        return []
        
    images = []
    for f in sorted(os.listdir(found_folder)):
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')) and not f.startswith('.'):
            images.append(os.path.join(found_folder, f))
            
    return images

def main():
    print("🚀 Starting Supplementary Processing...")
    
    # Prepare CSV data
    new_csv_rows = []
    
    for product in NEW_PRODUCTS:
        ref = product['ref']
        title = product['title']
        print(f"Processing Ref {ref}: {title}")
        
        # 1. Handle Images
        source_images = find_images_for_ref(ref)
        if not source_images:
            print(f"❌ No images found for Ref {ref}")
            continue # Should we continue or error? Let's continue and log.
            
        final_image_urls = []
        slug = slugify(title)
        
        # Copy and Rename
        for idx, src_path in enumerate(source_images, start=1):
            ext = os.path.splitext(src_path)[1].lower()
            new_filename = f"REF-{ref:02d}_{slug}_{idx}{ext}"
            dest_path = os.path.join(TARGET_DIR, new_filename)
            
            shutil.copy2(src_path, dest_path)
            
            # Construct URL
            # Note: The user's system seems to assume these names map to this URL structure
            final_image_urls.append(f"{BASE_URL}/{new_filename}")
            
        print(f"✅ Copied {len(source_images)} images.")
        
        # 2. Construct Description
        # Combine parts: Header + [Sizes] + Material + Collection
        # NOTE: User asked to format description cleanly.
        
        description_parts = []
        description_parts.append(product['desc_header'])
        
        if product['sizes']:
             description_parts.append(f"\n\n**AVAILABLE SIZES: {product['sizes']}**")
             
        # Add collection info locally or material? 
        # The prompt implies a specific order? 
        # "Titulo | Foto | ... | Categoria | Descricao coleção | Texto padrão"
        # Usually Wix description is one HTML block.
        # Let's combine them logically.
        
        full_description = f"{product['desc_header']}\n\n{product['collection_desc']}\n\n{product['material_desc']}"
        if product['sizes']:
            full_description = f"**AVAILABLE SIZES: {product['sizes']}**\n\n" + full_description

        # Clean up quotes generally handled by CSV writer, but we pass string.
        
        # 3. Build CSV Row
        # Headers: handleId,fieldType,name,description,productImageUrl,collection,sku,ribbon,price,surcharge,visible,discountMode,discountValue,inventory,weight,cost
        
        sku = f"GOLD-{ref:02d}"
        
        row = {
            'handleId': slug,
            'fieldType': 'Product',
            'name': title,
            'description': full_description,
            'productImageUrl': ";".join(final_image_urls),
            'collection': '18k GOLD Plated',
            'sku': sku,
            'ribbon': '',
            'price': product['price'],
            'surcharge': 0,
            'visible': 'FALSE',
            'discountMode': 'PERCENT',
            'discountValue': 0,
            'inventory': 'InStock',
            'weight': 0,
            'cost': 0
        }
        
        new_csv_rows.append(row)

    # 4. Append to CSV
    if new_csv_rows:
        headers = [
            'handleId', 'fieldType', 'name', 'description', 'productImageUrl', 'collection', 'sku', 'ribbon', 
            'price', 'surcharge', 'visible', 'discountMode', 'discountValue', 'inventory', 'weight', 'cost'
        ]
        
        # Check if file exists to determine if we need header (it should exist based on prompt)
        file_exists = os.path.exists(OUTPUT_CSV)
        
        with open(OUTPUT_CSV, 'a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers, extrasaction='ignore')
            if not file_exists:
                writer.writeheader()
            
            # Optional: Add a newline if file doesn't end with one? 
            # 'a' mode usually appends to end. CSV writer handles newlines for rows.
            
            writer.writerows(new_csv_rows)
            
        print(f"✅ Appended {len(new_csv_rows)} products to {OUTPUT_CSV}")
        print("Done!")
    else:
        print("⚠️ No products processed.")

if __name__ == "__main__":
    main()
