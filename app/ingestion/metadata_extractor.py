# ingestion/metadata_extractor.py

import re

def extract_metadata(text, source_name):

    metadata = []

    current_section = "root"

    for line in text.split("\n"):

        if line.startswith("#"):

            current_section = line.replace("#", "").strip()

        metadata.append({
            "section": current_section,
            "source": source_name
        })

    return metadata