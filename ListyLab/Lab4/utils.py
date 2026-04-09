import os
import json
from datetime import datetime

def get_converted_dir():
    target_dir = os.environ.get('CONVERTED_DIR', os.path.join(os.getcwd(), 'converted'))
    os.makedirs(target_dir, exist_ok=True)
    return target_dir

def get_timestamp_string():
   
    return datetime.now().strftime("%Y%m%d%H%M%S")

def save_history(target_dir, record):

    history_file = os.path.join(target_dir, 'history.json')
    history = []
    

    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                pass
                
    history.append(record)
    

    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=4, ensure_ascii=False)