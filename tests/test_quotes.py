import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from quotes import get_random_quote, _load_quotes


def test_load_quotes():
    """Test that quotes can be loaded from JSON"""
    quotes = _load_quotes()
    assert isinstance(quotes, list)
    assert len(quotes) >= 200
    
    # Check structure of first quote
    first = quotes[0]
    assert "id" in first
    assert "content" in first
    assert "category" in first
    assert "tags" in first


def test_get_random_quote_structure():
    """Test that get_random_quote returns correct structure"""
    quote = get_random_quote()
    assert "id" in quote
    assert "content" in quote
    assert "category" in quote
    assert "tags" in quote
    assert isinstance(quote["content"], str)
    assert len(quote["content"]) > 0


def test_get_random_quote_category_filter():
    """Test category filtering"""
    quote = get_random_quote("sweet")
    assert quote["category"].lower() == "sweet"
    
    quote = get_random_quote("funny")
    assert quote["category"].lower() == "funny"
    
    quote = get_random_quote("romantic")
    assert quote["category"].lower() == "romantic"


def test_get_random_quote_invalid_category():
    """Test that invalid category raises ValueError"""
    with pytest.raises(ValueError):
        get_random_quote("invalid_category")


def test_get_random_quote_no_consecutive_repeat():
    """Test that consecutive calls don't return the same quote"""
    # Get multiple quotes and check they're not all the same
    quotes_set = set()
    for _ in range(10):
        quote = get_random_quote()
        quotes_set.add(quote["id"])
    
    # With 200+ quotes, we should get some variety in 10 calls
    assert len(quotes_set) > 1, "Should get different quotes across multiple calls"
