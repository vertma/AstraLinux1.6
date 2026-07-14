from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from PyQt5.QtWidgets import QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from user_dialog import AddUserDialog
from edit_user_dialog import EditUserDialog

class MainWindow(QMainWindow):
    def __init__(self, network, user_role='user'):
        super().__init__()
        self.network = network
        self.user_role = user_role
        self.setWindowTitle("Управление пользователями")
        self.resize(900, 600)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Логин", "ФИО", "Должность", "Телефон", "Роль", "Активен"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по логину или ФИО")
        self.search_input.textChanged.connect(self.filter_table)

        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Поиск:"))
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        layout.addWidget(self.table)
        btn_layout = QHBoxLayout()
        self.btn_refresh = QPushButton("Обновить")
        self.btn_refresh.clicked.connect(self.load_users)
        btn_layout.addWidget(self.btn_refresh)

        self.btn_add = QPushButton("Добавить")
        self.btn_add.clicked.connect(self.add_user)
        btn_layout.addWidget(self.btn_add)

        self.btn_edit = QPushButton("Редактировать")
        self.btn_edit.clicked.connect(self.edit_user)
        btn_layout.addWidget(self.btn_edit)

        self.btn_delete = QPushButton("Удалить")
        self.btn_delete.clicked.connect(self.delete_user)
        btn_layout.addWidget(self.btn_delete)

        self.btn_audit = QPushButton("Журнал аудита")
        self.btn_audit.clicked.connect(self.show_audit)
        btn_layout.addWidget(self.btn_audit)

        layout.addLayout(btn_layout)

        if self.user_role != 'admin':
            self.btn_add.setVisible(False)
            self.btn_edit.setVisible(False)
            self.btn_delete.setVisible(False)
            self.btn_audit.setVisible(False)

        self.load_users()


    def load_users(self):
        def on_response(resp):
            if resp.get("success"):
                users = resp.get("users", [])
                self.table.setRowCount(len(users))
                for row, u in enumerate(users):
                    self.table.setItem(row, 0, QTableWidgetItem(str(u.get("id", ""))))
                    self.table.setItem(row, 1, QTableWidgetItem(u.get("login", "")))
                    self.table.setItem(row, 2, QTableWidgetItem(u.get("full_name", "")))
                    self.table.setItem(row, 3, QTableWidgetItem(u.get("position", "")))
                    self.table.setItem(row, 4, QTableWidgetItem(u.get("phone", "")))
                    self.table.setItem(row, 5, QTableWidgetItem(u.get("role", "user")))
                    is_active_val = u.get("is_active", True)
                    if is_active_val == True or is_active_val == "t" or is_active_val == "Да" or is_active_val == 1:
                        active_text = "Да"
                    else:
                        active_text = "Нет"
                    self.table.setItem(row, 6, QTableWidgetItem(active_text))
            else:
                QMessageBox.warning(self, "Ошибка", resp.get("error", "Ошибка"))
        self.network.send({"action": "get_users"}, on_response)

    def add_user(self):
        dialog = AddUserDialog(self.network)
        if dialog.exec_():
            self.load_users()

    def show_audit(self):
        def on_response(resp):
            if resp.get("success"):
                text = "Админ | Действие | Цель | Время\n" + "-"*50 + "\n"
                for log in resp["audit"]:
                    text += "{} | {} | {} | {}\n".format(
                        log['admin_login'], log['action'], log['target_login'], log['created_at']
                    )
                QMessageBox.information(self, "Журнал аудита", text)

        self.network.send({"action": "get_audit"}, on_response)

    def get_selected_user(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Выберите пользователя в таблице")
            return None

        return {
            "id": int(self.table.item(row, 0).text()),
            "login": self.table.item(row, 1).text(),
            "full_name": self.table.item(row, 2).text(),
            "position": self.table.item(row, 3).text(),
            "phone": self.table.item(row, 4).text(),
            "role": self.table.item(row, 5).text(),
            "is_active": self.table.item(row, 6).text() == "Да"
        }

    def edit_user(self):
        user = self.get_selected_user()
        if not user:
            return

        dialog = EditUserDialog(self.network, user)
        if dialog.exec_():
            self.load_users()

    def delete_user(self):
        user = self.get_selected_user()
        if not user:
            return

        reply = QMessageBox.question(
            self, "Подтверждение", "Уверены, что хотите удалить пользователя {}?".format(user["login"]), QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            def on_response(resp):
                if resp.get("success"):
                    self.load_users()
                else:
                    QMessageBox.warning(self, "Ошибка", resp.get("error"))

            self.network.send({
                "action": "delete_user", "id": user["id"], "login": user["login"]
            }, on_response)

    def filter_table(self):
        query = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            login = self.table.item(row, 1).text().lower() if self.table.item(row, 1) else ""
            full_name = self.table.item(row, 2).text().lower() if self.table.item(row, 2) else ""

            if query in login or  query in full_name or query == "":
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)

