import sys
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtNetwork import QTcpServer,QTcpSocket, QHostAddress
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMainWindow
import ctypes
from ui import receiver



class Receiver(QMainWindow,receiver.Ui_MainWindow):
    def __init__(self,code,port):
        super(Receiver, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("receiver")
        self.port=port
        self.code=code
        self.sock=None
        c=""
        for i in code:
            c+=" "+str(i)
        self.label.setText("持有码片向量:"+c)
        self.textBrowser.append("这里是状态栏🔍")
        self.server = QTcpServer(self)
        if not self.server.listen(QHostAddress.LocalHost, 9000):
            print(self.server.errorString())
        self.server.newConnection.connect(self.new_socket_slot)

    def new_socket_slot(self):
        self.textBrowser.append("连接已就绪，接收信号")
        sock = self.server.nextPendingConnection()
        self.sock=sock
        sock.readyRead.connect(lambda: self.signal_to_str(sock.readAll()))
        sock.disconnected.connect(sock.close)
    def signal_to_str(self,data):
        string=""
        s = [ctypes.c_byte(i).value for i in data.data()]
        self.textBrowser.append("信号如下:\n"+str(s))
        self.textBrowser.append("二进制解码如下")
        begin=0
        while begin<len(s):
            b=""
            self.sign = 0
            for i in range(8):
                self.sign = 0
                for j in range(8):
                    self.sign+=self.code[j]*s[begin+j]
                if self.sign==0:
                    break
                begin+=8
                b+=("1" if self.sign>0 else "0")
            if self.sign == 0:
                break
            string+=chr(int(b,2))
            self.textBrowser.append(b)
        self.textBrowser.append("信息接收完毕")
        self.lineEdit.setText("收到信息:"+string)
    def closeEvent(self, event):
        self.server.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    rcv=Receiver([1,1,1,1,-1,-1,-1,-1],9000)
    rcv.move(1300,300)
    rcv.show()
    sys.exit(app.exec_())