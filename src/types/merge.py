# src/types/merge.py
from typing import Any


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """
    Recursively merge two dictionaries, with override taking precedence.
    
    Args:
        base: Base dictionary
        override: Dictionary with values to override
        
    Returns:
        Merged dictionary
    """
    result = base.copy()
    
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            # Recursively merge nested dictionaries
            result[key] = deep_merge(result[key], value)
        else:
            # Override or add the value
            result[key] = value
    
    return result


def merge_lists_unique(base: list[Any], override: list[Any]) -> list[Any]:
    """
    Merge two lists, preserving order and removing duplicates.
    Override items take precedence and appear first.
    
    Args:
        base: Base list
        override: List with items to add/override
        
    Returns:
        Merged list with unique items
    """
    seen = set()
    result = []
    
    # Add override items first
    for item in override:
        if item not in seen:
            seen.add(item)
            result.append(item)
    
    # Add base items not already present
    for item in base:
        if item not in seen:
            seen.add(item)
            result.append(item)
    
    return result