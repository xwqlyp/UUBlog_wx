import itchat, time, sys

def output_info(msg):
    print('[INFO] %s' % msg)

def open_QR():
    print('aaa')
    for get_count in range(10):
        output_info('Getting uuid')
        uuid = itchat.get_QRuuid()
        while uuid is None: uuid = itchat.get_QRuuid();time.sleep(1)
        output_info('Getting QR Code')
        if itchat.get_QR(uuid):
            break
        elif get_count >= 9:
            output_info('Failed to get QR Code, please restart the program')
            sys.exit()
    with open('itchat.txt', 'w') as f:
        f.write(uuid)
    output_info('Please scan the QR Code')

    return uuid

def login(uuid):

    # uuid = open_QR()
    waitForConfirm = False
    while 1:
        status = itchat.check_login(uuid)
        if status == '200':
            break
        elif status == '201':
            if waitForConfirm:
                output_info('Please press confirm')
                waitForConfirm = True
        elif status == '408':
            output_info('Reloading QR Code')
            uuid = open_QR()
            waitForConfirm = False
    userInfo = itchat.web_init()
    print(userInfo)
    print(itchat.show_mobile_login())
    return itchat

    # output_info('Login successfully as %s' % userInfo[0]['NickName'])

def send_wx():
    with open('itchat.txt', 'r') as f:
        print('qqqqqqqqq')
        uuid = f.read()
    itchat=login(uuid)
    print('qqsas')
    itchat.show_mobile_login()
    itchat.get_friends(True)
    print(itchat.search_friends('wt'))
    print(itchat.get_friends(True))


if __name__ == '__main__':

    send_wx()

