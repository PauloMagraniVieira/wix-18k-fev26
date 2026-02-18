import csv
import os

INPUT_CSV = '/Users/paulomagrani/Desktop/wix-18k-fev26/Wix_Import_FINAL_READY.csv'
OUTPUT_CSV = '/Users/paulomagrani/Desktop/wix-18k-fev26/Wix_UPLOAD_ONLY_NEW_4.csv'

def main():
    with open(INPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        all_rows = list(reader)
        
    header = all_rows[0]
    data_rows = all_rows[1:]
    
    # Get last 4 rows
    if len(data_rows) >= 4:
        last_4_rows = data_rows[-4:]
    else:
        last_4_rows = data_rows
        
    print(f"Total data rows: {len(data_rows)}")
    print(f"Extracting last {len(last_4_rows)} rows.")
    
    with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(last_4_rows)
        
    print(f"Successfully created {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
