from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QMessageBox, QComboBox

class AddUserDialog(QDialog):
    def __init__(self, network):
        super().__init__()
        self.network = network
        self.setWindowTitle("Новый пользователь")
        self.resize(300, 250)

        layout = QFormLayout()
        self.login = QLineEdit()
        self.password = QLineEdit()
        self.name = QLineEdit()
        self.position = QLineEdit()
        self.phone = QLineEdit()

        layout.addRow("Логин:", self.login)
        layout.addRow("Пароль:", self.password)
        layout.addRow("ФИО:", self.name)
        layout.addRow("Должность:", self.position)
        layout.addRow("Телефон:", self.phone)
        self.role_combo = QComboBox()
        self.role_combo.addItems(["user", "admin"])
        layout.addRow("Роль:", self.role_combo)

        self.btn = QPushButton("Создать")
        self.btn.clicked.connect(self.create)
        layout.addRow(self.btn)
        self.setLayout(layout)

    def create(self):
        def on_response(resp):
            if resp.get("success"):
                self.accept()
            else:
                QMessageBox.warning(self, "Ошибка", resp.get("error"))
        if not self.password.text():
            QMessageBox.warning(self, "Ошибка", "Пароль обязателен для заполнения")
            return

        self.network.send({
            "action": "create_user",
            "login": self.login.text(),
            "password": self.password.text(),
            "full_name": self.name.text(),
            "position": self.position.text(),
            "phone": self.phone.text(),
            "role": self.role_combo.currentText()
        }, on_response)
