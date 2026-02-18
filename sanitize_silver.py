import csv
import re
import os

INPUT_CSV = "/Users/paulomagrani/Desktop/wix-18k-fev26/Wix_Import_SILVER_READY.csv"
OUTPUT_CSV = "/Users/paulomagrani/Desktop/wix-18k-fev26/Wix_Import_SILVER_FINAL_CORRECTED.csv"

def sanitize_description(row):
    name = row['name']
    description = row['description']
    
    name_lower = name.lower()
    desc_lower = description.lower()
    
    # Rule 1: Ring (and NOT Earring) in Name, but Earring in Desc
    if "ring" in name_lower and "earring" not in name_lower and "earring" in desc_lower:
        description = re.sub(r'earring', 'Ring', description, flags=re.IGNORECASE)
        
    # Rule 2: Bracelet in Name, but Earring in Desc
    if "bracelet" in name_lower and "earring" in desc_lower:
         description = re.sub(r'earring', 'Bracelet', description, flags=re.IGNORECASE)

    # Rule 3: Necklace in Name, but Earring in Desc
    if "necklace" in name_lower and "earring" in desc_lower:
         description = re.sub(r'earring', 'Necklace', description, flags=re.IGNORECASE)

    # Rule 4: Ear Cuff in Name, but Necklace in Desc
    if "ear cuff" in name_lower and "necklace" in desc_lower:
        description = re.sub(r'necklace', 'Ear Cuff', description, flags=re.IGNORECASE)
        
    row['description'] = description
    return row


def main():
    if not os.path.exists(INPUT_CSV):
        print(f"Error: {INPUT_CSV} not found.")
        return

    with open(INPUT_CSV, 'r', encoding='utf-8') as f_in:
        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames
        
        rows = []
        for row in reader:
            rows.append(sanitize_description(row))
            
    with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"✅ CSV Sanitized. Saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
