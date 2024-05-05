import sys
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtNetwork import QTcpServer,QTcpSocket, QHostAddress
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMainWindow
from ui import user_accept


def new_socket_slot(win, server, line):
    win.sock = server.nextPendingConnection()
    sock=win.sock
    print("yes")
    sock.readyRead.connect(lambda: line.setText(sock.readAll().data().decode()))
    sock.disconnected.connect(sock.close)
class user(QMainWindow,user_accept.Ui_MainWindow):
    def __init__(self,port):
        super(user, self).__init__()
        self.setupUi(self)
        self.label.setText("等待接收数据")
        self.server = QTcpServer(self)
        if not self.server.listen(QHostAddress.LocalHost, port):
            print(self.server.errorString())
        self.server.newConnection.connect(lambda: new_socket_slot(self,self.server, self.lineEdit))

    def closeEvent(self, event):
        self.server.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    a=user(7777)
    a.setWindowTitle("A")
    a.move(200, 0)
    a.show()
    b = user(7778)
    b.setWindowTitle("B")
    b.move(800, 0)
    b.show()
    c = user(7779)
    c.setWindowTitle("C")
    c.move(1400, 0)
    c.show()
    sys.exit(app.exec_())