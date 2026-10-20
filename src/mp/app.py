from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = 'sch688_vvedenie'
DB_USER = 'sch688_vvedenie'
DB_HOST = '185.114.247.43'
DB_PASS = "Querty123"

app = Flask(__name__)
app.secret_key = 'super_secret_key_change_me' 

def connect():
    return mysql.connector.connect(
        host=DB_HOST,
        port=3306,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

@app.route("/")
def info():
    return render_template('info.html')

@app.route("/reg")
def reg():
    return render_template('reg.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/register", methods=['POST'])
def user_reg():
    req = request.get_json()
    name = req.get('name', '').strip()
    email = req.get('email', '').strip()
    password = req.get('password')
    
    if not name or not email or not password:
        return jsonify({"error": "Заполните все обязательные поля"}), 400

    password_hash = generate_password_hash(password)

    try:
        cnx = connect()
        cur = cnx.cursor()
        
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            return jsonify({"error": "Этот email уже зарегистрирован"}), 400

        cur.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
            (name, email, password_hash)
        )
        cnx.commit() 
        return jsonify({"success": True})
    except mysql.connector.Error as err:
        return jsonify({"error": f"Ошибка базы данных: {err}"}), 500
    finally:
        cur.close()
        cnx.close()

# ========================================================
# 1. ОБНОВЛЕННЫЙ РОУТ АВТОРИЗАЦИИ (записывает данные в сессию)
# ========================================================
@app.route("/user_authorization", methods=['POST'])
def user_login():
    req = request.get_json()
    email = req.get('email', '').strip()
    password = req.get('password')

    if not email or not password:
        return jsonify({"error": "Введите email и пароль"}), 400

    try:
        cnx = connect()
        cur = cnx.cursor(dictionary=True)
        
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        if user and check_password_hash(user['password'], password):
            # Сохраняем данные пользователя в сессию Flask
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            
            # Если у вас в таблице пока нет столбца balance, 
            # код автоматически поставит заглушку 500 рублей, чтобы ничего не ломалось
            session['user_balance'] = user.get('balance', 500) 
            
            return jsonify({"success": True})
        else:
            return jsonify({"error": "Неверный email или пароль"}), 401
            
    except Exception as err:
        return jsonify({"error": f"Ошибка базы данных: {str(err)}"}), 500
    finally:
        if 'cur' in locals(): cur.close()
        if 'cnx' in locals(): cnx.close()


# ========================================================
# 2. НОВЫЙ РОУТ ДЛЯ ЛИЧНОГО КАБИНЕТА
# ========================================================
@app.route("/lk")
def lk():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('lk.html')


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('info'))

if __name__ == "__main__":
    app.run(debug=True)
