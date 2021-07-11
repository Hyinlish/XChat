#!/usr/bin/python
# -*- coding: UTF-8 -*-

from socket import *             # 导入 socket 模块
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui import U_MainWindow
import sys
import _thread

host = ''
true_meg = 'Send successfully!'
my_frd = {}
setlist = []
Normal = QColor(250,250,250)
Green = QColor(0,250,0)
Red = QColor(250,0,0)

#读取朋友信息
box = open('Friend','r')
obj_1 = box.read()
obj_2 = obj_1.split(':')
for i in range(0,len(obj_2),2):
    obj_3 = obj_2[i]
    cmd = 'my_frd.update(' + obj_3 + '=' + obj_2[i+1] + ')'
    exec(cmd)
my_keys = my_frd.keys()
box.close()

#发送消息
def Send_Meg():
    try:
        s = socket()
        host = my_frd.get(ui.otherBox.currentText())
        s.connect((host, 8000))
        try:
            meg = ui.megEdit.toPlainText()
            s.send(meg.encode())
            ui.yourMeg.setText(meg)
            ui.Output.setTextColor(Green)
            ui.Output.setText(true_meg)
        except:
            ui.Output.setText('Unknown fault')
    except:
        ui.Output.setTextColor(Red)
        ui.Output.setText('Connection refused.')
#更新朋友列表
def Box_Update():
    ui.otherBox.clear()
    ui.otherBox.addItems(my_keys)

#服务端进程
def Server():
    t = socket()                # 创建 socket 对象
    port = 8086                 # 设置端口
    host = my_frd.get('Me')
    t.bind((host, port))        # 绑定端口
    t.listen(5)                 # 等待客户端连接
    while True:
        d,addr_2 = t.accept()     # 建立客户端连接
        f = d.recv(1024)
        ui.otherBox.setText(f.decode())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = U_MainWindow.Ui_MainWindow()
    ui.setupUi(MainWindow)

    Box_Update()
    ui.sendButton.clicked.connect(Send_Meg)         
    ui.exitButton.clicked.connect(sys.exit)
    ui.Output.setTextColor(Normal)      

    MainWindow.show()

    _thread.start_new_thread(Server,())
    sys.exit(app.exec())
    
    
    
