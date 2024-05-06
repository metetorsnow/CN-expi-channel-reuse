import sys
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtNetwork import QTcpServer,QTcpSocket, QHostAddress
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMainWindow,QMessageBox
from ui import user_send



class user(QMainWindow,user_send.Ui_MainWindow):
    def __init__(self,user_from):
        super(user, self).__init__()
        self.setupUi(self)

        self.user_from=user_from
        self.sockets=[]

        self.pushButton.clicked.connect(lambda :self.send_data())
    def send_data(self):
        frequence=int(self.lineEdit_2.text()) if self.lineEdit_2.text()!="" else 0
        if frequence>=20 and frequence<=120:
            self.sock = QTcpSocket(self)
            self.sockets.append(self.sock)
            self.sock.connectToHost(QHostAddress.LocalHost, 9000)
            self.sock.connected.connect(lambda: self.sock.write((self.user_from + ":" + self.lineEdit.text()).encode()))
        elif frequence>=200 and frequence<=500:
            self.sock = QTcpSocket(self)
            self.sockets.append(self.sock)
            self.sock.connectToHost(QHostAddress.LocalHost, 9001)
            self.sock.connected.connect(lambda: self.sock.write((self.user_from + ":" + self.lineEdit.text()).encode()))
        elif frequence>=800 and frequence<=1200:
            self.sock = QTcpSocket(self)
            self.sockets.append(self.sock)
            self.sock.connectToHost(QHostAddress.LocalHost, 9002)
            self.sock.connected.connect(lambda: self.sock.write((self.user_from + ":" + self.lineEdit.text()).encode()))
        else:
            QMessageBox.warning(self,"warning","频率有误")


    def closeEvent(self, event):
        for i in self.sockets:
            i.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    a=user("A")
    a.setWindowTitle("userA1")
    a.move(50, 80)
    a.show()
    b = user("B")
    b.setWindowTitle("userB1")
    b.move(50, 400)
    b.show()
    c = user("C")
    c.setWindowTitle("userC1")
    c.move(50, 700)
    c.show()
    sys.exit(app.exec_())