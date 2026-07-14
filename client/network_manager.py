import json
from PyQt5.QtNetwork import QTcpSocket, QHostAddress
from PyQt5.QtWidgets import QMessageBox

PORT = 5555

class NetworkManager:
    def __init__(self):
        self.socket = QTcpSocket()
        self.response_callback = None

    def connect_to_server(self):
        self.socket.connectToHost(QHostAddress.LocalHost, PORT)
        return self.socket.waitForConnected(3000)

    def send(self, data, callback):
        self.response_callback = callback
        self.socket.readyRead.connect(self._on_ready_read)
        self.socket.write(json.dumps(data).encode('utf-8'))
        self.socket.flush()

    def _on_ready_read(self):
        self.socket.readyRead.disconnect(self._on_ready_read)
        raw = self.socket.readAll().data().decode('utf-8')
        if self.response_callback:
            self.response_callback(json.loads(raw))