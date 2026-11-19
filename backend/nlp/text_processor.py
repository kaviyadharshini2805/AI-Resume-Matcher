import re
from typing import List, Set

COMMON_STOPWORDS: Set[str] = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", 
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", 
    "by", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", 
    "further", "had", "has", "have", "having", "he", "her", "here", "hers", "herself", "him", 
    "himself", "his", "how", "i", "if", "in", "into", "is", "it", "its", "itself", "just", "me", 
    "more", "most", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", 
    "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "should", 
    "so", "some", "such", "than", "that", "the", "their", "theirs", "them", "themselves", "then", 
    "there", "these", "they", "this", "those", "through", "to", "too", "under", "until", "up", 
    "very", "was", "we", "were", "what", "when", "where", "which", "while", "who", "whom", "why", 
    "with", "would", "you", "your", "yours", "yourself", "yourselves"
}

def clean_text(text: str) -> str:
    """Normalize text: convert to lowercase, remove URLs, special characters, and excessive whitespaces."""
    if not text:
        return ""
    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", " ", text, flags=re.MULTILINE)
    # Remove special chars but retain alphanumeric and common technical symbols (+, #, .)
    text = re.sub(r"[^\w\s\+\#\.]", " ", text)
    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text.lower()

def extract_keywords(text: str) -> List[str]:
    """Tokenize and filter out common stopwords from text."""
    cleaned = clean_text(text)
    tokens = [t.strip(".") for t in cleaned.split() if t.strip(".")]
    keywords = [t for t in tokens if t not in COMMON_STOPWORDS and len(t) > 1]
    return keywords
