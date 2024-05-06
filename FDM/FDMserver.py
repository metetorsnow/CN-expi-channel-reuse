
import sys
import time
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtNetwork import QTcpServer,QTcpSocket, QHostAddress
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMainWindow
from ui import FMDs
class Server(QMainWindow,FMDs.Ui_MainWindow):
    def __init__(self):
        super(Server, self).__init__()
        self.setupUi(self)
        self.serverlow = QTcpServer(self)
        self.servermedium = QTcpServer(self)
        self.serverhigh = QTcpServer(self)
        self.sockets=[]
        if not self.serverlow.listen(QHostAddress.LocalHost, 6666):
            print(self.serverlow.errorString())
        if not self.servermedium.listen(QHostAddress.LocalHost, 6667):
            print(self.servermedium.errorString())
        if not self.serverhigh.listen(QHostAddress.LocalHost, 6668):
            print(self.serverhigh.errorString())
        self.serverlow.newConnection.connect(lambda :self.new_socket_slot(self.serverlow,self.lineEdit))
        self.servermedium.newConnection.connect(lambda: self.new_socket_slot(self.servermedium,self.lineEdit_2))
        self.serverhigh.newConnection.connect(lambda: self.new_socket_slot(self.serverhigh,self.lineEdit_3))
    def new_socket_slot(self,server,line):
        sock = server.nextPendingConnection()
        self.sockets.append(sock)
        sock.readyRead.connect(lambda: self.send_to_user(sock.readAll(),line))
        sock.disconnected.connect(sock.close)
    def send_to_user(self,data,line):
        sock = QTcpSocket(self)
        self.sockets.append(sock)
        message=data.data().decode()
        line.setText(message)
        tag=message[0]
        if tag=="A":
            sock.connectToHost(QHostAddress.LocalHost,7777)
        elif tag=="B":
            sock.connectToHost(QHostAddress.LocalHost, 7778)
        else:
            sock.connectToHost(QHostAddress.LocalHost, 7779)
        sock.connected.connect(lambda: sock.write(data))
    def closeEvent(self, event):
        self.serverlow.close()
        self.servermedium.close()
        self.serverhigh.close()
        for i in self.sockets:
            i.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Server()
    demo.move(1100, 650)
    demo.setWindowTitle("Server")
    demo.show()
    sys.exit(app.exec_())