import json
import re

input_file = 'dialogues_only_cleaned.jsonl'
output_file = 'final_super_cleaned.jsonl'

# 1️⃣ Keywords to filter out anywhere in the utterance (case‐insensitive)
keywords = [
    'also read', 'categories', 'tags', 'news', 'home', 'wikipedia', 'category', 'author',
    'KHALEELSHAMRAS:', 'Note:', 'NOTE:', 'Continue reading', 'Genus (ജനുസ്സ്)', 'tag', 'docat',
    'noun', 'verb', 'mal:', 'adverb', 'adjective', 'Pingback', 'Genus', 'Lyricis', 'Singer',
    'Comments', '‎', 'Subfolders', 'EXCLUSIVE', 'Vidyalayam:', 'Song', 'IFFK', 'justify;',
    'Read:', 'Caption:', 'Mute:', 'PS:', 'Mistake', 'VIEWS', 'More', 'VIEWS', 'Posted:', 'Step',
    'About:', 'Address', 'Reply:', 'IPL', 'RSS', 'Download', 'Response', 'Topic', '2018:', 'Family',
    'Re:', 'msgstr', 'Description:', r'\.com', 'location', 'part', 'malayalam', r'\bml\b', '#tags',
    'ans', 'answer', 'next', 'previous', 'name', 'source', 'Description ', 'MALAJÁLAM:', 'mlwiki',
    'DISCLAIMER', 'KERALA', 'Options', 'Most Read', 'Music', 'Q', 'Today’s Headlines', 'Chapter',
    'Video', 'ISLAM', 'Image:', 'NB:', 'Subject:', 'LIVE:', 'Ref:', 'Gallery:', 'Subfamily',
    'LINKS', 'Email', 'Filed', 'CPU:', 'DYFI', 'Hits:', 'Contact:'
]
keywords_pattern = re.compile(r'(' + r'|'.join(keywords) + r')', re.IGNORECASE)

# 2️⃣ Abnormal symbols at start (excluding @, ', \, /)
abnormal_symbols = re.compile(r"^[^a-zA-Z\d@'\\/]")

# 3️⃣ Regex to count English words
english_word_regex = re.compile(r'\b[a-zA-Z]+\b')

def is_english_word(word):
    return bool(re.fullmatch(r'[a-zA-Z]+', word))

# 4️⃣ Detect exactly four digits
four_digit_regex = re.compile(r'^\d{4}$')

# 5️⃣ Allowed character ranges: ASCII printable (\x20-\x7E), Malayalam (\u0D00-\u0D7F), basic emojis (\U0001F600-\U0001F64F)
invalid_char_regex = re.compile(r'[^\x20-\x7E\u0D00-\u0D7F\U0001F600-\U0001F64F]')

# 6️⃣ Substrings that, if present anywhere in utterance, should cause removal
bad_substrings = ['.JPG', '=', ' -', '" ', ' "', ' - ', '>>', '<<','NB','www','WWW','Posted', 'Contact','Module']

# Track duplicates
seen_utterances = set()

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', encoding='utf-8') as outfile:

    for line in infile:
        data = json.loads(line)
        utterance = data.get('utterance', '').strip()
        if not utterance:
            continue

        words = utterance.split()
        num_words = len(words)

        # --------------------------------------------------
        # A. LENGTH-BASED CHECK (very cheap)
        #    → Drop if fewer than 3 or more than 20 words
        if num_words < 4 or num_words > 20:
            continue

        # B. FIRST-WORD “DAY” CHECK (cheap string comparison)
        if words and words[0].upper() == 'DAY':
            continue

        # C. SECOND-WORD FOUR-DIGIT CHECK (cheap regex)
        if num_words >= 2 and four_digit_regex.fullmatch(words[1]):
            continue

        # D. BAD SUBSTRINGS CHECK (cheap substring search)
        if any(sub in utterance for sub in bad_substrings):
            continue

        # E. INVALID CHARACTER CHECK (regex on entire string)
        if invalid_char_regex.search(utterance):
            continue

        # F. START-CHARACTER CHECKS (single-char operations)
        # 1) Starts with digit → drop
        first_char = utterance[0]
        if first_char.isdigit():
            continue

        # 2) Starts with abnormal symbol (excluding @, ', \, /) → drop
        if abnormal_symbols.match(utterance):
            continue

        # G. FIRST-FOUR WORDS ALL-ENGLISH (requires checking 4 words)
        if num_words >= 4:
            first_four = words[:4]
            if all(is_english_word(w) for w in first_four):
                continue

        # H. COLON/SEMICOLON AFTER WORD 2
        #    → If utterance has ':' or ';' anywhere after the first two words, drop
        if num_words > 2:
            tail = ' '.join(words[2:])
            if ':' in tail or ';' in tail:
                continue

        # I. SYMBOLS ANYWHERE (cheap regex for '|' or '/')
        if re.search(r'[|/]', utterance):
            continue

        # J. COUNT ENGLISH WORDS IN ENTIRE UTTERANCE (moderate cost)
        if len(english_word_regex.findall(utterance)) > 5:
            continue

        # K. KEYWORD-PATTERN SEARCH (expensive regex)
        if keywords_pattern.search(utterance):
            continue

        # L. DUPLICATE CHECK (hash lookup, very cheap)
        if utterance in seen_utterances:
            continue
        seen_utterances.add(utterance)

        # — If it passed every rule, write it out
        outfile.write(json.dumps(data, ensure_ascii=False) + '\n')

print(f"✅ Final super-cleaned file created: {output_file}")
