from persistence.repository import load_data, save_data
from datetime import datetime

def login_check(username, password):
    data = load_data()
    for user in data['users']:
        if user['username'] == username and user['password'] == password:
            return user
    return None

def get_all_recipients():
    """Mengambil semua user kecuali admin untuk daftar pilihan di dashboard"""
    data = load_data()
    return [u for u in data['users'] if u['role'] != 'admin']

def get_notifications_by_user(user_data):
    """Mengambil notifikasi: Admin lihat semua, User lihat milik sendiri"""
    data = load_data()
    all_notifs = data.get('notifikasi', [])
    
    if user_data['role'] == 'admin':
        return all_notifs
    
    # User hanya melihat pesan yang ditujukan ke username mereka
    return [n for n in all_notifs if n.get('penerima_username') == user_data['username']]

def add_notification(penerima_username, pesan):
    """Menambahkan notifikasi dengan mencatat username dan nama penerima"""
    data = load_data()
    
    # Cari nama asli penerima berdasarkan username
    penerima_nama = "Umum"
    for u in data['users']:
        if u['username'] == penerima_username:
            penerima_nama = u['nama']
            break

    new_notif = {
        "penerima_username": penerima_username,
        "penerima_nama": penerima_nama,
        "pesan": pesan,
        "waktu": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    if 'notifikasi' not in data:
        data['notifikasi'] = []
    data['notifikasi'].append(new_notif)
    save_data(data)
    return True