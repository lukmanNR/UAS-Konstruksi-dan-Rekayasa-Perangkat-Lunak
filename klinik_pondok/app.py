from flask import Flask, render_template, request, redirect, url_for, session, flash
from logic.service import login_check, get_notifications_by_user, add_notification, get_all_recipients

app = Flask(__name__)
app.secret_key = 'kunci_rahasia_uas_klinik'

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = login_check(username, password)
    if user:
        session['user'] = user
        return redirect(url_for('dashboard'))
    flash("Username atau Password salah!")
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('index'))
    
    user = session['user']
    notifs = get_notifications_by_user(user)
    notifs.reverse() # Terbaru di atas
    
    # Ambil daftar user untuk dropdown admin
    recipients = get_all_recipients() if user['role'] == 'admin' else []
    
    return render_template('dashboard.html', user=user, notifications=notifs, recipients=recipients)

@app.route('/add_notif', methods=['POST'])
def add_notif():
    if 'user' in session and session['user']['role'] == 'admin':
        penerima_username = request.form.get('penerima_username')
        pesan = request.form.get('pesan')
        if penerima_username and pesan:
            add_notification(penerima_username, pesan)
            flash("Notifikasi berhasil dikirim!")
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)