import re
def extract_yt_term(query):
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    if not isinstance(query, str):
        return None
    match = re.search(pattern, query, re.IGNORECASE)
    return match.group(1) if match else None