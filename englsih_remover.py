import json
import re
import os

# --- CONFIGURATION ---
input_filename = "final_super_cleaned.jsonl"  # REPLACE with your actual file name
output_filename = "experiment_sentences.jsonl"

# Ensure output directory exists
os.makedirs("data", exist_ok=True)

print(f"Filtering text from {input_filename}...")
print("Criteria: Deleting lines containing English letters, '@', or ':'")

valid_sentences = []

try:
    with open(input_filename, 'r', encoding='utf-8') as infile:
        for line in infile:
            if not line.strip(): continue
            
            try:
                data = json.loads(line)
                text = data.get("utterance", "").strip()
                
                # --- UPDATED FILTER LOGIC ---
                # Checks for:
                # 1. English letters (a-z, A-Z)
                # 2. The '@' symbol
                # 3. The ':' symbol
                if re.search(r'[a-zA-Z@:]', text):
                    continue  # SKIP this line completely
                
                # If valid, keep it
                valid_sentences.append(text)
                
            except json.JSONDecodeError:
                continue

    # --- WRITING STEP ---
    total_valid = len(valid_sentences)
    midpoint = total_valid // 2
    
    print(f"Found {total_valid} valid sentences.")
    
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        for index, text in enumerate(valid_sentences):
            count = index + 1
            
            # First half = Formal, Second half = Informal
            domain = "Formal" if count <= midpoint else "Informal"
            
            new_record = {
                "Sentence_ID": f"S{count:03d}",
                "Domain": domain,
                "text": text
            }
            
            outfile.write(json.dumps(new_record, ensure_ascii=False) + "\n")

    print(f"Successfully saved clean dataset to {output_filename}")

except FileNotFoundError:
    print(f"Error: File '{input_filename}' not found.")