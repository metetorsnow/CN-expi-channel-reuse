
import sys
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtNetwork import QTcpServer,QTcpSocket, QHostAddress
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMainWindow
from ui import client
class Client(QMainWindow,client.Ui_MainWindow):
    def __init__(self):
        super(Client, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Client")
        self.socklow = QTcpSocket(self)
        self.sockhigh = QTcpSocket(self)
        self.sockmedium = QTcpSocket(self)
        self.socklow.connectToHost(QHostAddress.LocalHost, 6666)
        self.sockmedium.connectToHost(QHostAddress.LocalHost, 6667)
        self.sockhigh.connectToHost(QHostAddress.LocalHost, 6668)
        self.socklow.connected.connect(lambda :self.textBrowser.append("低频连接就绪"))
        self.sockmedium.connected.connect(lambda :self.textBrowser.append("中频连接就绪"))
        self.sockhigh.connected.connect(lambda :self.textBrowser.append("高频连接就绪"))
        self.serverlow = QTcpServer(self)
        self.servermedium = QTcpServer(self)
        self.serverhigh = QTcpServer(self)
        self.sockets = []
        if not self.serverlow.listen(QHostAddress.LocalHost, 9000):
            print(self.serverlow.errorString())
        if not self.servermedium.listen(QHostAddress.LocalHost, 9001):
            print(self.servermedium.errorString())
        if not self.serverhigh.listen(QHostAddress.LocalHost, 9002):
            print(self.serverhigh.errorString())
        self.serverlow.newConnection.connect(lambda: self.new_socket_slot(self.serverlow, 9000))
        self.servermedium.newConnection.connect(lambda: self.new_socket_slot(self.servermedium, 9001))
        self.serverhigh.newConnection.connect(lambda: self.new_socket_slot(self.serverhigh, 9002))
    def new_socket_slot(self,server,port):
        sock = server.nextPendingConnection()
        self.sockets.append(sock)
        sock.readyRead.connect(lambda: self.send_to_server(sock.readAll(),port))
        sock.disconnected.connect(sock.close)
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
        self.serverlow.close()
        self.servermedium.close()
        self.serverhigh.close()
        self.socklow.close()
        self.sockmedium.close()
        self.sockhigh.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Client()
    demo.move(1100,50)
    demo.show()
    sys.exit(app.exec_())