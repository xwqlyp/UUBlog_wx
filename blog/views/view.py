from django.shortcuts import render,HttpResponse,redirect
from blog.models import IMG
import itchat,sys
from prettytable import PrettyTable
from PIL import Image,ImageDraw,ImageFont
import qrcode,os,requests
from PIL import Image
from pyzbar import pyzbar
import paramiko,multiprocessing,time,re
from multiprocessing import Manager
imgDIR= os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/static/images'
itchatDIR= os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/static/images'

def index(request):
    wx = login_itchat()
    if request.method=='POST':
        uuid=request.POST.get('uuid')
        print('uuid',uuid)
        statusInfo=wx.check_login(uuid)
        status=statusInfo['status']
        statusDES=statusInfo['statusDES']
        if  status=='200':
            info=wx.web_init()
            return render(request, 'index.html', locals())
        elif status=='201':
            img = "images/QR.png"
            return render(request, 'index.html', locals())
        else :
            img = "images/QR.png"
            return render(request, 'index.html', locals())
    else:
        loginInfo=wx.login()
        status=loginInfo['status']
        statusDES=loginInfo['statusDES']
        uuid=loginInfo['uuid']

        if  status=='200':
            info = wx.web_init()
            return render(request, 'index.html', locals())
        else :
            img = "images/QR.png"
            return render(request, 'index.html', locals())

def login(request):
    parms={
        'appkey':'BS-95b179678275462d85a7be0e25344f8a',
        'channel':'1234',
        'content':'你好',
    }
    url='http://goeasy.io/goeasy/publish'
    res=requests.post(url,parms)
    return render(request, 'login.html', locals())

def goEasy(channel,content):
    url='http://goeasy.io/goeasy/publish'
    parms={
            'appkey':'BC-2a4759e3e1d245d99ab0fb9316090594',
            'channel':channel,
            'content':content,
    }
    requests.post(url,parms)



class login_itchat():

    def output_info(self,msg):
        print('[INFO] %s' % msg)

    def open_QR(self):
        for get_count in range(10):
            self.output_info('Getting uuid')
            uuid = itchat.get_QRuuid()
            while uuid is None: uuid = itchat.get_QRuuid();time.sleep(1)
            self.output_info('Getting QR Code')
            http = "https://login.weixin.qq.com/l/" + uuid
            QR = imgDIR + '/QR.png'
            if make_qr_code(http, QR)=='ok':
                break
            elif get_count >= 9:
                self.output_info('Failed to get QR Code, please restart the program')
                sys.exit()
        with open('itchat.txt', 'w') as f:
            f.write(uuid)
        self.output_info('Please scan the QR Code')
        return uuid

    def web_init(self):
        itchat.show_mobile_login()
        userInfo = itchat.web_init()
        return userInfo

    def check_login(self,uuid):

        status=itchat.check_login(uuid)
        if status=='200':
            result = {'status': '200', 'statusDES': '登陆成功', 'uuid': uuid}
            return result
        elif status=='201':
            result = {'status': '201', 'statusDES': '已扫描二维码,手机上登录', 'uuid': uuid}
            return result
        else:
            result = {'status': '0', 'statusDES': '已生成二维码,请扫描登录', 'uuid': uuid}
            return result

    def login(self):
        with open('itchat.txt', 'r') as f:
            uuid=f.read()
        result=self.check_login(uuid)
        status=result['status']
        statusDES=result['statusDES']
        uuid=result['uuid']
        if status == '200' :
            self.web_init()
            result = {'status': status,'statusDES':statusDES, 'uuid': uuid}
            goEasy()
            itchat.run()
            return result
        elif status == '201':
            result = {'status': status, 'statusDES': statusDES, 'uuid': uuid}
            return result
        else:
            uuid = self.open_QR()
            result = {'status': status, 'statusDES': statusDES, 'uuid': uuid}
            return result

    def show(self):
        info=itchat.search_friends()
        return info

    def send(self):
        info=itchat.search_friends()
        return info

class Colored(object):
    # 显示格式: \033[显示方式;前景色;背景色m
    # 只写一个字段表示前景色,背景色默认
    RED = '\033[31m'  # 红色
    GREEN = '\033[32m'  # 绿色
    YELLOW = '\033[33m'  # 黄色
    BLUE = '\033[34m'  # 蓝色
    FUCHSIA = '\033[35m'  # 紫红色
    CYAN = '\033[36m'  # 青蓝色
    WHITE = '\033[37m'  # 白色

    #: no color
    RESET = '\033[0m'  # 终端默认颜色

    def color_str(self, color, s):
        return '{}{}{}'.format(
            getattr(self, color),
            s,
            self.RESET
        )

    def red(self, s):
        return self.color_str('RED', s)

    def green(self, s):
        return self.color_str('GREEN', s)

    def yellow(self, s):
        return self.color_str('YELLOW', s)

    def blue(self, s):
        return self.color_str('BLUE', s)

    def fuchsia(self, s):
        return self.color_str('FUCHSIA', s)

    def cyan(self, s):
        return self.color_str('CYAN', s)

    def white(self, s):
        return self.color_str('WHITE', s)

def get_data(ip, table,return_dict,index):
    host = Linux(ip, 'duyingshu', 'mLPsPUad9U7fMV#e')  # 传入Ip，用户名，密码
    host.connect()
    cdsql = host.send('ttisql smscc')  # 发送一个查看ip的命令
    selInfo = host.send('select count(0) from smscc.'+table+';')  # 发送一个查看ip的命令
    count = selInfo[selInfo.rfind("<") + 1:selInfo.find(" >")].strip()
    if count.isdigit():
        if table=='DELIVERSMINFO':
            jsonInfo={'ip':ip,'way':table+'__状态','count':count}
        elif table=='mtinfo':
            jsonInfo = {'ip': ip, 'way': table+'__通道', 'count': count}
        elif table=='smsmtinfo':
            jsonInfo = {'ip': ip, 'way': table+'__提交', 'count': count}
        elif table=='httpmtinfo':
            jsonInfo = {'ip': ip, 'way': table+'__接口', 'count': count}
        return_dict[index]=jsonInfo

def sava_treading(func):
    manager = Manager()
    return_dict = manager.dict()
    jobs = []
    # td_DELIVERSMINFO
    p1 = multiprocessing.Process(target=func, args=('121.41.105.235', 'DELIVERSMINFO',return_dict,'p1'))
    p2 = multiprocessing.Process(target=func, args=('121.40.185.29', 'DELIVERSMINFO',return_dict,'p2'))
    p3 = multiprocessing.Process(target=func, args=('121.43.159.17', 'DELIVERSMINFO',return_dict,'p3'))
    p4 = multiprocessing.Process(target=func, args=('121.40.176.39', 'DELIVERSMINFO',return_dict,'p4'))

    # td_mtinfo
    p5 = multiprocessing.Process(target=func, args=('121.41.105.235', 'mtinfo',return_dict,'p5'))
    p6 = multiprocessing.Process(target=func, args=('121.40.185.29', 'mtinfo',return_dict,'p6'))
    p7 = multiprocessing.Process(target=func, args=('121.43.159.17', 'mtinfo',return_dict,'p7'))
    p8 = multiprocessing.Process(target=func, args=('121.40.176.39', 'mtinfo',return_dict,'p8'))
    # 平台pt_smsmtinfo
    p9 = multiprocessing.Process(target=func, args=('120.55.192.229', 'smsmtinfo',return_dict,'p9'))
    p10 = multiprocessing.Process(target=func, args=('121.43.193.154', 'smsmtinfo',return_dict,'p10'))
    p11 = multiprocessing.Process(target=func, args=('120.55.116.3', 'smsmtinfo',return_dict,'p11'))
    p12 = multiprocessing.Process(target=func, args=('120.26.60.182', 'smsmtinfo',return_dict,'p12'))

    # td_DELIVERSMINFO
    p13 = multiprocessing.Process(target=func, args=('47.97.82.174', 'httpmtinfo',return_dict,'p13'))
    p14= multiprocessing.Process(target=func, args=('118.31.174.250', 'httpmtinfo',return_dict,'p14'))


    jobs.append(p1)
    jobs.append(p2)
    jobs.append(p3)
    jobs.append(p4)
    jobs.append(p5)
    jobs.append(p6)
    jobs.append(p7)
    jobs.append(p8)
    jobs.append(p9)
    jobs.append(p10)
    jobs.append(p11)
    jobs.append(p12)
    jobs.append(p13)
    jobs.append(p14)
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    p7.start()
    p8.start()
    p9.start()
    p10.start()
    p11.start()
    p12.start()
    p13.start()
    p14.start()
    for proc in jobs:
        proc.join()
    data=return_dict.values()
    print(data)
    return data

# 定义一个类，表示一台远端linux主机
class Linux(object):
    # 通过IP, 用户名，密码，超时时间初始化一个远程Linux主机
    def __init__(self, ip, username, password, timeout=30):
        self.ip = ip
        self.username = username
        self.password = password
        self.timeout = timeout
        # transport和chanel
        self.t = ''
        self.chan = ''
        # 链接失败的重试次数
        self.try_times = 3

    # 调用该方法连接远程主机
    def connect(self):
        while True:
            # 连接过程中可能会抛出异常，比如网络不通、链接超时
            try:
                self.t = paramiko.Transport(sock=(self.ip, 22))
                self.t.connect(username=self.username, password=self.password)
                self.chan = self.t.open_session()
                self.chan.settimeout(self.timeout)
                self.chan.get_pty()
                self.chan.invoke_shell()
                # 如果没有抛出异常说明连接成功，直接返回
                print(u'连接%s成功' % self.ip)
                # 接收到的网络数据解码为str
                print(self.chan.recv(65535).decode('utf-8'))
                return
            # 这里不对可能的异常如socket.error, socket.timeout细化，直接一网打尽
            except Exception as e1:
                if self.try_times != 0:
                    print(u'连接%s失败，进行重试' % self.ip)
                    self.try_times -= 1
                else:
                    print(u'重试5次失败，结束程序')
                    exit(1)

    # 断开连接
    def close(self):
        self.chan.close()
        self.t.close()

    # 发送要执行的命令
    def send(self, cmd):
        cmd += '\r'
        # 通过命令执行提示符来判断命令是否执行完成
        p = re.compile('root@scdel-02:.*?#')
        result = ''
        # 发送要执行的命令
        self.chan.send(cmd)
        # 回显很长的命令可能执行较久，通过循环分批次取回回显,执行成功返回true,失败返回false
        while True:
            time.sleep(0.5)
            ret = self.chan.recv(65535)
            ret = ret.decode('utf-8')
            result += ret
            return result

# 查询当时信息
def monitorNow():
    data=sava_treading(get_data)
    data.sort(key=lambda x: int(x['count']), reverse=True)

    tab = PrettyTable(["ip", "way", "count"])
    tab.valign['ip'] = 'c'
    tab.valign['way'] = 'c'
    tab.valign['count'] = 'c'
    tab.align['ip'] = 'l'
    tab.align['way'] = 'l'
    tab.align['count'] = 'l'
    tab.padding_width = 1

    # 表格内容插入
    for i in data:
        tab.add_row([i['ip'], i['way'], i['count']])
    times = '当前时间:' + time.strftime('%Y.%m.%d %X', time.localtime(time.time()))
    content=str(times+'\n'+str(tab))
    font = ImageFont.truetype('simsun.ttc', 16)
    im = Image.new('RGB', (400, 320), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    draw.text((0, 0), content, (0, 0, 0), font=font)
    # draw.text((0,60),unicode('你好','utf-8'),(0,0,0),font=font)
    im.save("img.jpg")
    return 'ok'

def send_wx(_info):
    itchat.auto_login(hotReload=True)
    if monitorNow()=='ok':
        img = "img.jpg"
        # 获得全部用户(可能是全部，打印出来太乱了没法看)
        # user = itchat.search_friends("wt")[0]["UserName"] #个人
        # myroom = itchat.search_chatrooms("info")[0]["UserName"]  # 群聊
        myroom1 = itchat.search_chatrooms("短信运维")[0]["UserName"] #群聊
        # itchat.send(contents,toUserName = myroom)
        # itchat.send_image(img,toUserName = user)
        itchat.send_image(img, toUserName=myroom1)
        # itchat.send_image(img,toUserName = myroom1)
        itchat.dump_login_status()

def make_qr_code_easy(content, save_path=None):
    """
    Generate QR Code by default
    :param content: The content encoded in QR Codeparams
    :param save_path: The path where the generated QR Code image will be saved in.
                      If the path is not given the image will be opened by default.
    """
    img = qrcode.make(data=content)
    if save_path:
        img.save(save_path)
    else:
        img.show()

def make_qr_code(content, save_path=None):
    """
    Generate QR Code by given params
    :param content: The content encoded in QR Code
    :param save_path: The path where the generated QR Code image will be saved in.
                      If the path is not given the image will be opened by default.
    """
    qr_code_maker = qrcode.QRCode(version=2,
                                  error_correction=qrcode.constants.ERROR_CORRECT_M,
                                  box_size=8,
                                  border=1,
                                  )
    qr_code_maker.add_data(data=content)
    qr_code_maker.make(fit=True)
    img = qr_code_maker.make_image(fill_color="black", back_color="white")
    if save_path:
        img.save(save_path)
        return 'ok'
    else:
        img.show()

def make_qr_code_with_icon(content, icon_path, save_path=None):
    """
    Generate QR Code with an icon in the center
    :param content: The content encoded in QR Code
    :param icon_path: The path of icon image
    :param save_path: The path where the generated QR Code image will be saved in.
                      If the path is not given the image will be opened by default.
    :exception FileExistsError: If the given icon_path is not exist.
                                This error will be raised.
    :return:
    """
    if not os.path.exists(icon_path):
        raise FileExistsError(icon_path)

    # First, generate an usual QR Code image
    qr_code_maker = qrcode.QRCode(version=4,
                                  error_correction=qrcode.constants.ERROR_CORRECT_H,
                                  box_size=8,
                                  border=1,
                                  )
    qr_code_maker.add_data(data=content)
    qr_code_maker.make(fit=True)
    qr_code_img = qr_code_maker.make_image(fill_color="black", back_color="white").convert('RGBA')

    # Second, load icon image and resize it
    icon_img = Image.open(icon_path)
    code_width, code_height = qr_code_img.size
    icon_img = icon_img.resize((code_width // 4, code_height // 4), Image.ANTIALIAS)

    # Last, add the icon to original QR Code
    qr_code_img.paste(icon_img, (code_width * 3 // 8, code_width * 3 // 8))

    if save_path:
        qr_code_img.save(save_path)
    else:
        qr_code_img.show()

def decode_qr_code(code_img_path):
    """
    Decode the given QR Code image, and return the content
    :param code_img_path: The path of QR Code image.
    :exception FileExistsError: If the given code_img_path is not exist.
                                This error will be raised.
    :return: The list of decoded objects
    """
    if not os.path.exists(code_img_path):
        raise FileExistsError(code_img_path)

    # Here, set only recognize QR Code and ignore other type of code
    return pyzbar.decode(Image.open(code_img_path), symbols=[pyzbar.ZBarSymbol.QRCODE])

def uploadImg(request):
    """
    图片上传
    :param request:
    :return:
    """
    if request.method == 'POST':
        new_img = IMG(
            img=request.FILES.get('img'),
            name=request.FILES.get('img').name
        )
        new_img.save()
    return render(request,'app/uploading.html')

def showImg(request):
    """
    图片显示
    :param request:
    :return:
    """
    imgs = IMG.objects.all()
    content = {
        'imgs': imgs,
    }
    for i in imgs:
        print(i.img.url)
    return render(request, 'app/showing.html', content)



