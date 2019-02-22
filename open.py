# -*-coding: utf-8 -*-
from linepy import *
#from numba import jit
from datetime import datetime
from time import sleep
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, timeit, _thread
#==============================================================================#
cl = LINE("")
print("Auth Token : " + str(cl.authToken))
clMID = cl.profile.mid
botStart = time.time()
oepoll = OEPoll(cl)
ban = json.load(codecs.open("ban.json","r","utf-8"))
pic = json.load(codecs.open("picture.json","r","utf-8"))
settings = json.load(codecs.open("temp.json","r","utf-8"))
msg_dict = {}
def restartBot():
    print ("[ INFO ] BOT RESETTED")
    backupData()
    python = sys.executable
    os.execl(python, python, *sys.argv)
def backupData():
    try:
        json.dump(settings,codecs.open('temp.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
        json.dump(pic,codecs.open('picture.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
        json.dump(ban, codecs.open('ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False
def logError(text):
    cl.log("[ ERROR ] " + str(text))
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
def sendMessageWithMention(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@x '
        cl.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        logError(error)
def sendMention(to, text="", mids=[]):
    arrData = ""
    arr = []
    mention = "@zeroxyuuki "
    if mids == []:
        raise Exception("Invaliod mids")
    if "@!" in text:
        if text.count("@!") != len(mids):
            raise Exception("Invalid mids")
        texts = text.split("@!")
        textx = ""
        for mid in mids:
            textx += str(texts[mids.index(mid)])
            slen = len(textx)
            elen = len(textx) + 15
            arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
            arr.append(arrData)
            textx += mention
            textx += str(texts[len(mids)])
    else:
        textx = ""
        slen = len(textx)
        elen = len(textx) + 15
        arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mids[0]}
        arr.append(arrData)
        textx += mention + str(text)
    cl.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
def helpmessage():
    helpMessage = """╔═══════════
╠♥ ✿✿✿ 喵の單體半垢 ✿✿✿ ♥
╠═✪〘 owners專用 〙✪═
╠✪〘 Help 〙✪═════
╠➥ Help 查看指令
╠✪〘 Status 〙✪════
╠➥ Restart 重新啟動
╠➥ Save 儲存設定
╠➥ Runtime 運作時間
╠➥ Speed 速度
╠➥ Set 設定
╠➥ About 關於發送者
╠➥ About Bot 關於機器
╠✪〘 Settings 〙✪═══
╠➥ AutoAdd On/Off 自動加入
╠➥ AutoJoin On/Off 網址進群
╠➥ AutoLeave On/Off 離開副本
╠➥ AutoRead On/Off 自動已讀
╠➥ Prompt On/Off 群組狀況提示
╠➥ ReRead On/Off 查詢收回
╠➥ Pro On/Off 所有保護
╠➥ Protect On/Off 踢人保護
╠➥ QrProtect On/Off 網址保護
╠➥ Invprotect On/Off 邀請保護
╠➥ Getinfo On/Off 取得友資詳情
╠➥ Detect On/Off 標註偵測
╠➥ Timeline On/Off 文章預覽
╠✪〘 Self 〙✪═════
╠➥ Me 我的連結
╠➥ Mymid 我的mid
╠➥ Mid @ 查mid[友資/Tag]
╠➥ Contact: 以mid查友資
╠➥ Info @ 查看資料
╠✪〘 Blacklist 〙✪═══
╠➥ Ban [@/:] 加入黑單[友資/Tag/MID]
╠➥ Unban [@/:] 取消黑單[友資/Tag/MID]
╠➥ Banlist 查看黑單
╠➥ CleanBan 清空黑單
╠➥ Kickban 踢除黑單
╠✪〘 Group 〙✪════
╠➥ Link On/Off 網址開啟/關閉
╠➥ Link 查看群組網址
╠➥ GroupList 所有群組列表
╠➥ GroupMemberList 成員名單
╠➥ GroupInfo 群組資料
╠➥ Gn [text] 更改群名
╠➥ Tk @ 標註踢人
╠➥ Nk 以名字踢人
╠➥ Nt 以名字標注
╠➥ Cancel 取消所有邀請
╠➥ Tagall 標註全體
╠➥ Setread 已讀點設置
╠➥ Cancelread 取消偵測
╠➥ Checkread 已讀偵測
╠➥ Gbc: 群組廣播(可限制人數)
╠➥ Fbc: 好友廣播
╠➥ Bye 機器退群(確認請打Y)
╠✪〘 Admin 〙✪════
╠➥ Adminadd @ 新增權限
╠➥ Admindel @ 刪除權限
╠➥ Adminlist 查看權限表
╠✪〘 Other 〙✪════
╠➥ Say [text times] 重複講話
╠➥ Timenow 現在時刻
╠➥ Tag @ [times] 重複標人
╠➥ Reply_text_reply 關鍵字回覆
╚═〘 Created By: 蘿莉喵™ 〙"""
    return helpMessage
wait = {
    "ban":False,
    "unban":False,
    "getmid":False,
    'bye':{},
    'reply':{}
}
wait2 = {
    'readPoint':{},
    'readMember':{},
    'setTime':{},
    'ROM':{}
}
setTime = {}
setTime = wait2['setTime']
owners=["ua10c2ad470b4b6e972954e1140ad1891","u0505fe1fb484fc1537d12ad53a5a4ea2","uc338f8ef91292e65aea28feb5002d0f3","u992a6e77041a772b8abd613ea64d4623",clMID]

#==============================================================================#
def lineBot(op):
    try:
        if op.type == 0:
            return
        if op.type == 5:
            if settings["autoAdd"] == True:
                cl.findAndAddContactsByMid(op.param1)
                sendMention(op.param1, " @! 感謝您加我為好友",[op.param1])
        if op.type == 11:
            G = cl.getGroup(op.param1)
            if op.param1 in settings["mention"]:
                sendMention(op.param1, " @! 更改群組設定",[op.param2])
            if op.param1 in settings["qrprotect"] and op.param3 == '4':
                if op.param2 in ban["admin"] or op.param2 in owners:
                    pass
                else:
                    gs = cl.getGroup(op.param1)
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    ban["blacklist"][op.param2] = True
                    gs.preventJoinByTicket = True
                    cl.updateGroup(gs)
        if op.type == 13:
            if clMID in op.param3:
                group = cl.getGroup(op.param1)
                if op.param2 in ban["admin"] or op.param2 in owners:
                    cl.acceptGroupInvitation(op.param1)
                    sendMention(op.param1, "權限者 @! 邀請入群",[op.param2])
                else:
                    sendMention(op.param2, "@! 你不是權限者",[op.param2])
            elif op.param1 in settings["invprotect"]:
                if op.param2 in ban["admin"] or op.param2 in ban["bots"] or op.param2 in owners:
                    pass
                else:
                    ban["blacklist"][op.param2] = True
                    cl.cancelGroupInvitation(op.param1,[op.param3])
                    cl.kickoutFromGroup(op.param1,[op.param2])
            else:
                gInviMids = []
                for z in op.param3:
                    if z in ban["blacklist"]:
                        gInviMids.append(z.mid)
                if gInviMids == []:
                    pass
                else:
                    for mid in gInviMids:
                        cl.cancelGroupInvitation(op.param1, [mid])
                    cl.sendMessage(op.param1,"Do not invite blacklist user...")
        if op.type == 17:
            if op.param1 in ban["blacklist"]:
                cl.kickoutFromGroup(op.param1,[op.param2])
                cl.sendMessage(op.param1,"Blacklist user joined...")
            if op.param1 in settings["mention"]:
                name = str(cl.getGroup(op.param1).name)
                sendMention(op.param1, "你好 @! 歡迎加入"+name,[op.param2])
        if op.type == 19:
            if op.param1 in settings["mention"]:
                chiya=[op.param2]
                chiya.append(op.param3)
                sendMention(op.param1,"警告!! @! 踢了 @! ", chiya)
            if op.param2 in ban["admin"] or op.param2 in ban["bots"] or op.param2 in owners:
                pass
            elif op.param3 in owners:
                ban["blacklist"][op.param2] = True
                json.dump(ban, codecs.open('ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                cl.kickoutFromGroup(op.param1,[op.param2])
                cl.inviteIntoGroup(op.param1,[op.param3])
            elif op.param1 in settings["protect"]:
                ban["blacklist"][op.param2] = True
                cl.kickoutFromGroup(op.param1,[op.param2])
                json.dump(ban, codecs.open('ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
        if op.type == 24 or op.type == 21 or op.type ==22:
            if settings["autoLeave"] == True:
                cl.leaveRoom(op.param1)
        if (op.type == 25 or op.type == 26) and op.message.contentType == 0:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            elif msg.toType == 2:
                to = receiver
            if text is None:
                return
            if sender in ban["blacklist"]:
                return
            if sender not in ban["blacklist"]:
                if text.lower() == 'about':
                    ret_ = "╔══[ 關於使用者 ]"
                    ret_ += "\n╠ 使用者名稱 : {}".format(cl.getContact(sender).displayName)
                    if sender in cl.getAllContactIds():ret_ += "\n╠ 與本帳關係 : 好友"
                    elif sender in cl.getBlockedContactIds():ret_ += "\n╠ 與本帳關係 : phon swo"
                    else:ret_ += "\n╠ 與本帳關係 : 普通"
                    if sender in owners:ret_ += "\n╠ 使用者權限 : 最高(擁有者)"
                    elif sender in ban["admin"]:ret_ += "\n╠ 使用者權限 : 部分(權限者)"
                    elif sender in ban["blacklist"]:ret_ += "\n╠ 使用者權限 : 無(黑單者)"
                    else:ret_ += "\n╠ 使用者權限 : 基本(抽圖片)"
                    ret_ += "\n╠ 詳細功能請打help"
                    ret_ += "\n╠ 製作者 : 天下第一喵"
                    ret_ += "\n╚══[ 感謝您的使用 ]"
                    cl.sendMessage(to, str(ret_))
                elif text.lower() in settings['mute']:
                    cl.sendMessage(to,settings['mute'][text.lower()])
                elif text.lower() in settings['changeGroupPicture']:
                    cl.sendImage(to, settings['changeGroupPicture'][text.lower()])
            if sender in ban["admin"] or sender in owners:
                if text.lower() == 'help':
                    helpMessage = helpmessage()
                    cl.sendMessage(to, str(helpMessage))
                elif text.lower() in ['speed','sp']:
                    cl.sendMessage(to,"小喵極緩慢的測速中...\n結果約為"+str(timeit.timeit('"-".join(str(n) for n in range(100))',number=1000)) + "秒")
                elif text.lower() == 'save':
                    backupData()
                    cl.sendMessage(to,"儲存設定成功!")
                elif text.lower() == 'runtime':
                    cl.sendMessage(to, "系統已運作 {}".format(str(format_timespan(time.time() - botStart))))
                elif text.lower() in ['bot','about bot']:
                    ret_ = "╔══[ 關於本機器 ]"
                    ret_ += "\n╠ 機器名稱 : {}".format(cl.getContact(clMID).displayName)
                    ret_ += "\n╠ 群組數 : {}".format(str(len(cl.getGroupIdsJoined())))
                    ret_ += "\n╠ 好友數 : {}".format(str(len(cl.getAllContactIds())))
                    ret_ += "\n╠ 已封鎖 : {}".format(str(len(cl.getBlockedContactIds())))
                    ret_ += "\n╠ 版本 : self bot"
                    ret_ += "\n╠ 製作者 : 天下第一喵"
                    ret_ += "\n╚══[ 感謝您的使用 ]"
                    cl.sendMessage(to, str(ret_))
                    cl.sendContact(to,"ua10c2ad470b4b6e972954e1140ad1891")
                elif text.lower() == 'set':
                    try:
                        ret_ = "╔══[ 本機設定 ]"
                        if settings["autoAdd"] == True: ret_ += "\n╠ 自動加入好友 ✅"
                        else: ret_ += "\n╠ 自動加入好友 ❌"
                        if settings["autoJoinTicket"] == True: ret_ += "\n╠ 自動進入網址 ✅"
                        else: ret_ += "\n╠ 自動進入網址 ❌"
                        if settings["autoLeave"] == True: ret_ += "\n╠ 自動退出副本 ✅"
                        else: ret_ += "\n╠ 自動退出副本 ❌"
                        if settings["autoRead"] == True: ret_ += "\n╠ 自動已讀 ✅"
                        else: ret_ += "\n╠ 自動已讀 ❌"
                        if settings["getmid"] == True: ret_ += "\n╠ 獲取友資詳情 ✅"
                        else: ret_ += "\n╠ 獲取友資詳情 ❌"
                        if settings["timeline"] == True: ret_ += "\n╠ 文章預覽 ✅"
                        else: ret_ += "\n╠ 文章預覽 ❌"
                        if settings["detectMention"] ==True: ret_+="\n╠ 標註偵測 ✅"
                        else: ret_ += "\n╠ 標註偵測 ❌"
                        if msg.toType==2:
                            ret_ += "\n╠══[ 單群設定 ]"
                            G = cl.getGroup(msg.to)
                            ret_ += "\n╠ 群組名稱 : {}".format(str(G.name))
                            if G.id in settings["protect"] : ret_+="\n╠ 踢人保護 ✅"
                            else: ret_ += "\n╠ 踢人保護 ❌"
                            if G.id in settings["qrprotect"] : ret_+="\n╠ 網址保護 ✅"
                            else: ret_ += "\n╠ 網址保護 ❌"
                            if G.id in settings["invprotect"] : ret_+="\n╠ 邀請保護 ✅"
                            else: ret_ += "\n╠ 邀請保護 ❌"
                            if G.id in settings["mention"] : ret_ += "\n╠ 群組狀況提示 ✅"
                            else: ret_ += "\n╠ 群組狀況提示 ❌"
                            if G.id in settings["reread"]: ret_+="\n╠ 復讀 ✅"
                            else: ret_ += "\n╠ 復讀 ❌"
                        ret_ += "\n╚[ 你以為還有嗎 ]"
                        cl.sendMessage(to, str(ret_))
                    except Exception as e:
                        cl.sendMessage(msg.to, str(e))
                elif text.lower().startswith("reply_"):
                    x = text.split('_')
                    settings['mute'][x[1].lower()] = x[2]
                    cl.sendMessage(to,'ok')
                elif text.lower().startswith("imagereply_"):
                    x = text[11:]
                    wait['reply'][sender]=x.lower()
                    cl.sendMessage(to,'please send a picture')
                elif text.lower() in ['adminlist','admin']:
                    if ban["admin"] == []:
                        cl.sendMessage(to,"無擁有權限者!")
                    else:
                        mc = "╔══[ 權限者 ]"
                        for mi_d in ban["admin"]:
                            try:
                                mc += "\n╠ "+cl.getContact(mi_d).displayName
                            except:
                                ban["admin"].remove(mi_d)
                                pass
                        cl.sendMessage(to,mc + "\n╚[ 想要權限請私作者 ]")
                elif text.lower().startswith("say "):
                    x = text.split(' ')
                    if len(x) == 2:
                        cl.sendMessage(to,x[1])
                    elif len(x) == 3:
                        try:
                            c = int(x[2])
                            for c in range(c):
                                cl.sendMessage(to,x[1])
                        except:
                            cl.sendMessage(to,"無法正確執行此指令")
                elif msg.text.lower().startswith("tag "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    x = text.split(' ')
                    if len(x) == 2:
                        sendMessageWithMention(to, inkey)
                    elif len(x) == 3:
                        c = int(x[2])
                        for c in range(c):
                            sendMessageWithMention(to, inkey)
#==============================================================================#
                elif text.lower() == 'me':
                    if msg.toType == 0:
                        cl.sendContact(to, sender)
                    else:
                        sendMessageWithMention(to, sender)
                        cl.sendContact(to,sender)
                elif text.lower() == 'mymid':
                    cl.sendMessage(msg.to,"[MID]\n" +  sender)
                elif msg.text.lower().startswith("contact:"):
                    y = text[8:].split(' ')
                    for mid in y:
                        cl.sendContact(msg.to,mid)
                elif msg.text.lower().startswith("mid "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        ret_ = "[ Mid User ]"
                        for ls in lists:
                            ret_ += "\n" + ls
                        cl.sendMessage(msg.to, str(ret_))
                elif text.lower() == 'mid':
                    wait["getmid"]=True
                    cl.sendMessage(to,"please send a contact")
                elif msg.text.lower().startswith("info "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = cl.getContact(ls)
                            cl.sendMessage(msg.to, "[ 名字 ]\n" + contact.displayName +"\n[ 個簽 ]\n" + contact.statusMessage +"\n[ MID ]\n" + contact.mid)
                            cl.sendImageWithURL(msg.to, str("http://dl.profile.line-cdn.net/" + cl.getContact(ls).pictureStatus)) 
                            cl.sendImageWithURL(msg.to, str(cl.getProfileCoverURL(ls)))
#==============================================================================#
                elif text.lower() in ['link on',"招待URL許可"]:
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            cl.sendMessage(to, "既に許可されていますよ。")
                        else:
                            if group.id in settings["qrprotect"]:
                                cl.sendMessage(to,"招待URLの設定変更が禁止されているので作成できませんね。\n保護 URL オフを実行してください。")
                            else:
                                group.preventedJoinByTicket = False
                                cl.updateGroup(group)
                                cl.sendMessage(to, "URL招待を許可しましたよ。")
                elif text.lower() in ["招待URL拒否",'link off']:
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        if group.preventedJoinByTicket == True:
                            cl.sendMessage(to, "既に拒否されていますよ。")
                        else:
                            group.preventedJoinByTicket = True
                            cl.updateGroup(group)
                            cl.sendMessage(to,  "URL招待を拒否しましたよ。")
                elif text.lower() in ['now','timenow',"魔刻結晶"]:
                    cl.sendMessage(to, "現在時刻は" + datetime.strftime(datetime.now(),'%Y年%m月%d日 %H:%M:%S') + "です。")
                elif text.lower() in ['gurl_get','gurl','link','grouplink',"招待URL生成"]:
                    if msg.toType==2:
                        group=cl.getGroup(to)
                        if group.id in wait["qrprotect"]:
                            cl.sendMessage(to, "招待URLの設定変更が禁止されているので作成できませんね。")
                        else:
                            cl.sendMessage(to,"https://line.me/R/ti/g/{}".format(str(cl.reissueGroupTicket(group.id))))
                elif text.lower() in ['groupinfo','ginfo']:
                    group = cl.getGroup(to)
                    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "不明"
                    if group.invitee is None:
                        gPending = "0"
                    else:
                        gPending = str(len(group.invitee))
                    if group.preventedJoinByTicket == True:
                        gQr = "關閉"
                        gTicket = "無"
                    else:
                        gQr = "開啟"
                        gTicket = "https://line.me/R/ti/g/{}".format(str(cl.reissueGroupTicket(group.id)))
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    ret_ = "╔══[ 群組資料 ]"
                    ret_ += "\n╠ 群組名稱 : {}".format(str(group.name))
                    ret_ += "\n╠ 群組 Id : {}".format(group.id)
                    ret_ += "\n╠ 創建者 : {}".format(str(gCreator))
                    ret_ += "\n╠ 群組人數 : {}".format(str(len(group.members)))
                    ret_ += "\n╠ 邀請中 : {}".format(gPending)
                    ret_ += "\n╠ 網址狀態 : {}".format(gQr)
                    ret_ += "\n╠ 群組網址 : {}".format(gTicket)
                    ret_ += "\n╚══[ 完 ]"
                    cl.sendMessage(to, str(ret_))
                    cl.sendImageWithURL(to, path)
                elif text.lower() in ['groupmemberlist','gmember','member']:
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        ret_ = "╔══[ 成員名單 ]"
                        no = 1
                        for mem in group.members:
                            ret_ += "\n╠ {}. {}".format(str(no), str(mem.displayName))
                            no += 1
                        ret_ += "\n╚══[ 全部成員共 {} 人]".format(str(no-1))
                        cl.sendMessage(to, str(ret_))
                elif text.lower() in ['grouplist','glist','lg']:
                    groups = cl.groups
                    ret_ = "╔══[ 群組一覽 ]"
                    no = 1
                    for gid in groups:
                        group = cl.getGroup(gid)
                        ret_ += "\n╠ {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                        no += 1
                    ret_ += "\n╚══[ 共 {} 群 ]".format(str(no))
                    cl.sendMessage(to, str(ret_))
#==============================================================================#
                elif text.lower() == 'tagall':
                    group = cl.getGroup(msg.to)
                    nama = [contact.mid for contact in group.members]
                    k = len(nama)//20
                    for a in range(k+1):
                        txt = u''
                        s=0
                        b=[]
                        for i in group.members[a*20 : (a+1)*20]:
                            b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
                            s += 7
                            txt += u'@Alin \n'
                        cl.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
                    cl.sendMessage(to, "總共 {} 人".format(str(len(nama))))
                elif text.lower().startswith("gn "):
                    if msg.toType == 2:
                        X = cl.getGroup(msg.to)
                        X.name = msg.text.replace("Gn ","")
                        cl.updateGroup(X)
                    else:
                        cl.sendMessage(msg.to,"It can't be used besides the group.")
                elif text.lower() in ['setread','sr','既読ポイント設定']:
                    cl.sendMessage(msg.to, "既読ポイントを設定しました。\n確認したい場合は「既読確認」と送信してください。")
                    try:
                        del wait2['readPoint'][msg.to]
                        del wait2['readMember'][msg.to]
                    except:
                        pass
                    now2 = datetime.now()
                    wait2['readPoint'][msg.to] = msg.id
                    wait2['readMember'][msg.to] = ""
                    wait2['setTime'][msg.to] = datetime.strftime(now2,"%H:%M")
                    wait2['ROM'][msg.to] = {}
                elif text.lower() in ['cancelread','cr']:
                    cl.sendMessage(to, "已讀點已刪除")
                    try:
                        del wait2['readPoint'][msg.to]
                        del wait2['readMember'][msg.to]
                        del wait2['setTime'][msg.to]
                    except:
                        pass
                elif text.lower() in ['checkread','lookread','lr','既読確認','sn']:
                    if msg.to in wait2['readPoint']:
                        if wait2["ROM"][msg.to].items() == []:
                            chiya = ""
                        else:
                            chiya = ""
                            for rom in wait2["ROM"][msg.to].items():
                                chiya += rom[1] + "\n"
                        cl.sendMessage(msg.to, "[已讀的人]:\n%s\n查詢時間:[%s]" % (chiya,setTime[msg.to]))
                    else:
                        cl.sendMessage(msg.to, "尚未開啟偵測")
                elif text.lower() == 'banlist':
                    if ban["blacklist"] == {}:
                        cl.sendMessage(msg.to,"無黑單成員!")
                    else:
                        mc = "╔══[ 黑單成員 ]"
                        for mi_d in ban["blacklist"]:
                            try:
                                mc += "\n╠ "+cl.getContact(mi_d).displayName
                            except:
                                pass
                        cl.sendMessage(msg.to,mc + "\n╚══[ 完 ]")
                elif text.lower().startswith("nt "):
                    if msg.toType == 2:
                        _name = msg.text.replace("Nt ","")
                        gs = cl.getGroup(msg.to)
                        targets = []
                        for g in gs.members:
                            if _name in g.displayName:
                                targets.append(g.mid)
                        if targets == []:
                            cl.sendMessage(msg.to,"Not Found")
                        else:
                            for target in targets:
                                try:
                                    sendMessageWithMention(to, target)
                                except:
                                    pass
                elif text.lower() in ["さようなら",'bye']:
                    cl.sendMessage(msg.to, "考え直して頂けませんか...?\n(y/n)")
                    wait['bye'][msg.to] = sender
                elif text.lower() in ["Y","y","おk","N","n","だめ"]:
                    if msg._from== wait['bye'][msg.to]:
                        if text.lower() in ["いいよ",'y']:
                            cl.sendMessage(msg.to, "分かりました...")
                            cl.leaveGroup(msg.to)
                            del wait['bye'][msg.to]
                        elif text.lower() in ['n',"だめ"]:
                            cl.sendMessage(msg.to, "考え直して頂けたようですね。ありがとうございます。")
                            del wait['bye'][msg.to]
                    else:
                        pass
#==============================================================================#
                elif text.lower() == 'restart':
                    cl.sendMessage(to, "重啟成功，請重新登入")
                    restartBot()
                elif text.lower() == 'autoadd on':
                    settings["autoAdd"] = True
                    cl.sendMessage(to, "自動加入好友開啟")
                elif text.lower() == 'autoadd off':
                    settings["autoAdd"] = False
                    cl.sendMessage(to, "自動加入好友關閉")
                elif text.lower() == 'autojoin on':
                    settings["autoJoinTicket"] = True
                    cl.sendMessage(to, "自動網址進群開啟")
                elif text.lower() == 'autojoin off':
                    settings["autoJoinTicket"] = False
                    cl.sendMessage(to, "自動網址進群關閉")
                elif text.lower() == 'autoleave on':
                    settings["autoLeave"] = True
                    cl.sendMessage(to, "自動離開副本開啟")
                elif text.lower() == 'autoleave off':
                    settings["autoLeave"] = False
                    cl.sendMessage(to, "自動離開副本關閉")
                elif text.lower() == 'autoread on':
                    settings["autoRead"] = True
                    cl.sendMessage(to, "自動已讀開啟")
                elif text.lower() == 'autoread off':
                    settings["autoRead"] = False
                    cl.sendMessage(to, "自動已讀關閉")
                elif text.lower() == 'prompt on':
                    if msg.toType ==2:
                        settings["mention"][to] = True
                        cl.sendMessage(to, "群組狀況提示開啟")
                elif text.lower() == 'prompt off':
                    if msg.toType ==2 :
                        try:
                            del settings["mention"][to]
                            cl.sendMessage(to, "群組狀況提示關閉")
                        except:
                            cl.sendMessage(to, "沒開你是要關洨==")
                elif text.lower() == 'reread on':
                    if msg.toType ==2 :
                        settings["reread"][to] = True
                        cl.sendMessage(to,"復讀開啟")
                elif text.lower() == 'reread off':
                    if msg.toType ==2 :
                        try:
                            del settings["reread"][to]
                            cl.sendMessage(to,"復讀關閉")
                        except:
                            pass
                elif text.lower() == 'protect on':
                    if msg.toType ==2:
                        settings["protect"][to] = True
                        cl.sendMessage(to, "踢人保護開啟")
                elif text.lower() == 'protect off':
                    if msg.toType ==2 :
                        try:
                            del settings["protect"][to]
                            cl.sendMessage(to, "踢人保護關閉")
                        except:
                            cl.sendMessage(to, "沒開你是要關洨==")
                elif text.lower() == 'detect on':
                    settings["detectMention"] = True
                    cl.sendMessage(to, "已開啟標註偵測")
                elif text.lower() == 'detect off':
                    settings["detectMention"] = False
                    cl.sendMessage(to, "已關閉標註偵測")
                elif text.lower() == 'ban':
                    wait["ban"]=True
                    cl.sendMessage(to,"please send a contact")
                elif text.lower() == 'unban':
                    wait["unban"]=True
                    cl.sendMessage(to,"please send a contact")
                elif text.lower() == 'qrprotect on':
                    if msg.toType ==2:
                        settings["qrprotect"][to] = True
                        cl.sendMessage(to, "網址保護開啟")
                elif text.lower() == 'qrprotect off':
                    if msg.toType ==2 :
                        try:
                            del settings["qrprotect"][to]
                            cl.sendMessage(to, "網址保護關閉")
                        except:
                            cl.sendMessage(to, "沒開你是要關洨==")
                elif text.lower() == 'invprotect on':
                    if msg.toType ==2:
                        settings["invprotect"][to] = True
                        cl.sendMessage(to, "邀請保護開啟")
                elif text.lower() == 'invprotect off':
                    if msg.toType ==2 :
                        try:
                            del settings["invprotect"][to]
                            cl.sendMessage(to, "邀請保護關閉")
                        except:
                            cl.sendMessage(to, "沒開你是要關洨==")
                elif text.lower() == 'getinfo on':
                    settings["getmid"] = True
                    cl.sendMessage(to, "友資詳情獲取開啟")
                elif text.lower() == 'getinfo off':
                    settings["getmid"] = False
                    cl.sendMessage(to, "友資詳情獲取關閉")
                elif text.lower() == 'timeline on':
                    settings["timeline"] = True
                    cl.sendMessage(to, "文章預覽開啟")
                elif text.lower() == 'timeline off':
                    settings["timeline"] = False
                    cl.sendMessage(to, "文章預覽關閉")
                elif text.lower() == 'savelolipic on':
                    wait["pic"] = True
                    cl.sendMessage(to,"send some picture for saveing~")
                elif text.lower() == 'savelolipic off':
                    wait["pic"] = False
                    backupData()
                    cl.sendMessage(to, "saveing...")
                elif text.lower() == 'savepic on':
                    wait["monmonpic"] = True
                    cl.sendMessage(to,"send some picture for saveing~")
                elif text.lower() == 'savepic off':
                    wait["monmonpic"] = False
                    backupData()
                    cl.sendMessage(to, "saveing...")
                elif text.lower() == 'pro on':
                    if msg.toType ==2:
                        settings["protect"][to] = True
                        settings["qrprotect"][to] = True
                        settings["invprotect"][to] = True
                        cl.sendMessage(to, "踢人保護開啟")
                        cl.sendMessage(to, "網址保護開啟")
                        cl.sendMessage(to, "邀請保護開啟")
                elif text.lower() == 'pro off':
                    if msg.toType ==2:
                        G = cl.getGroup(msg.to)
                        try:
                            del settings["protect"][G.id]
                            cl.sendMessage(to, "踢人保護關閉")
                        except:
                            pass
                        try:
                            del settings["qrprotect"][G.id]
                            cl.sendMessage(to, "網址保護關閉")
                        except:
                            pass
                        try:
                            del settings["invprotect"][G.id]
                            cl.sendMessage(to, "邀請保護關閉")
                        except:
                            pass
                elif msg.text.lower().startswith("adminadd ") or msg.text.lower().startswith("add "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    if inkey not in ban["admin"] and inkey not in ban["blacklist"] and inkey not in owners: 
                        ban["admin"].append(str(inkey))
                        cl.sendMessage(to, "已獲得權限！")
                        json.dump(ban, codecs.open('ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                elif msg.text.lower().startswith("admindel ") or msg.text.lower().startswith("del "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    if inkey in ban["admin"]:
                        ban["admin"].remove(str(inkey))
                        cl.sendMessage(to, "已取消權限！")
                        json.dump(ban, codecs.open('ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                elif msg.text.lower().startswith("tk "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            cl.sendMessage(to,"Fuck you")
                            cl.kickoutFromGroup(msg.to,[target])
                        except:
                            cl.sendMessage(to,"Error")
                elif text.lower().startswith("nk "):
                    if msg.toType == 2:
                        _name = msg.text.replace("Nk ","")
                        gs = cl.getGroup(msg.to)
                        targets = []
                        for g in gs.members:
                            if _name in g.displayName:
                                targets.append(g.mid)
                        if targets == []:
                            cl.sendMessage(msg.to,"Not Found")
                        else:
                            for target in targets:
                                try:
                                    cl.kickoutFromGroup(msg.to,[target])
                                except:
                                    pass
                elif text.lower() in ['byeall','.kickall','kickall']:
                    if msg.toType == 2:
                        gs = cl.getGroup(msg.to)
                        for g in gs.members:
                            try:
                                cl.kickoutFromGroup(msg.to,[g.mid])
                                cl.sendContact(to,"\'")
                                sleep(0.2)
                            except:
                                pass
                elif text.lower() == 'cancel':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        gMembMids = [contact.mid for contact in group.invitee]
                    for _mid in gMembMids:
                        cl.cancelGroupInvitation(msg.to,[_mid])
                        sleep(0.3)
                    cl.sendMessage(msg.to,"已取消所有邀請!")
                elif text.lower().startswith("inv "):
                    if msg.toType == 2:
                        midd = text.split(' ')
                        cl.findAndAddContactsByMid(midd)
                        cl.inviteIntoGroup(to,[midd])
#==============================================================================#
                elif msg.text.lower().startswith("ban "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        if target not in owners :
                            try:
                                ban["blacklist"][target] = True
                                cl.sendMessage(msg.to,"已加入黑單!")
                                json.dump(ban, codecs.open('ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                            except:
                                cl.sendMessage(msg.to,"添加失敗 !")
                elif text.lower().startswith("ban :"):
                    txt = text.replace("Ban :","")
                    if txt not in owners and len(txt) ==33 and txt.lower.startswith("u"):
                        ban["blacklist"][txt] = True
                        cl.sendMessage(msg.to,"已加入黑單!")
                        json.dump(ban, codecs.open('ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                    else:
                        cl.sendMessage(msg.to,"添加失敗 !")
                elif text.lower().startswith("unban :"):
                    txt = text.replace("Unban :","")
                    if txt in ban["blacklist"] :
                        del ban["blacklist"][txt]
                        cl.sendMessage(msg.to,"已刪除黑單!")
                        json.dump(ban, codecs.open('ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                    else:
                        cl.sendMessage(msg.to,"此人不在黑單之中 !")
                elif msg.text.lower().startswith("unban "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            del ban["blacklist"][target]
                            cl.sendMessage(msg.to,"刪除成功 !")
                            json.dump(ban, codecs.open('ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                        except:
                            cl.sendMessage(msg.to,"刪除失敗 !")
                elif text.lower() in ['kickban','killban']:
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        gMembMids = [contact.mid for contact in group.members]
                        matched_list = []
                    for tag in ban["blacklist"]:
                        matched_list+=filter(lambda str: str == tag, gMembMids)
                    if matched_list == []:
                        cl.sendMessage(msg.to,"There was no blacklist user")
                        return
                    for jj in matched_list:
                        cl.kickoutFromGroup(msg.to,[jj])
                    cl.sendMessage(msg.to,"Blacklist kicked out")
                elif text.lower() in ['cleanban','clear ban','clearban']:
                    for mi_d in ban["blacklist"]:
                        ban["blacklist"] = {}
                    cl.sendMessage(to, "已清空黑名單")
#==============================================================================#
                elif text.lower().startswith("fbc:"):
                    bctxt = text.split(':')
                    t = cl.getAllContactIds()
                    for manusia in t:
                        cl.sendMessage(manusia,bctxt[1])
                elif text.lower().startswith("gbc:"):
                    bctxt = text.split(':')
                    n = cl.getGroupIdsJoined()
                    if len(bctxt)==2:
                        for g in n:
                            cl.sendMessage(g,bctxt[1])
            if text.lower() == 'cc9487':
                if sender in ['ua10c2ad470b4b6e972954e1140ad1891']:
                    sys.exit()
#==============================================================================#
        if op.type == 25 or op.type == 26:
            msg=op.message
            sender = msg._from
            receiver = msg.to
            text = msg.text
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 1:
                if sender in wait['reply']:
                    settings['changeGroupPicture'][wait['reply'][sender]] = cl.downloadObjectMsg(msg.id, saveAs="linepy/tmp/{}.jpg".format(wait['reply'][sender]))
                    del wait['reply'][sender]
                    cl.sendMessage(to,'ok')
            if msg.contentType == 13:
                if settings["getmid"] == True:
                    contact = cl.getContact(msg.contentMetadata["mid"])
                    cl.sendMessage(to, "[ 名字 ]\n" + contact.displayName +"\n[ 個簽 ]\n" + contact.statusMessage +"\n[ MID ]\n" + contact.mid)
                    path = "http://dl.profile.line-cdn.net/" + contact.pictureStatus
                    cl.sendImageWithURL(to, str(path))
                    path = cl.getProfileCoverURL(msg.contentMetadata["mid"])
                    cl.sendImageWithURL(to, str(path))
                if wait["ban"] ==True:
                    if msg._from in owners and msg.contentMetadata["mid"] not in owners and msg.contentMetadata["mid"] not in ban["admin"]:
                        ban["blacklist"][msg.contentMetadata["mid"]]=True
                        cl.sendMessage(to,"OK")
                        json.dump(ban, codecs.open('ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                        wait["ban"] =False
                if wait["unban"] ==True:
                    if msg._from in owners:
                        if msg.contentMetadata["mid"] in ban["blacklist"]:
                            del ban["blacklist"][msg.contentMetadata["mid"]]
                            json.dump(ban, codecs.open('ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                            cl.sendMessage(to,"OK")
                            wait["unban"] =False
                        else:
                            cl.sendMessage(to,"User is not in banlist")
                if wait["getmid"] ==True:
                    if msg._from in owners or msg._from in ban["admin"]:
                        cl.sendMessage(to,msg.contentMetadata["mid"])
                        wait["getmid"] =False
        if op.type == 26:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            elif msg.toType == 2:
                to = receiver
            if sender in ban["blacklist"]:
                return
            if msg.contentType == 16:
                if settings["timeline"] == True:
                    if msg.contentMetadata["serviceType"] == "GB" or msg.contentMetadata['serviceType'] == 'MH':
                        ret_ = "═══文章預覽═══"
                        ret_ += "\n[文章作者 ]\n @!"
                        if "text" in msg.contentMetadata:
                            ret_ += "\n[ 文章詳情 ]\n"+msg.contentMetadata["text"]
                        ret_ += "\n[ URL ]\n {}".format(str(msg.contentMetadata["postEndUrl"]).replace("line://","https://line.me/R/"))
                        if "mediaOid" in msg.contentMetadata:
                            object_ = msg.contentMetadata["mediaOid"].replace("svc=myhome|sid=h|","")
                            if msg.contentMetadata["mediaType"] == "V":
                                if msg.contentMetadata["serviceType"] == "GB":
                                    ourl = "\n[ Objek URL ]\n https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
                                    murl = "\n[ Media URL ]\n https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(msg.contentMetadata["mediaOid"]))
                                elif msg.contentMetadata['serviceType'] == 'MH':
                                    ourl = "\n[ Objek URL ]\n https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
                                    murl = "\n[ Media URL ]\n https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(object_))
                                ret_ += murl
                            else:
                                if msg.contentMetadata["serviceType"] == "GB":
                                    ourl = "\n[ Objek URL ]\n https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
                                elif msg.contentMetadata['serviceType'] == 'MH':
                                    ourl = "\n[ Objek URL ]\n https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
                            ret_ += ourl
                        if "stickerId" in msg.contentMetadata:
                            ret_ += "\n[ 貼圖訊息 ]\n https://line.me/R/shop/detail/{}".format(str(msg.contentMetadata["packageId"]))
                        if msg.contentMetadata['serviceType'] == 'MH':
                            f = msg.contentMetadata["postEndUrl"].split('userMid=')
                            s = f[1].split('&')
                            sendMention(msg.to, ret_,[s[0]])
                        elif msg.contentMetadata["serviceType"] == "GB":
                            sendMention(msg.to, ret_,[sender])
            elif msg.contentType == 0 :
                if "/ti/g/" in msg.text.lower():
                    if sender in owners or sender in ban["bots"]:
                        if settings["autoJoinTicket"] == True:
                            link_re = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
                            links = link_re.findall(text)
                            n_links = []
                            for l in links:
                                if l not in n_links:
                                    n_links.append(l)
                            for ticket_id in n_links:
                                group = cl.findGroupByTicket(ticket_id)
                                cl.acceptGroupInvitationByTicket(group.id,ticket_id)
            if settings["autoRead"] == True:
                cl.sendChatChecked(to, msg_id)
            if msg.contentType == 0 and sender not in owners and msg.toType == 2:
                if 'MENTION' in msg.contentMetadata.keys()!= None:
                    names = re.findall(r'@(\w+)', text)
                    mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                    mentionees = mention['MENTIONEES']
                    lists = []
                    for mention in mentionees:
                        if clMID in mention["M"]:
                            if settings["detectMention"] == True:
                                contact = cl.getContact(sender)
                                sendMention(to,"@! 標毛?", [contact.mid])
                            break
            if to in settings["reread"]:
                if msg.contentType == 0:
                    msg_dict[msg.id] = {"text":msg.text,"from":msg._from,"createdTime":time.time()}
                elif msg.contentType == 7:
                    stk_id = msg.contentMetadata['STKID']
                    cl.sendMessage(to,stk_id)
                    msg_dict[msg.id] = {"from":msg._from,"stkid": stk_id ,"createdTime":time.time()}
                elif msg.contentType == 13:
                    mid = msg.contentMetadata["mid"]
                    msg_dict[msg.id] = {"from":msg._from,"mid": mid ,"createdTime":time.time()}
#==============================================================================#
        if op.type == 65:
            try:
                msg = op.message
                at = op.param1
                msg_id = op.param2
                if op.param1 in settings["reread"]:
                    if msg_id in msg_dict:
                        timeNow = time.time()
                        opi=[]
                        opi.append(msg_dict[msg_id]["from"])
                        if "text" in msg_dict[msg_id]:
                            sendMention(at,"[收回訊息者]\n @! \n[訊息內容]\n"+str(msg_dict[msg_id]["text"]),opi)
                            cl.sendMessage(at,"收回時間"+str(timeNow - msg_dict[msg_id]["createdTime"])+"秒之前")
                            del msg_dict[msg_id]
                        elif "stkid" in msg_dict[msg_id]:
                            path = "https://stickershop.line-scdn.net/stickershop/v1/sticker/{}/ANDROID/sticker.png;compress=true".format(msg_dict[msg_id]["stkid"])
                            sendMention(at,"[收回訊息者]\n @! \n[訊息內容]\n一張貼圖",opi)
                            cl.sendImageWithURL(at,path)
                            cl.sendMessage(at,"收回時間"+str(timeNow - msg_dict[msg_id]["createdTime"])+"秒之前")
                            del msg_dict[msg_id]
                        elif "mid" in msg_dict[msg_id]:
                            sendMention(at,"[收回訊息者]\n @! \n[訊息內容]\n一則友資",opi)
                            cl.sendContact(at,msg_dict[msg_id]["mid"])
                            cl.sendMessage(at,"收回時間"+str(timeNow - msg_dict[msg_id]["createdTime"])+"秒之前")
                            del msg_dict[msg_id]
                    else:
                        print("unsend")
            except Exception as e:
                print (e)
#==============================================================================#
        if op.type == 55:
            try:
                if op.param1 in wait2['readPoint']:
                    Name = cl.getContact(op.param2).displayName
                    if Name in wait2['readMember'][op.param1]:
                        pass
                    else:
                        wait2['readMember'][op.param1] += "\n[※]" + Name
                        wait2['ROM'][op.param1][op.param2] = "[※]" + Name
                        print (time.time() + name)
                else:
                    pass
            except:
                pass
    except Exception as error:
        logError(error)
#==============================================================================#
while 1:
    if time.time() -botStart > 18000 :
        restartBot()
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)


