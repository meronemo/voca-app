import json
import os

DECKS_DIR = './decks'

def get_deck_path(deck_title):
    return os.path.join(DECKS_DIR, f'{deck_title}.json')

def read_json(filepath, default=None):
    if not os.path.exists(filepath):
        return default
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default

def write_json(filepath, data, key=None):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    if key:
        # Read existing data and update only the specified key
        existing = read_json(filepath, default={})
        existing[key] = data
        data = existing
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
