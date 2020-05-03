# -*- coding: utf-8 -*-

import itchat
import schedule
import time
import datetime
import os
os.system('mode con cols=120 lines=60')

print('\033[1;32m **************************************  \033[0m')
print("\033[1;32m ***                                *** \033[0m")
print("\033[1;32m *** \033[0m \033[1;34m 分中心微信自动健康报告工具 \033[0m \033[1;32m *** \033[0m")
print("\033[1;32m ***                                *** \033[0m")
print("\033[1;32m ************************************** \033[0m")

print("\r\n\033[1;41m使用须知：本程序完全基于网页版微信协议在您的本机实现，不涉及任何用户隐私和安全问题！\r\n源代码已公开在 https://github.com/mayaxcn/FZX-AutoCheckin 上接受交流和审查 \033[0m\r\n")
print("## 根据提示设置需报告时间、报告群名称和报告内容即可 ##\r\n")

def verify_date_str_lawyer(datetime_str):
    try:
    	datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')        
    	return True
    except ValueError:        
    	return False

while True:
    repeatTime = input("1. 请设置24小时制的回复时间（如填入 04:30 则表示为每日凌晨4点30分）：")
    repeatTime = repeatTime.replace('：',':')
    if len(repeatTime)==5 and verify_date_str_lawyer("2020-05-01 "+repeatTime.split(':')[0]+":"+repeatTime.split(':')[1]+":00"):
        break
    else:
        print("\033[1;33m --> 时间格式输入有误！\r\n\033[0m")

repeatH = repeatTime.split(':')[0]
repeatM = repeatTime.split(':')[1]

while True:
    replyGroupname = input("2. 需回复的群完整昵称：")
    if replyGroupname.strip()!="":
        replyGroupname=replyGroupname.strip()
        break
    else:
        print("\033[1;33m --> 群昵称不能为空！\r\n\033[0m")


while True:
    replyContent = input("3. 回复内容：")
    if replyContent.strip()!="":
        replyContent=replyContent.strip()
        break
    else:
        print("\033[1;33m --> 回复内容不能为空！\r\n\033[0m")

print("\r\n\033[1;33m设置完成，将于每日"+repeatH+"时"+repeatM+"分在“"+replyGroupname+"”群自动回复“"+replyContent+"”内容，读取微信网页版登录二维码中...\033[0m\r\n")

itchat.auto_login(enableCmdQR=True)
itchat.send("分中心健康报告微信自动签报设置成功，工具将于每日"+repeatH+"时"+repeatM+"分在“"+replyGroupname+"”群自动回复“"+replyContent+"”内容，退出网页版微信即可停止本功能。", toUserName="filehelper")

print("I'm working now !!")

def SentChatRoomsMsg(name, context):
    itchat.get_chatrooms(update=True)
    iRoom = itchat.search_chatrooms(name)
    for room in iRoom:
        if name in room['NickName']:
            userName = room['UserName']
            break
    itchat.send_msg(str(context), userName)
    print("发送时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
        "发送到：" + name + "\n"
        "发送内容：" + context + "\n")

def autoCheckin():
    SentChatRoomsMsg(replyGroupname,replyContent)

schedule.every().day.at(repeatTime).do(autoCheckin)

while True:
    schedule.run_pending()
    time.sleep(1)
