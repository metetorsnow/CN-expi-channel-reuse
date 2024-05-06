import sys
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtNetwork import QTcpServer,QTcpSocket, QHostAddress
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMainWindow
from ui import user_accept


def new_socket_slot(win, server, line):
    win.sock = server.nextPendingConnection()
    sock=win.sock
    win.label.setText(f"已接收到 {win.count} 条信息")
    win.count+=1
    sock.readyRead.connect(lambda: line.setText(sock.readAll().data().decode()[2:]))
    sock.disconnected.connect(sock.close)
class user(QMainWindow,user_accept.Ui_MainWindow):
    def __init__(self,port):
        super(user, self).__init__()
        self.setupUi(self)
        self.server = QTcpServer(self)
        self.count=1
        if not self.server.listen(QHostAddress.LocalHost, port):
            print(self.server.errorString())
        self.server.newConnection.connect(lambda: new_socket_slot(self,self.server, self.lineEdit))

    def closeEvent(self, event):
        self.server.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    a=user(7777)
    a.setWindowTitle("userA2")
    a.move(550, 80)
    a.show()
    b = user(7778)
    b.setWindowTitle("userB2")
    b.move(550, 400)
    b.show()
    c = user(7779)
    c.setWindowTitle("userC2")
    c.move(550, 700)
    c.show()
    sys.exit(app.exec_())