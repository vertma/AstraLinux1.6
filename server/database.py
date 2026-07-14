import psycopg2
import psycopg2.extras
from common import DB_CONFIG

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id SERIAL PRIMARY KEY,
            admin_login VARCHAR(50),
            action VARCHAR(100),
            target_login VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def log_action(admin_login, action, target_login=""):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO audit_log (admin_login, action, target_login) VALUES (%s, %s, %s)",
        (admin_login, action, target_login)
    )
    conn.commit()
    cur.close()
    conn.close()

def find_user(login, password_hash):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, full_name, position FROM users WHERE login=%s AND password_hash=%s AND is_active=true",
        (login, password_hash)
    )
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

def get_all_users():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id, login, full_name, position, phone, is_active, created_at, role FROM users ORDER BY id")
    rows = cur.fetchall()
    users = []
    for row in rows:
        users.append({
            'id': row['id'],
            'login': row['login'],
            'full_name': row['full_name'],
            'position': row['position'],
            'phone': row['phone'],
            'is_active': row['is_active'],
            'created_at': str(row['created_at']) if row['created_at'] else '',
            'role': row['role']
        })
    cur.close()
    conn.close()
    return users

def create_user(login, password_hash, full_name, position, phone, role='user'):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO users (login, password_hash, full_name, position, phone, is_active, role) 
           VALUES (%s, %s, %s, %s, %s, true, %s)""",
        (login, password_hash, full_name, position, phone, role)
    )
    conn.commit()
    cur.close()
    conn.close()

def update_user(user_id, full_name, position, phone, is_active):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET full_name=%s, position=%s, phone=%s, is_active=%s WHERE id=%s",
        (full_name, position, phone, is_active, user_id)
    )
    conn.commit()
    cur.close()
    conn.close()

def deactivate_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET is_active=false WHERE id=%s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()

def get_audit_logs(limit=50):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        "SELECT admin_login, action, target_login, created_at FROM audit_log ORDER BY created_at DESC LIMIT %s",
        (limit,)
    )
    logs = [dict(row) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return logs

def get_user_role(login):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT role FROM users WHERE login = %s", (login,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0] if result else 'user'
