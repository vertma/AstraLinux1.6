import json
from common import hash_password
import database

class ClientHandler:
    def __init__(self, socket):
        print("=== Новое подключение ===")
        self.socket = socket
        self.socket.readyRead.connect(self.read_data)
        self.buffer = b""
        self.current_admin = None
        self.current_user_role = None

    def read_data(self):
        print("=== Получены данные ===")
        self.buffer += self.socket.readAll().data()
        try:
            request = json.loads(self.buffer.decode('utf-8'))
            self.buffer = b""
            response = self.process_request(request)
            self.socket.write(json.dumps(response).encode('utf-8'))
            self.socket.flush()
        except json.JSONDecodeError:
            print("=== Ошибка JSON ===")
            pass

    def process_request(self, request):
        action = request.get("action")
        print("=== обработка:", action)
        handlers = {
            "login":       self.handle_login,
            "get_users":   self.handle_get_users,
            "create_user": self.handle_create_user,
            "update_user": self.handle_update_user,
            "delete_user": self.handle_delete_user,
            "get_audit":   self.handle_get_audit,
        }
        handler = handlers.get(action)
        if handler:
            return handler(request)
        return {"success": False, "error": "Неизвестная команда"}

    def handle_login(self, req):
        user = database.find_user(req["login"], hash_password(req["password"]))
        if user:
            self.current_admin = req["login"]
            self.current_user_role = database.get_user_role(req["login"])
            return {"success": True, "user_id": user[0], "full_name": user[1], "position": user[2], "role": self.current_user_role}
        return {"success": False, "error": "Неверный логин или пароль"}

    def handle_get_users(self, req):
        users = database.get_all_users()
        return {"success": True, "users": users}

    def handle_create_user(self, req):
        if self.current_user_role != 'admin':
            return {"success": False, "error": "Нет прав"}
        password = req.get("password")
        if not password:
            return {"success": False, "error":" Обязательно заполните поле"}
        try:
            role = req.get("role", "user")
            database.create_user(
                req["login"], hash_password("password"),
                req["full_name"], req.get("position", ""), req.get("phone", ""), role
            )
            database.log_action(self.current_admin, "create_user", req["login"])
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def handle_update_user(self, req):
        if self.current_user_role != 'admin':
            return {"success": False, "error": "Нет прав"}
        try:
            database.update_user(req["id"], req["full_name"], req.get("position",""), req.get("phone",""), req["is_active"])
            database.log_action(self.current_admin, "update_user", req.get("login",""))
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def handle_delete_user(self, req):
        if self.current_user_role != 'admin':
            return {"success": False, "error": "Нет прав"}
        try:
            database.deactivate_user(req["id"])
            database.log_action(self.current_admin, "delete_user", req.get("login",""))
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def handle_get_audit(self, req):
        if self.current_user_role != 'admin':
            return {"success": False, "error": "Нет прав"}
        logs = database.get_audit_logs()
        for log in logs:
            if 'created_at' in log and log['created_at']:
               log['created_at'] = str(log['created_at'])
        return {"success": True, "audit": logs}
