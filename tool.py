# -*- coding: utf-8 -*-

from tkinter import *
import os
import tkinter.messagebox as msgbox
import random

global entry_path       #目录输入框
global entry_numlen     #序号长度输入框
global entry_ftype      #后缀名输入框
global len_str          #序号长度
global type_str         #后缀名    

global current_path
current_path = os.getcwd()  #获取当前目录 

def msg_box(msg):
    msgbox.showinfo(title="成功", message=msg)

def err_box(msg):
    msgbox.showerror(title="失败", message=msg)

def warn_box(msg):
    msgbox.showwarning(title="提醒", message=msg)

#判断该文件是否为修改的后缀类型
def is_same_type(filename):
    type = entry_ftype.get()
    #截取文件名等长的后面几位
    file_type = filename[len(filename)-len(type):len(filename)]
    #print("file_type:" + file_type)
    if (file_type == type):
        return True
    return False

#判断字符串是否全为数字
def is_number(s):
    #if (False == s.isnumeric()):
    #    return False
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

#对某个文件按规则顺序命名
def rename(path, file, index):
    global type_str
    global len_str
    need_len = int(len_str)
    index_len = len(str(index))
    zero_pre = "-"
    for i in range(need_len - index_len):
        zero_pre = zero_pre + "0"
        
    old_name = path + "\\" + file
    new_name = path + "\\" + path.rsplit('\\', 1)[1] + zero_pre + str(index) + type_str
    print(str(index) + " old_name:" + old_name)
    print(str(index) + " new_name:" + new_name)
    os.rename(old_name, new_name)

#对某个文件随机重命名
def rename_rand(path, file):
    global type_str
    old_name = path + "\\" + file
    print("old_name:" + old_name)
    while(True):
        new_name = path + "\\" + path.rsplit('\\', 1)[1] + "-rand" + str(random.randint(500000, 10000000)) + type_str
        if (False == os.path.exists(new_name)):
            os.rename(old_name, new_name)
            print("rand_name:" + new_name)
            break

    
#重命名操作函数
def opr_file_name(file_dir, is_rand):
    global type_str
    for root, dirs, files in os.walk(file_dir):        
        index = 1
        for file in files:
            if (True == is_same_type(file)):
                #第一遍修改为随机名，确保第二次修改成功
                if (is_rand):
                    rename_rand(root, file)
                else:
                    rename(root, file, index)
                    index += 1

#点击确定后要执行的函数
def run():
    path = entry_path.get()
    global len_str
    global type_str
    len_str = entry_numlen.get()
    type_str = entry_ftype.get()
    #检测路径合法
    if (False == os.path.exists(path)):
        err_box("输入的路径有误！")
        return
    #检测长度合法
    if (False == is_number(len_str) or int(len_str) < 0 or int(len_str) > 10):
        err_box("输入的长度有误！")
        return
    #检测文件类型合法
    if (type_str[0] != '.' or type_str.count('.') > 1 or len(type_str) > 10):
        err_box("输入的后缀名有误！")
        return
    
    #先重命名第一遍，名字是随机名
    opr_file_name(path, True)
    print("--------------------------")
    #再重命名第二遍，根据指定规则
    opr_file_name(path, False)
    msg_box("操作成功！")


#创建主窗口
window = Tk()
window.title("批量文件重命名工具")         #标题设置
window.geometry('470x120')              #设置窗口大小为900x500 横纵尺寸
window.resizable(0, 0)                  #固定大小

#目录标签设置
label_path = Label(window, text="文件夹根目录(默认当前路径)：")
label_path.grid(row=1, column=0)
#创建输入框
entry_path = Entry(window, bg='azure', bd=3, width=40)
entry_path.insert(0, current_path)     #默认值为当前路径
entry_path.grid(row=1, column=1, stick=W)
#长度标签设置
label_numlen = Label(window, text="命名序号长度(如0001为4位)：")
label_numlen.grid(row=2, column=0)
#创建输入框
entry_numlen = Entry(window, bg='azure', bd=3, width=5)
entry_numlen.insert(0, "4")   #默认值
entry_numlen.grid(row=2, column=1, stick=W)
#后缀标签设置
label_ftype = Label(window, justify=LEFT, text="修改的文件类型(如.jpg)：")
label_ftype.grid(row=3, column=0)
#创建输入框
entry_ftype = Entry(window, bg='azure', bd=3, width=5)
entry_ftype.insert(0, ".jpg")   #默认值
entry_ftype.grid(row=3, column=1, stick=W)

#通过button直接创建一个按钮，宽度width为10，样式bd为1
b1 = Button(window, text="确定", width=10, height=1, anchor='center', compound='bottom', command=run)
b1.grid(row=5, column=0)

#通过button直接创建一个按钮，宽度width为10，样式bd为1
b2 = Button(window, text="退出", width=10, height=1, anchor='center', compound='bottom', command=window.quit)
b2.grid(row=5, column=1)


#调用主事件循环，让窗口程序保持运行
window.mainloop()
