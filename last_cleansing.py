import json
import re

input_file = "final_super_cleaned.jsonl"
output_file = "cleaned_final.jsonl"

# List of words to filter out
remove_words = {"studio", "movie"}  # Case-insensitive match

def tokenize(text):
    # Simple word tokenizer (punctuation-safe)
    return re.findall(r'\b\w+\b', text.lower())

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile:
        try:
            data = json.loads(line)
            utterance = data.get("utterance", "")
            bow = set(tokenize(utterance))  # Convert to set for faster lookup

            # If none of the remove_words are in the utterance, keep it
            if bow.isdisjoint(remove_words):
                outfile.write(json.dumps(data, ensure_ascii=False) + "\n")
        except json.JSONDecodeError as e:
            print(f"Skipping malformed line: {e}")
