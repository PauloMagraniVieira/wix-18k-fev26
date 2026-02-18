# SYSTEM ROLE: SENIOR DATA ARCHITECT
# MISSION: GENERATE 100% CLEAN CSV FROM HARDCODED DATA

import os
import csv
import re

# 1. DADOS PURIFICADOS (Baseado no seu texto + Correção do 55)
# A Regra é: O Título é a Verdade Absoluta.
products_db = {
    "39": {"name": "Premium Fancy Yellow Earring", "price": "65", "desc": "Delicate and full of charm, this sterling silver earring features a heart-shaped center stone in a soft yellow hue, surrounded by a halo of crystal zirconia that enhances its brilliance even more.\n*Dimensions : 0.39 x 0.39 inches\n*Material: Sterling silver\n*Stones: zirconia"},
    "40": {"name": "Premium Fancy Yellow Ring", "price": "65", "desc": "Delicate and full of charm, this sterling silver earring features a heart-shaped center stone in a soft yellow hue, surrounded by a halo of crystal zirconia that enhances its brilliance even more.\n*Dimensions : 0.39 x 0.39 inches\n*Material: Sterling silver\n*Stones: zirconia\nSize 8"},
    "41": {"name": "Premium Fancy Yellow Bracelet", "price": "100", "desc": "Delicate and full of charm, this sterling silver earring features a heart-shaped center stone in a soft yellow hue, surrounded by a halo of crystal zirconia that enhances its brilliance even more.\n*Dimensions Pendant : 0.39 x 0.39 inches *Dimensions : 6.69 inches\n*Material: Sterling silver\n*Stones: zirconia"},
    "42": {"name": "Fusion Turmalina Triangle Earring", "price": "125", "desc": "Elegant and contemporary, this sterling silver earring features an intense fusion tourmaline stone in a rounded triangular geometric shape, surrounded by a delicate halo of crystal zirconia that enhances its brilliance even more.\n*Dimensions : 0.59 x 0.59 inches\n*Material: Sterling silver\n*Stones: Zirconia"},
    "43": {"name": "Fusion Turmalina Triangle Necklace", "price": "100", "desc": "Elegant and contemporary, this sterling silver earring features an intense fusion tourmaline stone in a rounded triangular geometric shape, surrounded by a delicate halo of crystal zirconia that enhances its brilliance even more.\n*Dimensions Pendant:0.59 x 0.59 inches *Dimension Chain : 21.65 inches\n*Material: Sterling silver\n*Stones: Zirconia"},
    "44": {"name": "Fusion Turmalina Triangle Earring", "price": "125", "desc": "Elegant and contemporary, this sterling silver earring features an intense fusion tanzanita stone in a rounded triangular geometric shape, surrounded by a delicate halo of crystal zirconia that enhances its brilliance even more.\n*Dimensions : 0.59 x 0.59 inches\n*Material: Sterling silver\n*Stones: Zirconia"},
    "45": {"name": "Fusion Turmalina Triangle Ring", "price": "100", "desc": "Elegant and contemporary, this sterling silver earring features an intense fusion tanzanita stone in a rounded triangular geometric shape, surrounded by a delicate halo of crystal zirconia that enhances its brilliance even more.\n*Dimensions : 0.59 x 0.59 inches\n*Material: Sterling silver\n*Stones: Zirconia"},
    "46": {"name": "Butterfly Glow Necklace", "price": "85", "desc": "Romantic and sophisticated, this sterling silver necklace features three delicate butterflies adorned with crystal zirconia, creating a luminous and elegant effect against the skin.\n*Dimensions 3 Pendant : 0.19 x 0.98 inches. *Dimensions Chain : 17.71 inches\n*Material: Sterling silver\n*Stones: Zirconia"},
    "48": {"name": "Butterfly Glow Ear cuff", "price": "85", "desc": "Romantic and sophisticated, this sterling silver necklace features three delicate butterflies adorned with crystal zirconia, creating a luminous and elegant effect against the skin.\n*Dimensions : 0.19 x 0.98 inches.\n*Material: Sterling silver\n*Stones: Zirconia"},
    "49": {"name": "Two Stars Earrings", "price": "95", "desc": "Sophisticated and full of personality, this sterling silver earring features two stars adorned with crystal zirconia, creating a luminous and contemporary effect.\n*Dimensions : 0.78 inches\n*Material: Sterling silver\n*Stones: Zirconia"},
    "50": {"name": "Eternal Sapphire Riviera", "price": "490", "desc": "Classic and sophisticated, this sterling silver riviera-style necklace is set with colorless sapphires, reflecting light with intensity and elegance, creating a refined and timeless sparkle.\n*Dimensions : 16.53 inches\n*Material: Sterling silver\n*Stones: Colorless sapphire"},
    "51": {"name": "Radiant Pearl Stud Earring", "price": "130", "desc": "Sophisticated and feminine, this sterling silver earring combines the elegance of a shell pearl with the delicate sparkle of zirconia stones set on the upper detail.\n*Dimensions : 0.59 inches\n*Material: Sterling silver\n*Stones: Shell Pearl and Zirconias"},
    "52": {"name": "Garden Radiance Stud Earring", "price": "99", "desc": "Elegant and feminine, this sterling silver earring features an oval stone in a soft tourmaline tone, highlighted by delicate marquise-cut zirconia that create a sophisticated floral effect. The final touch is a small shell pearl, adding lightness and romantic charm to the design.\n*Dimensions : 0.59 inches\n*Material: Sterling silver\n*Stones: Zirconia and Shell Pearl"},
    "53": {"name": "Royal Champagne Earrings", "price": "99", "desc": "Sophisticated and refined, this sterling silver earring features a brilliant-cut center stone in a champagne hue, surrounded by a delicate halo of zirconia that enhances its sparkle even more.\n*Dimensions : 0.39 x 0.39 inches\n*Material: Sterling silver\n*Stones: Zirconias"},
    "55": {"name": "Royal Champagne Ring", "price": "115", "desc": "Sophisticated and refined, this sterling silver ring features a brilliant-cut center stone in a champagne hue, surrounded by a delicate halo of zirconia that enhances its sparkle even more.\n*Dimensions : 0.39 inches\n*Material: Sterling silver\n*Stones: Zirconias"}, 
    "56": {"name": "Aurora Interlace Earrings", "price": "99", "desc": "Elegant and contemporary, this sterling silver earring features an organic design with delicately intertwined curves, adorned with crystal zirconia that provide a subtle and refined sparkle.\n*Dimensions : 0.39 x 0.39 inches\n*Material: Sterling silver\n*Stones: zirconia"},
    "57": {"name": "Majestic Sparkle Ring", "price": "99", "desc": "Elegant and contemporary, this sterling silver earring features an organic design with delicately intertwined curves, adorned with crystal zirconia that provide a subtle and refined sparkle.\n*Dimensions : 0.39 x 0.39 inches\n*Material: Sterling silver\n*Stones: zirconia\nSize 6.5"},
    "58": {"name": "Royal White Earrings", "price": "99", "desc": "Sophisticated and refined, this sterling silver earring features a brilliant-cut center stone, surrounded by a delicate halo of zirconia that enhances its sparkle even more.\n*Dimensions : 0.39 x 0.39 inches\n*Material: Sterling silver\n*Stones: zirconia"},
    "59": {"name": "Butterfly Radiance Earrings", "price": "130", "desc": "Classic and sophisticated, this sterling silver butterfly-shaped earring combines the striking brilliance of delicately faceted zirconia with the timeless softness of a shell pearl.\n*Dimensions : 0.78 x 0.59inches\n*Material: Sterling silver\n*Stones: zirconia"}
}

# 2. CONFIGURAÇÕES
images_dir = "/Users/paulomagrani/Desktop/wix-18k-fev26/wix-Fev26/925 Silver"
output_csv = "/Users/paulomagrani/Desktop/wix-18k-fev26/Wix_Import_SILVER_MASTER_FIXED.csv"
base_url = "https://wix-18k-fev26.pages.dev/925%20Silver/"

# 3. LÓGICA DE EXECUÇÃO
print("🚀 Iniciando Reconstrução do CSV Silver...")

# Escanear arquivos existentes
if not os.path.exists(images_dir):
    print(f"❌ Erro: Diretório {images_dir} não encontrado.")
    exit(1)

existing_files = sorted(os.listdir(images_dir))
files_map = {}
for f in existing_files:
    if f.startswith("REF-") and (f.endswith(".webp") or f.endswith(".jpeg") or f.endswith(".jpg")):
        # Extrair numero do REF (ex: REF-39_... -> 39)
        try:
            # Handle standard "REF-XX_..."
            # Also handle if underscore logic varies, but REF-XX is standard.
            # Split by _ or - or just take char 4-5?
            # Assuming format "REF-XX_..."
            parts = f.split("_")
            if len(parts) > 0:
                ref_part = parts[0] # REF-39
                ref_num = ref_part.replace("REF-", "")
                
                # Handling "REF-5" vs "REF-05"? DB keys are "39", "40".
                # If file is REF-5_..., ref_num is "5".
                # If file is REF-05_..., ref_num is "05".
                # Let's normalize to int then str to match DB keys if they are no leading zeros?
                # The DB keys are "39", "55".
                # The file REF-39_... -> "39".
                # Assuming no leading zeros in DB keys (confirmed).
                # But files might have "05"?
                # Let's just strip leading zeros if numeric.
                if ref_num.isdigit():
                    ref_num = str(int(ref_num))
                
                if ref_num not in files_map:
                    files_map[ref_num] = []
                files_map[ref_num].append(f)
        except Exception as e:
            print(f"Error parsing file {f}: {e}")
            continue

# Preparar CSV
header = ["handleId", "fieldType", "name", "description", "productImageUrl", "collection", "sku", "price", "visible"]
csv_rows = []

for ref in sorted(products_db.keys(), key=lambda x: int(x)):
    data = products_db[ref]
    # Verificar se temos imagens para este REF
    if ref not in files_map:
        print(f"⚠️ AVISO: Ref {ref} ({data['name']}) ignorado - Sem imagens na pasta.")
        continue
    
    images = files_map[ref]
    # Gerar URLs
    # Encode spaces in filenames?
    # base_url ends in .../925%20Silver/
    # If file is "REF-39_name.webp", url is base_url + "REF-39_name.webp".
    # Browser handles spaces in filename if not encoded? Use %20?
    # Usually better to encode. But let's stick to what worked or simple concat if filenames are safe.
    # Filenames here have hyphens and underscores mostly. 
    # But if there are spaces, we should encode.
    
    from urllib.parse import quote
    image_urls = []
    for img in images:
        # We manually encode the filename part just in case
        # But base_url already has %20.
        # img might have space.
        img_encoded = quote(img) 
        image_urls.append(base_url + img_encoded)
        
    image_field = ";".join(image_urls)
    

    # SANITIZAÇÃO DE TEXTO (CORREÇÃO DE ERROS)
    clean_desc = data['desc']
    title_lower = data['name'].lower()
    
    # Fix: Ensure "earring" doesn't trigger "ring" logic
    if "ring" in title_lower and "earring" not in title_lower:
        clean_desc = clean_desc.replace("earring", "ring").replace("Earring", "Ring")
    elif "bracelet" in title_lower:
        clean_desc = clean_desc.replace("earring", "bracelet").replace("Earring", "Bracelet")

    elif "necklace" in title_lower:
        clean_desc = clean_desc.replace("earring", "necklace").replace("Earring", "Necklace")
    elif "ear cuff" in title_lower:
         clean_desc = clean_desc.replace("necklace", "ear cuff").replace("Necklace", "Ear cuff")
        
    # Criar Handle ID amigável
    # User code: handle = data['name'].lower().replace(" ", "-").replace("&", "and").replace("/", "-")
    handle = data['name'].lower().replace(" ", "-").replace("&", "and").replace("/", "-")
    
    row = [
        handle,
        "Product",
        data['name'],
        clean_desc,
        image_field,
        "925 Silver; New Arrivals",
        f"REF-{ref}",
        data['price'],
        "FALSE" # Visible False para segurança
    ]
    csv_rows.append(row)

# Salvar CSV
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(csv_rows)

print(f"✅ SUCESSO! CSV Gerado: {output_csv}")
print(f"📦 Total de Produtos: {len(csv_rows)}")
print("🔍 Verifique o Ref 55 no arquivo final!")
