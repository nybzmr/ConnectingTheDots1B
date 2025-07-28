import json
import logging
import datetime

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def load_json(path: str) -> dict:
    with open(path, 'r') as f:
        return json.load(f)

def save_json(path: str, data: dict):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def get_current_timestamp() -> str:
    return datetime.datetime.now().isoformat()