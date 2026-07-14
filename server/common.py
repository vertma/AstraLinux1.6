import hashlib

PORT = 5555

DB_CONFIG = {
    "dbname": "user_accounting",
    "user": "postgres",
    "password": "",
    "host": "localhost"
}

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()
