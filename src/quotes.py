import json
import random
from typing import Optional, Dict, Any

# Global variable to track last quote ID for avoiding consecutive repeats
_LAST_QUOTE_ID: Optional[int] = None


def _load_quotes() -> list:
    """Load quotes from data/quotes.json."""
    try:
        with open("data/quotes.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict) or "quotes" not in data:
                raise ValueError("Invalid quotes.json structure")
            quotes = data["quotes"]
            if not isinstance(quotes, list):
                raise ValueError("quotes must be a list")
            return quotes
    except FileNotFoundError:
        raise FileNotFoundError("data/quotes.json not found")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in quotes.json: {e}")


def get_random_quote(category: Optional[str] = None) -> Dict[str, Any]:
    """
    Get a random love quote from the database.
    
    Args:
        category: Optional category filter ('sweet', 'funny', 'romantic')
        
    Returns:
        Dict with 'id', 'content', 'category', 'tags'
        
    Raises:
        FileNotFoundError: If quotes.json is not found
        ValueError: If category is invalid or no quotes match
    """
    global _LAST_QUOTE_ID
    
    quotes = _load_quotes()
    
    if not quotes:
        raise ValueError("No quotes available")
    
    # Filter by category if specified
    if category:
        category_lower = category.lower()
        filtered = [q for q in quotes if q.get("category", "").lower() == category_lower]
        if not filtered:
            valid_categories = set(q.get("category") for q in quotes if q.get("category"))
            raise ValueError(f"Invalid category '{category}'. Valid categories: {valid_categories}")
        candidates = filtered
    else:
        candidates = quotes
    
    # Avoid consecutive repeats if possible
    if _LAST_QUOTE_ID is not None and len(candidates) > 1:
        candidates = [q for q in candidates if q.get("id") != _LAST_QUOTE_ID]
    
    # Select random quote
    quote = random.choice(candidates)
    _LAST_QUOTE_ID = quote.get("id")
    
    return quote
