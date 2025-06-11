import json
import re

input_file = 'dialogues_only.jsonl'
output_file = 'dialogues_only_cleaned.jsonl'

# URL & email regex
url_regex = re.compile(r'https?://\S+|www\.\S+')
email_regex = re.compile(r'[\w\.-]+@[\w\.-]+')

# Extended date/time patterns
date_patterns = [
    # Day and month names (short and long)
    r'\b(Sun(day)?|Mon(day)?|Tue(sday)?|Wed(nesday)?|Thu(rsday)?|Fri(day)?|Sat(urday)?)\b',
    r'\b(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\b',

    # Numeric date formats (various separators and orders)
    r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b',         # 22-10-2013, 22/10/13
    r'\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b',           # 2013-10-22
    r'\b\d{1,2}/\d{1,2}/\d{4}\b',                 # 10/22/2013

    # Day with suffix
    r'\b\d{1,2}(st|nd|rd|th)?\s+(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)(\s+\d{4})?\b',

    # Time formats
    r'\b\d{1,2}:\d{2}(:\d{2})?\s?(AM|PM|am|pm)?\b',  # 11:57:00 PM, 23:59

    # Common posting phrases
    r'\bPosted on\b',
    r'\bPosted by\b',
    r'\bat\s+\d{1,2}:\d{2}',        # e.g., at 8:25 PM
    r'\b\d{1,2}:\d{2}(\s?[APap][Mm])?\b',  # time without "at"
    r'\b\d{1,2}(st|nd|rd|th)?\s+\w+\s+\d{4}\b',  # e.g., 20th October 2013
]

# Combine into one regex
date_regex = re.compile('|'.join(date_patterns), re.IGNORECASE)

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', encoding='utf-8') as outfile:
    for line in infile:
        data = json.loads(line.strip())
        utterance = data['utterance'].strip()
        
        # Remove lines with URLs or emails
        if url_regex.search(utterance):
            continue
        if email_regex.search(utterance):
            continue
        
        # Remove lines starting with known irrelevant prefixes
        if utterance.lower().startswith(('labels', 'title', 'വെബ്', 'gmail','by','read more','read also')):
            continue
        
        # Remove lines ending with "said..." or matching "name said..."
        if utterance.endswith('said...') or utterance.endswith('പറഞ്ഞു...'):
            continue
        if re.match(r'.+\s+said\.\.\.$', utterance, re.IGNORECASE):
            continue
        if '.JPG' in utterance:
            continue
        
        if '=' in utterance:
            continue


        # Remove lines containing any date/time or "posted on/by" patterns
        if date_regex.search(utterance):
            continue

        # Keep clean dialogues only
        outfile.write(json.dumps(data, ensure_ascii=False) + '\n')

print(f"✅ Final cleaned file created: {output_file}")
