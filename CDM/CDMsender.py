import sys
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtNetwork import QTcpServer,QTcpSocket, QHostAddress
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMainWindow,QMessageBox
from ui import sender

class user(QMainWindow,sender.Ui_MainWindow):
    def __init__(self,code,port):
        super(user, self).__init__()
        self.setupUi(self)
        self.port=port
        self.code=code
        self.sockets=[]

        self.pushButton.clicked.connect(lambda :self.send_data())
    def send_data(self):
        if not self.lineEdit.text().isascii() or self.lineEdit.text()=='':
            QMessageBox.warning(self, "warning", "输入有误")
            return
        self.signal=self.str_to_signal(self.lineEdit.text())
        self.sock = QTcpSocket(self)
        self.sockets.append(self.sock)
        self.sock.connectToHost(QHostAddress.LocalHost, self.port)
        self.sock.connected.connect(lambda: self.sock.write(self.signal))

    def str_to_signal(self,string):
        for c in string:
            ch=bin(ord(c))[2:].zfill(8)

    def closeEvent(self, event):
        for i in self.sockets:
            i.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    a=user([1,1,1,1,-1,-1,-1,-1],6666)
    a.setWindowTitle("senderA1")
    a.label.setText("A1码片向量:+1 +1 +1 +1 -1 -1 -1 -1")
    a.move(50, 80)
    a.show()
    b = user([-1,-1,1,1,-1,-1,1,1],6667)
    b.setWindowTitle("senderB1")
    b.label.setText("B1码片向量:-1 -1 +1 +1 -1 -1 +1 +1")
    b.move(50, 400)
    b.show()
    c = user([1,1,-1,-1,-1,-1,1,1],6668)
    c.setWindowTitle("senderC1")
    c.label.setText("C1码片向量:+1 +1 -1 -1 -1 -1 +1 +1")
    c.move(50, 700)
    c.show()
    sys.exit(app.exec_())