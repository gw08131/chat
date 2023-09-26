from socket import *
import time
import json
import threading

#protocol
LOGIN = 1

CHAT = 10
DIRECT_CHAT = 11

SHOW_LIST = 20



startTime=time.time()
serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('', 2323))
serverSock.listen(1)

UserList = []
count = 0

class User:
    def __init__(self,Socket,addr):
        self.Socket = Socket
        self.addr = addr
        self.name = ''
        self.receiverName = ''
    def SetName(self,name):
        self.name = name
    def GetName(self):
        return self.name
    def getSocket(self):
        return self.Socket

    # def FindReceiverName(self,receiverName):
    #     UserList.name = receiverName

def RecvThread(user):
    global count
    connectionSock = user.getSocket()
    while True:
        sign = True
        try:
            data = connectionSock.recv(1024)
        except ConnectionError:
            UserList.remove(user)
            break
        if data == b'':
            UserList.remove(user)
            break
        dic = json.loads(data) 
        
        if dic['option'] == LOGIN:
            count += 1
            user.SetName(dic['name'])
            for client in UserList:
                if client != user:
                    if dic['name'] == client.GetName():
                        sign = False
                        dic['errorType'] = 0    # 중복 로그인
            if count == 3:
                sign = False
                dic['errorType'] = 1    # 룸 풀
            if sign == False:
                dic['sucess'] = 0
                connectionSock.send(json.dumps(dic).encode('utf-8'))
                UserList.remove(user)
                count-= 1

        elif dic['option']== CHAT:
            dic['name'] = user.GetName() #내 이름 가져오기 (내가 보내는 사람)
            for client in UserList:
                if client != user:
                    client.getSocket().send(json.dumps(dic).encode('utf-8')) 
                    #Userlist에서 나 자산을 제외한 사람에게 내 text 보여주기
        # user list
        elif dic['option']== SHOW_LIST: 
            for client in UserList:
                dic['userName'] = client.name
                dic['addr'] = client.addr
                connectionSock.send(json.dumps(dic).encode('utf-8'))

        # DM
        elif dic['option']== DIRECT_CHAT:
            dic['name'] = user.GetName() #내 이름 가져오기 (내가 보내는 사람)
            for receiverName in UserList:
                if receiverName != user and dic['receiver'] == receiverName.name: 
                    receiverName.getSocket().send(json.dumps(dic).encode('utf-8')) 
                    
        # elif dic['option'] == '2':
        #     dic['text'] = dic['text'][::-1]
        #     connectionSock.send(json.dumps(dic).encode('utf-8'))
           
        # elif dic['option'] == '3':
        #     dic['ip'] = ip;
        #     dic['port'] =port;
        #     connectionSock.send(json.dumps(dic).encode('utf-8'))
        # elif dic['option'] == '4':
        #     currentTime=time.time()
        #     dic['text'] = time.strftime('%H:%M:%S', time.gmtime(currentTime-startTime))
        #     connectionSock.send(json.dumps(dic).encode('utf-8'))
        elif dic['option'] == b'5':
            break
        if sign == False:
            break

while True:
    
    connectionSock, addr = serverSock.accept()  # 또 block
    print(str(addr),'에서 접속이 확인되었습니다.')
    user = User(connectionSock, addr)
    ip,port = addr
    #'port' = b'port'
    UserList.append(user)
    t = threading.Thread(target=RecvThread, args=(user,))
    t.start()
    

while True:
    

    
    while True:
        try:
            data = connectionSock.recv(1024)
        except ConnectionError:
            break
        if data == b'':
            break
        dic = json.loads(data) 
        
        if dic['option']== '1':
            dic['text'] = dic['text'].upper()
            connectionSock.send(json.dumps(dic).encode('utf-8'))
           
        elif dic['option'] == '2':
            dic['text'] = dic['text'][::-1]
            connectionSock.send(json.dumps(dic).encode('utf-8'))
           
        elif dic['option'] == '3':
            dic['ip'] = ip;
            dic['port'] =port;
            connectionSock.send(json.dumps(dic).encode('utf-8'))
        elif dic['option'] == '4':
            currentTime=time.time()
            dic['text'] = time.strftime('%H:%M:%S', time.gmtime(currentTime-startTime))
            connectionSock.send(json.dumps(dic).encode('utf-8'))
        elif dic['option'] == b'5':
            break
    

