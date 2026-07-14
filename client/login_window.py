from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QMessageBox

class LoginWindow(QDialog):
    def __init__(self, network):
        super().__init__()
        self.network = network
        self.setWindowTitle("Вход в систему")
        self.resize(300, 150)

        layout = QFormLayout()
        self.login_edit = QLineEdit()
        self.pass_edit = QLineEdit()
        self.pass_edit.setEchoMode(QLineEdit.Password)

        layout.addRow("Логин:", self.login_edit)
        layout.addRow("Пароль:", self.pass_edit)

        self.btn = QPushButton("Войти")
        self.btn.clicked.connect(self.try_login)
        layout.addRow(self.btn)
        self.setLayout(layout)

    def try_login(self):
        def on_response(resp):
            print("===  Получен ответ:", resp)
            if resp.get("success"):
                self.user_role = resp.get("role", "user")
                self.accept()
            else:
                QMessageBox.warning(self, "Ошибка", resp.get("error"))

        self.network.send({
            "action": "login",
            "login": self.login_edit.text(),
            "password": self.pass_edit.text()
        }, on_response)
