import itchat,sys,time
class wx_login():

    def show_mobile_login(self):
        userInfo = itchat.web_init()

    def status(self,uuid):
        userInfo = itchat.web_init()
        itchat.show_mobile_login()
        itchat.get_friends(True)
        self.output_info('Login successfully as %s' % userInfo['NickName'])
        itchat.start_receiving()


    def output_info(self,msg):
        print('[INFO] %s' % msg)

    def get_uuid(self):
        self.output_info('Getting uuid')
        uuid = itchat.get_QRuuid()
        while uuid is None: uuid = itchat.get_QRuuid();time.sleep(1)
        with open('itchat.txt', 'w') as f:
            f.write(uuid)
        return uuid

    def open_QR(self,uuid):
        for get_count in range(10):
            self.output_info('Getting QR Code')
            if itchat.get_QR(uuid):
                break
            elif get_count >= 9:
                self.output_info('Failed to get QR Code, please restart the program')
                sys.exit()
        self.output_info('Please scan the QR Code')
        print()
        return 'ok'

    def login(self):
        with open('itchat.txt', 'r') as f:
            uuid = f.read()
        waitForConfirm = False
        while 1:
            status = itchat.check_login(uuid)
            if status == '200':
                userInfo = itchat.web_init()
                self.output_info('Login successfully as %s' % userInfo['User']['NickName'])
                break
            elif status == '201':
                if waitForConfirm:
                    self.output_info('Please press confirm')
                    waitForConfirm = True
            else:
                self.output_info('Reloading QR Code')
                uuid = self.get_uuid()
                QR = self.open_QR(uuid)
                waitForConfirm = False


if __name__ == '__main__':
    it=wx_login()
    it.get_uuid()