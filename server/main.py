import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtNetwork import QTcpServer, QHostAddress
from common import PORT
from clienthandler import ClientHandler
import database

class ServerApp:
    def __init__(self):
        self.server = QTcpServer()
        self.server.newConnection.connect(self.on_new_connection)
        self.clients = []

    def start(self):
        if not self.server.listen(QHostAddress.AnyIPv4, PORT):
            print("Ошибка: {}".format(self.server.errorString()))
            sys.exit(1)
        print("Сервер запущен на порту {}".format(PORT))

    def on_new_connection(self):
        socket = self.server.nextPendingConnection()
        handler =  ClientHandler(socket)
        self.clients.append(handler)
        print("Клиент подлючен. Всего  клиентов: {}".format(len(self.clients)))

if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    database.init_db()
    server = ServerApp()
    server.start()
    sys.exit(app.exec_())
