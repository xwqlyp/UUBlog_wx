#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Author: ####

from prettytable import PrettyTable
import time,datetime
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
color=Colored()
times= '当前时间:'+time.strftime('%Y.%m.%d',time.localtime(time.time()))
x = PrettyTable(["姓名", "性别", "年龄", "存款"])
x.align["姓名"] = "1" #以姓名字段左对齐
x.padding_width = 1  # 填充宽度
x.add_row([color.red("赵一"),"男", 20, 100000])
x.add_row(["钱二","男", 21, 500])
x.add_row(["孙三", "男", 22, 400.7])

with open('itchat.txt', 'w') as f:
    f.write('aa')
