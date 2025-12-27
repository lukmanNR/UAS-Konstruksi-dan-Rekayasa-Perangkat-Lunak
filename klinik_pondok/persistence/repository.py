import json
import os

# Mencari lokasi absolut agar tidak error saat dijalankan dari terminal manapun
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'data.json')

def load_data():
    if not os.path.exists(DB_PATH):
        return {"users": [], "notifikasi": []}
    with open(DB_PATH, 'r') as f:
        return json.load(f)

def save_data(data):
    # Pastikan folder database ada
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with open(DB_PATH, 'w') as f:
        json.dump(data, f, indent=4)