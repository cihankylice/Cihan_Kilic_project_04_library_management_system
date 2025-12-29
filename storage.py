import json
import os
import shutil
from datetime import datetime

def ensure_data_paths(base_dir: str) -> None:
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    files = ['books.json', 'patrons.json', 'loans.json']
    for f in files:
        path = os.path.join(base_dir, f)
        if not os.path.exists(path):
            with open(path, 'w') as file:
                json.dump([], file)

def load_state(base_dir: str) -> tuple:
    try:
        with open(os.path.join(base_dir, 'books.json'), 'r') as f:
            books = json.load(f)
        with open(os.path.join(base_dir, 'patrons.json'), 'r') as f:
            patrons = json.load(f)
        with open(os.path.join(base_dir, 'loans.json'), 'r') as f:
            loans = json.load(f)
        return books, patrons, loans
    except FileNotFoundError:
        return [], [], []
    except json.JSONDecodeError:
        print("Error reading data files. Starting empty.")
        return [], [], []

def save_state(base_dir: str, books: list, patrons: list, loans: list) -> None:
    with open(os.path.join(base_dir, 'books.json'), 'w') as f:
        json.dump(books, f, indent=4)
    with open(os.path.join(base_dir, 'patrons.json'), 'w') as f:
        json.dump(patrons, f, indent=4)
    with open(os.path.join(base_dir, 'loans.json'), 'w') as f:
        json.dump(loans, f, indent=4)

def backup_state(base_dir: str, backup_dir: str) -> list:
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_files = []
    
    files = ['books.json', 'patrons.json', 'loans.json']
    for f in files:
        src = os.path.join(base_dir, f)
        dst = os.path.join(backup_dir, f"{f}_{timestamp}.bak")
        if os.path.exists(src):
            shutil.copy2(src, dst)
            backup_files.append(dst)
            
    return backup_files

def validate_catalog_schema(books: list) -> bool:
    required_keys = ['isbn', 'title', 'authors', 'year', 'genre', 'copies_owned', 'copies_available']
    for book in books:
        if not all(k in book for k in required_keys):
            return False
    return True