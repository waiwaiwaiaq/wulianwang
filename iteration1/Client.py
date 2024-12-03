import socket
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MainWin(QMainWindow):
    def __init__(self, parent=None):
        super(MainWin, self).__init__(parent)
        self.pc = None
        self.MainWindow()
        self.Arrangement()
        self.Componets()

    def getHostIP(self):
        self.IP_info.setText(socket.gethostbyname_ex(socket.gethostname())[-1][-1])
    
    def MainWindow(self):
        self.setWindowTitle("客户端")
        self.setFixedSize(1000, 600)

    # 布局
    def Arrangement(self):
        self.centerWidget = QWidget()
        self.mainLayout = QGridLayout()
        self.NE = QGridLayout()
        self.SE = QGridLayout()
        self.Settings = QGroupBox("设置")
        self.Function = QGroupBox("功能")

        # IP、端口、服务端设置
        self.IP_info = QLineEdit()
        self.IP_info.setText('127.0.0.1')
        self.IP_info.setAlignment(Qt.AlignCenter)
        self.hostIP_info = QPushButton("获得本机IP")
        self.hostIP_info.clicked.connect(self.getHostIP)
        self.port_info = QLineEdit()
        self.port_info.setText("8081")
        self.port_info.setAlignment(Qt.AlignCenter)
        self.hostname_info = QLineEdit()
        self.hostname_info.setText("客户端")
        self.hostname_info.setAlignment(Qt.AlignCenter)

        # 聊天界面设置
        self.Chat = QTextEdit()
        self.Input = QTextEdit()
        self.Send_info = QPushButton("发送")
        self.Send_info.clicked.connect(self.sendInfo)

        # 功能模块
        self.Connect = QPushButton("连接服务器")
        self.Connect.clicked.connect(self.setClient)
        self.Quit = QPushButton("退出")
        self.Quit.clicked.connect(self.quit)
        self.statusBar = QStatusBar()

    # 组装控件
    def Componets(self):
        self.setCentralWidget(self.centerWidget)
        self.setStatusBar(self.statusBar)
        self.centerWidget.setLayout(self.mainLayout)
        self.Settings.setLayout(self.NE)
        self.Function.setLayout(self.SE)

        self.mainLayout.addWidget(self.Chat, 0, 2, 6, 2)
        self.mainLayout.addWidget(self.Input, 6, 2, 2, 2)
        self.mainLayout.addWidget(self.Send_info, 8, 2, 1, 2)
        self.mainLayout.addWidget(self.Settings, 0, 0, 5, 1)
        self.mainLayout.addWidget(self.Function, 5, 0, 3, 1)
        self.NE.addWidget(QLabel("IP"), 0, 0, 1, 2)
        self.NE.addWidget(self.IP_info, 0, 1, 1, 2)
        self.NE.addWidget(self.hostIP_info, 0, 3, 1, 1)
        self.NE.addWidget(QLabel("端口"), 1, 0, 1, 1)
        self.NE.addWidget(self.port_info, 1, 1, 1, 2)
        self.NE.addWidget(QLabel("用户名"), 2, 0, 1, 1)
        self.NE.addWidget(self.hostname_info, 2, 1, 1, 2)
        self.SE.addWidget(self.Connect, 0, 2, 1, 1)
        self.SE.addWidget(self.Quit, 1, 2, 1, 1)

    # 信息显示
    def sendInfo(self):
        info = self.Input.toPlainText()
        self.Input.clear()
        info = self.pc.hostName + ": " + info
        self.pc.btnsend(info)

    # 本主机客户端
    def setClient(self):
        host = self.hostname_info.text()
        port = self.port_info.text()
        ip = self.IP_info.text()
        self.pc = Client(self, ip, host, int(port))

    def quit(self):
        if self.pc != None:
            self.pc.closeThread()
        self.close()


# 客户端
class Client():
    def __init__(self, widget, ip, hostName, port):
        self.widget = widget
        self.ip = ip
        self.hostName = hostName
        self.port = port
        self.buildSocket()

    # 设置Socket
    def buildSocket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buildClient()

    # 初始化客户端
    def buildClient(self):
        self.client = ClientThread(self.socket)
        self.client._flag.connect(self.getFlag)
        self.client._signal.connect(self.getMessage)
        self.client._text.connect(self.getText)
        if self.client.connectServer(self.ip, self.port):
            self.client.start()

    def sendToServer(self, text):
        self.socket.send((text + "\n").encode('utf-8'))

    def btnsend(self, text):
        self.sendToServer(text)

    def closeThread(self):
        self.runflag = False

    def getFlag(self, flag):
        if flag == "connect":
            self.widget.statusBar.showMessage("connect success!!")
        elif flag == "disconnect":
            self.client.runflag = False

    def getMessage(self, signal):
        self.widget.statusBar.showMessage(signal)

    def getText(self, text):
        print("111" + text)
        self.widget.Chat.append(text + "\n")


class ClientThread(QThread):
    _signal = pyqtSignal(str)
    _text = pyqtSignal(str)
    _flag = pyqtSignal(str)

    def __init__(self, serverSocket):
        super(ClientThread, self).__init__()
        self.serverSocket = serverSocket
        self.runflag = True
        self.connectList = ["connect", "disconnect"]

    def connectServer(self, ip, port):
        self.serverSocket.connect((ip, port))
        self.sendFlag(0)
        return True

    def run(self):
        while self.runflag:
            msg = self.serverSocket.recv(1024).decode("utf-8")
            self.sendText(msg)

    def sendMessage(self, message):
        self._signal.emit(str(message))

    def sendText(self, text):
        self._text.emit(str(text))

    def sendFlag(self, flagIndex):
        self._flag.emit(str(self.connectList[flagIndex]))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec_())