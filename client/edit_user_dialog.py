from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QMessageBox, QCheckBox

class EditUserDialog(QDialog):
    def __init__(self, network, user_data):
        super().__init__()
        self.network = network
        self.user_data = user_data
        self.setWindowTitle("Редактировать пользователя")
        self.resize(300, 250)

        layout = QFormLayout()

        self.login = QLineEdit()
        self.login.setText(user_data.get("login", ""))
        self.login.setReadOnly(True)

        self.name = QLineEdit()
        self.name.setText(user_data.get("full_name", ""))

        self.position = QLineEdit()
        self.position.setText(user_data.get("position", ""))

        self.phone = QLineEdit()
        self.phone.setText(user_data.get("phone", ""))

        self.is_active = QCheckBox()
        self.is_active.setChecked(user_data.get("is_active", True))

        layout.addRow("Логин:", self.login)
        layout.addRow("ФИО:", self.name)
        layout.addRow("Должность:", self.position)
        layout.addRow("Телефон:", self.phone)
        layout.addRow("Активен:", self.is_active)

        self.btn = QPushButton("Сохранить")
        self.btn.clicked.connect(self.save)
        layout.addRow(self.btn)
        self.setLayout(layout)

    def save(self):
        def on_response(resp):
            if resp.get("success"):
                self.accept()
            else:
                QMessageBox.warning(self, "Ошибка", resp.get("error"))
        self.network.send({
            "action": "update_user",
            "id": self.user_data["id"],
            "login": self.user_data["login"],
            "full_name": self.name.text(),
            "position": self.position.text(),
            "phone": self.phone.text(),
            "is_active": self.is_active.isChecked()
        }, on_response)







