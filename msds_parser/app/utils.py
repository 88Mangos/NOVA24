# app/utils.py
import os
from typing import Dict, Any
import json

def load_sample_msds(filename: str) -> str:
    """Load sample MSDS from data directory."""
    path = os.path.join('data', 'samples', filename)
    with open(path, 'r') as f:
        return f.read()

def cache_result(chemical_name: str, result: Dict[str, Any]) -> None:
    """Cache parsing results."""
    path = os.path.join('data', 'parsed', f'{chemical_name}.json')
    with open(path, 'w') as f:
        json.dump(result, f, indent=2)