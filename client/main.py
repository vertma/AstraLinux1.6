import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from network_manager import NetworkManager
from login_window import LoginWindow
from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    network = NetworkManager()
    if not network.connect_to_server():
        QMessageBox.critical(None, "Ошибка", "Сервер не запущен!")
        sys.exit(1)

    login_win = LoginWindow(network)
    if login_win.exec_():
        user_role = login_win.user_role if hasattr(login_win, 'user_role') else 'user'
        main_win = MainWindow(network, user_role)
        main_win.show()
        sys.exit(app.exec_())
