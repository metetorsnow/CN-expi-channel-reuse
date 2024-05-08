import sys
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtNetwork import QTcpServer,QTcpSocket, QHostAddress
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMainWindow
from ui import channel
import ctypes

class Channel(QMainWindow,channel.Ui_MainWindow):
    def __init__(self):
        super(Channel, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Channel")
        self.serverA = QTcpServer(self)
        self.serverB = QTcpServer(self)
        self.serverC = QTcpServer(self)
        self.sockets = []
        self.codeA=[]
        self.codeB = []
        self.codeC = []
        self.signal=[]
        self.signal_for_send = []
        if not self.serverA.listen(QHostAddress.LocalHost, 6666):
            print(self.serverA.errorString())
        if not self.serverB.listen(QHostAddress.LocalHost, 6667):
            print(self.serverB.errorString())
        if not self.serverC.listen(QHostAddress.LocalHost, 6668):
            print(self.serverC.errorString())
        self.serverA.newConnection.connect(lambda: self.new_socket_slot(self.serverA, "A"))
        self.serverB.newConnection.connect(lambda: self.new_socket_slot(self.serverB, "B"))
        self.serverC.newConnection.connect(lambda: self.new_socket_slot(self.serverC, "C"))
        self.pushButton_1.clicked.connect(self.calculate)
        self.pushButton_2.clicked.connect(self.wipe)
        self.pushButton_3.clicked.connect(self.send)
    def new_socket_slot(self,server,flow):
        sock = server.nextPendingConnection()
        self.sockets.append(sock)
        sock.readyRead.connect(lambda: (self.textBrowser.append("*收到用户"+flow+"的信号:"),
                                        self.read_data(sock.readAll(),flow)))
        sock.disconnected.connect(sock.close)

    def read_data(self,data,flow):
        if flow=="A":
            s=[ctypes.c_byte(i).value for i in data.data()]
            self.codeA+=s
            self.textBrowser.append(str(s))
        elif flow=="B":
            s = [ctypes.c_byte(i).value for i in data.data()]
            self.codeB += s
            self.textBrowser.append(str(s))
        else:
            s = [ctypes.c_byte(i).value for i in data.data()]
            self.codeC += s
            self.textBrowser.append(str(s))
    def calculate(self):
        length=max(len(self.codeA),len(self.codeB),len(self.codeC))
        self.signal=[0]*length
        for i in range(length):
            if i<len(self.codeA):
                self.signal[i]+=self.codeA[i]
            if i<len(self.codeB):
                self.signal[i]+=self.codeB[i]
            if i<len(self.codeC):
                self.signal[i]+=self.codeC[i]
        self.textBrowser.append("*信号计算完成:\n"+str(self.signal))

    def wipe(self):
        self.codeA=[]
        self.codeB = []
        self.codeC = []
        self.signal = []
        self.textBrowser.append("*所有信号和缓存已清空")

    def send(self):
        if not self.signal:
            self.textBrowser.append("*信号为空，无法发送")
            return
        self.sock = QTcpSocket(self)
        self.sockets.append(self.sock)
        self.sock.connectToHost(QHostAddress.LocalHost, 9000)
        self.signal_for_send=bytes([ctypes.c_ubyte(i).value for i in self.signal])
        self.sock.connected.connect(lambda: (self.sock.write(self.signal_for_send),
                                             self.textBrowser.append("*信号已发送")))
    def closeEvent(self, event):
        self.serverA.close()
        self.serverB.close()
        self.serverC.close()
        for i in self.sockets:
            i.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Channel()
    demo.move(600,150)
    demo.show()
    sys.exit(app.exec_())