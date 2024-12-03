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
        self.componentWidgets()

    def Find_self_Host(self):
        self.IP_info.setText(socket.gethostbyname_ex(socket.gethostname())[-1][-1])

    def MainWindow(self):
        self.setWindowTitle("服务端")
        self.setFixedSize(1000, 600)

    def Arrangement(self):
        self.NE = QGridLayout()
        self.SE = QGridLayout()
        self.centerWidget = QWidget()
        self.MainWidget = QGridLayout()
        self.Settings = QGroupBox("设置")
        self.Function = QGroupBox("功能")

        # IP、端口、服务端设置
        self.IP_info = QLineEdit()
        self.IP_info.setText('127.0.0.1')
        self.IP_info.setAlignment(Qt.AlignCenter)
        self.hostIP_info = QPushButton("当前IP")
        self.hostIP_info.clicked.connect(self.Find_self_Host)
        self.port_info = QLineEdit()
        self.port_info.setText("8081")
        self.port_info.setAlignment(Qt.AlignCenter)
        self.hostname_info = QLineEdit()
        self.hostname_info.setText("服务端")
        self.hostname_info.setAlignment(Qt.AlignCenter)
        self.Server_button = QRadioButton("服务端")
        self.Server_button.setChecked(True)

        # 聊天界面设置
        self.Chat = QTextEdit()
        self.Input = QTextEdit()
        self.Send_info = QPushButton("发送")
        self.Send_info.clicked.connect(self.sendInfo)

        # 功能模块
        self.Create = QPushButton("创建服务器")
        self.Create.clicked.connect(self.setServer)
        self.Quit_window = QPushButton("退出")
        self.Quit_window.clicked.connect(self.quit)
        self.statusBar = QStatusBar()

    # 布局设置
    def componentWidgets(self):
        self.setCentralWidget(self.centerWidget)
        self.setStatusBar(self.statusBar)
        self.centerWidget.setLayout(self.MainWidget)
        self.Settings.setLayout(self.NE)
        self.Function.setLayout(self.SE)

        self.MainWidget.addWidget(self.Chat, 0, 2, 6, 2)
        self.MainWidget.addWidget(self.Input, 6, 2, 2, 2)
        self.MainWidget.addWidget(self.Send_info, 8, 2, 1, 2)
        self.MainWidget.addWidget(self.Settings, 0, 0, 5, 1)
        self.MainWidget.addWidget(self.Function, 5, 0, 3, 1)
        self.NE.addWidget(QLabel("IP"), 0, 0, 1, 2)
        self.NE.addWidget(self.IP_info, 0, 1, 1, 2)
        self.NE.addWidget(self.hostIP_info, 0, 3, 1, 1)
        self.NE.addWidget(QLabel("端口"), 1, 0, 1, 1)
        self.NE.addWidget(self.port_info, 1, 1, 1, 2)
        self.NE.addWidget(QLabel("用户名"), 2, 0, 1, 1)
        self.NE.addWidget(self.hostname_info, 2, 1, 1, 2)
        self.SE.addWidget(self.Create, 0, 2, 1, 1)
        self.SE.addWidget(self.Quit_window, 1, 2, 1, 1)

    # 信息显示
    def sendInfo(self):
        info = self.Input.toPlainText()
        self.Input.clear()
        info = self.pc.hostName + ": " + info
        self.pc.Send_info(info)

    # 本主机服务器
    def setServer(self):
        host = self.hostname_info.text()
        port = self.port_info.text()
        ip = self.IP_info.text()
        self.pc = Server(self, ip, host, int(port))

    def quit(self):
        if self.pc != None:
            self.pc.closeThread()
        self.close()


# 服务端
class Server():
    def __init__(self, widget, ip, host, port):
        self.widget = widget
        self.ip = ip
        self.hostName = host
        self.port = port
        self.ServerName = {}
        self.serverID = 0
        self.buildSocket()

    # 设置Socket
    def buildSocket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.initialServer()

    # 初始化服务端
    def initialServer(self):
        self.socket.bind((self.ip, self.port))
        self.socket.listen(5)
        self.buildServer()

    # 创建新的服务线程
    def buildServer(self):
        server = ServerThread(str(self.serverID), self.socket)
        self.ServerName[str(self.serverID)] = server
        self.serverID += 1
        server._flag.connect(self.Connect_get)
        server._text.connect(self.getText)
        server.start()

    # 发送消息
    def Cast_info(self, info):
        for client in self.ServerName:
            if self.ServerName[client].ClientSocket != None:
                self.ServerName[client].sendToClient(info)

    def Send_info(self, text):
        text = text.replace("\n", "")
        self.widget.Chat.append(text + "\n")
        self.Cast_info(text)

    def closeThread(self):
        for server in self.ServerName:
            self.ServerName[server].runflag = False

    def Connect_get(self, flag):
        flag = flag.split("-----")
        if flag[1] == "connect":
            self.buildServer()
        elif flag[1] == "disconnect":
            self.ServerName[flag[0]].runflag = False

    def getText(self, text):
        text = text.replace("\n", "")
        self.widget.Chat.append(text + "\n")
        self.Cast_info(text)


# 对接客户端
class ServerThread(QThread):
    _text = pyqtSignal(str)
    _flag = pyqtSignal(str)

    def __init__(self, serverID, serverSocket):
        super(ServerThread, self).__init__()
        self.serverID = serverID
        self.serverSocket = serverSocket
        self.ClientSocket = None
        self.addr = None
        self.runflag = True

    # 等待连接
    def run(self):
        self.sendText("等待连接")
        self.ClientSocket, self.addr = self.serverSocket.accept()
        self.sendText("客户端已连接")
        self.getMessage()

    # 接收
    def getMessage(self):
        while self.runflag:
            data = self.ClientSocket.recv(1024).decode('utf-8')
            self.sendText(data)
        self.ClientSocket.close()

    def sendToClient(self, info):
        self.ClientSocket.send(info.encode("utf-8"))

    def sendText(self, text):
        self._text.emit(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec_())
