Malayalam Corpus Processing Pipeline

This repository processes a large Malayalam corpus downloaded from CC100 Malayalam Dataset. The original .txt file was approximately 8 GB in size and was split into 250 smaller chunks for easier handling and processing.

Processing Steps
extract_dialogues.py
This script processes the split corpus files and generates a file named dialogues_only.jsonl, containing only the extracted dialogue lines.

cleaning_dialogues.py
The dialogues_only.jsonl file is manually reviewed to identify common unwanted patterns. These patterns are removed using this script, producing dialogues_only_cleaned.jsonl.

super_clean_filter.py
After another round of manual review, dialogues_only_cleaned.jsonl is filtered further to remove any remaining noise, resulting in the final_super_cleaned.jsonl file.

last_cleansing.py
A final pass is done on final_super_cleaned.jsonl to manually remove outliers and unwanted patterns. This results in the cleanest version: cleaned_final.jsonl.
