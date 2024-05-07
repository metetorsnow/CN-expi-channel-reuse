import sys
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtNetwork import QTcpServer,QTcpSocket, QHostAddress
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMainWindow
from ui import channel

class Channel(QMainWindow,channel.Ui_MainWindow):
    def __init__(self):
        super(Channel, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Client")
        self.serverA = QTcpServer(self)
        self.serverB = QTcpServer(self)
        self.serverC = QTcpServer(self)
        self.sockets = []
        if not self.serverA.listen(QHostAddress.LocalHost, 6666):
            print(self.serverA.errorString())
        if not self.serverB.listen(QHostAddress.LocalHost, 6667):
            print(self.serverB.errorString())
        if not self.serverC.listen(QHostAddress.LocalHost, 6668):
            print(self.serverC.errorString())
        self.serverA.newConnection.connect(lambda: self.new_socket_slot(self.serverA, 6666))
        self.serverB.newConnection.connect(lambda: self.new_socket_slot(self.serverB, 6667))
        self.serverC.newConnection.connect(lambda: self.new_socket_slot(self.serverC, 6668))
    def new_socket_slot(self,server,port):
        sock = server.nextPendingConnection()
        self.sockets.append(sock)
        sock.readyRead.connect(lambda: (self.textBrowser.append("*收到端口"+str(port)+"连接"),
                                        self.read_data(sock.readAll())))
        sock.disconnected.connect(sock.close)

    def read_data(self,data):
        pass
    def send_to_server(self,data,port):
        if port==9000:
            self.textBrowser.append("*收到来自低频信息:\n"+data.data().decode())
            self.socklow.write(data)
        elif port==9001:
            self.textBrowser.append("*收到来自中频信息:\n" + data.data().decode())
            self.sockmedium.write(data)
        else:
            self.textBrowser.append("*收到来自高频信息:\n" + data.data().decode())
            self.sockhigh.write(data)
    def closeEvent(self, event):
        self.serverA.close()
        self.serverB.close()
        self.serverC.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Channel()
    demo.move(1100,50)
    demo.show()
    sys.exit(app.exec_())