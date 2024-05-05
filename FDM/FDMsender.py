import sys
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtNetwork import QTcpServer,QTcpSocket, QHostAddress
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMainWindow
from ui import user_send



class user(QMainWindow,user_send.Ui_MainWindow):
    def __init__(self,port):
        super(user, self).__init__()
        self.setupUi(self)
        self.label.setText("输入数据发送")
        self.sock = QTcpSocket(self)
        self.sock.connectToHost(QHostAddress.LocalHost, port)
        self.pushButton.clicked.connect(lambda :self.sock.write(self.lineEdit.text().encode()))

    def closeEvent(self, event):
        self.sock.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    a=user(9000)
    a.setWindowTitle("userA1")
    a.move(200, 400)
    a.show()
    b = user(9001)
    b.setWindowTitle("userB1")
    b.move(800, 400)
    b.show()
    c = user(9002)
    c.setWindowTitle("userC1")
    c.move(1400, 400)
    c.show()
    sys.exit(app.exec_())