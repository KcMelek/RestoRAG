# ingestion/normalizer.py

import re

def normalize_text(text: str):

    text = re.sub(r'\n{3,}', '\n\n', text)

    text = re.sub(r'[ \t]+', ' ', text)

    return text.strip()