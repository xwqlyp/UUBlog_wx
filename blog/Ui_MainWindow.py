class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        @param parent reference to the parent widget
        @type QWidget
    """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

    # 在控制台中写入信息
    def outputWritten(self, text=None):
        # 获取文本框中文本的游标
        cursor = self.textEdit.textCursor()
        # 将游标位置移动到当前文本的结束处
        cursor.movePosition(QtGui.QTextCursor.End)
        # 写入文本
        cursor.insertText(text)
        # 设置文本的游标为创建了cursor
        self.textEdit.setTextCursor(cursor)
        self.textEdit.ensureCursorVisible()

    '''
            ItChat登陆功能
        '''

    @staticmethod
    def _show_message(message):
        print('{}'.format(message))

    # 获取群聊复选框选择状态
    def checkChatRoom(self, state):
        try:
            checkBox = self.sender()
            if state == Qt.Unchecked:
                self.outputWritten(u'取消选择了{0}: {1}\n'.format(checkBox.id_, checkBox.text()))
                self.chatroom_list.remove(self.chatroom_dict[checkBox.text()])
            elif state == Qt.Checked:
                self.outputWritten(u'选择了{0}: {1}\n'.format(checkBox.id_, checkBox.text()))
                self.chatroom_list.append(self.chatroom_dict[checkBox.text()])
        except Exception as e:
            self.outputWritten("获取群聊选择状态失败：{}\n".format(e))

    # 生成群聊列表
    def generate_chatroom(self, chatrooms):
        # 清空原有群里列表
        while self.gridLayout.count():
            item = self.gridLayout.takeAt(0)
            widget = item.widget()
            widget.deleteLater()

        chatrooms = chatrooms[0]
        self.chatroom_dict = dict()
        try:
            for c, i in zip(chatrooms, range(len(chatrooms))):
                print(c['NickName'], c['UserName'])
                checkbox = QCheckBox(c['NickName'])
                checkbox.id_ = i
                self.chatroom_dict[c['NickName']] = c['UserName']
                checkbox.stateChanged.connect(self.checkChatRoom)  # 1
                self.gridLayout.addWidget(checkbox)
                # self.horizontalLayout_3.addWidget(self.checkBox_2)
            self.outputWritten("生成群聊成功！\n")
        except Exception as e:
            print(e)

    # 生成好友列表
    def generate_friends(self, chatrooms):
        # 清空原有群里列表
        while self.verticalLayout_4.count():
            item = self.verticalLayout_4.takeAt(0)
            widget = item.widget()
            widget.deleteLater()
        chatrooms = chatrooms[1]
        self.chatroom_dict = dict()
        try:
            for c, i in zip(chatrooms, range(len(chatrooms))):
                print(c['NickName'], c['UserName'])
                checkbox = QCheckBox(c['NickName'])
                checkbox.id_ = i
                self.chatroom_dict[c['NickName']] = c['UserName']
                checkbox.stateChanged.connect(self.checkChatRoom)  # 1
                self.verticalLayout_4.addWidget(checkbox)
                # self.horizontalLayout_3.addWidget(self.checkBox_2)
            self.outputWritten("生成好友成功！\n")
        except Exception as e:
            print(e)

    # 生成公众号列表
    def generate_mps(self, chatrooms):
        # 清空原有群里列表
        while self.verticalLayout_6.count():
            item = self.verticalLayout_6.takeAt(0)
            widget = item.widget()
            widget.deleteLater()
        chatrooms = chatrooms[2]
        self.chatroom_dict = dict()
        try:
            for c, i in zip(chatrooms, range(len(chatrooms))):
                print(c['NickName'], c['UserName'])
                checkbox = QCheckBox(c['NickName'])
                checkbox.id_ = i
                self.chatroom_dict[c['NickName']] = c['UserName']
                checkbox.stateChanged.connect(self.checkChatRoom)  # 1
                self.verticalLayout_6.addWidget(checkbox)
                # self.horizontalLayout_3.addWidget(self.checkBox_2)
            self.outputWritten("生成公众号成功！\n")
        except Exception as e:
            print(e)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        # 登录微信 - 线程
        """

        # 登录微信 - 线程
        try:
            self.login_wechat_thread = LoginWechat(
                label=self.textEdit,
                scroll_widget_layout=self.verticalLayout,
                refresh_button=self.pushButton,
                exit_button=self.pushButton_2,
            )
            self.login_wechat_thread.finished_signal.connect(self.generate_chatroom)
            self.login_wechat_thread.finished_signal.connect(self.generate_friends)
            self.login_wechat_thread.finished_signal.connect(self.generate_mps)
            # self.login_wechat_thread.finished_signal.connect(self.generate_chatroom)
            self.login_wechat_thread.start()
        except Exception as e:
            print("执行登录线程出错：", e)
            self.outputWritten("执行登录线程出错：{}\n".format(e))

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        注销按钮
        """
        # 设置登录按钮为激活状态
        self.pushButton.setEnabled(True)
        # 在文本控制台中输入
        self.outputWritten("退出微信登录\n")
        # 注销微信登录
        itchat.logout()
        # 设置注销按钮为禁用状态
        self.pushButton_2.setEnabled(False)
        # 更改登陆按钮
        self.pushButton.setText("登录")