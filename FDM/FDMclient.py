
import sys
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtNetwork import QTcpServer,QTcpSocket, QHostAddress
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMainWindow
from ui import FMDs
class Client(QMainWindow,FMDs.Ui_MainWindow):
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
        self.socklow.connected.connect(lambda :self.write_data(self.socklow))
        self.sockmedium.connected.connect(lambda :self.write_data(self.sockmedium))
        self.sockhigh.connected.connect(lambda :self.write_data(self.sockhigh))
    def write_data(self,sock):
        sock.write("yes!".encode())
        sock.write("yes!".encode())
    def closeEvent(self, event):
        self.socklow.close()
        self.sockmedium.close()
        self.sockhigh.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Client()
    demo.lineEdit.setText("cnm")
    demo.show()
    sys.exit(app.exec_())