from socket import *
import time
import json
import threading

#protocol
LOGIN = 1               # name, success

CHAT = 10               # text
DIRECT_CHAT = 11        # receiver, DMtext

SHOW_LIST = 20          # userName, addr

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('127.0.0.1', 2323))
name = input('TYPE YOUR NAME: ')
dic = {'option' : LOGIN, 'name' : name, 'success': ' '}
clientSock.send(json.dumps(dic).encode('utf-8'))


print('CONFIRM CONNECTION')
sign = True
def RecvThread():
    while True:
        global sign
        try:
            data = clientSock.recv(1024)
        except error:
            break
        datalist = data.split(b'}')
        for data in datalist:
            if data == b'':
                continue
            data+=(b'}')
            dic = json.loads(data)
            if dic['option'] == LOGIN and dic['sucess'] == 0:
                if dic['errorType'] == 0:
                    print("DUPLICATED NAME")
                elif dic['errorType'] == 1:
                    print("CHAT IS FULL")
                clientSock.close()
                sign = False
                break
            elif dic['option'] == CHAT:
                print(dic['name']+' : '+ dic['text'])         
            elif dic['option'] == SHOW_LIST: #list
                print('Name: ',dic['userName'] + ' ' + 'ADDRESS: ',dic['addr'])
                #print ('Port: ',dic['port'])
            elif dic['option'] == DIRECT_CHAT: #list
                print(dic['name'] + ' : ' + dic['DMtext'])
        if sign == False:
            break
            

t = threading.Thread(target=RecvThread)
t.start()


while True:
    text = input('')
    if sign == False:
        break
    if text == '\list':
        dic = {'option' : SHOW_LIST}
    elif text =='\dm':
        receiverName = input('NAME INPUT: ')
        DMtext = input('=> ')
        dic = {'option' : DIRECT_CHAT, 'receiver' : receiverName ,'DMtext' : DMtext}
    elif text =='\quit':
        break
    else :  
        dic = {'option' : CHAT, 'text' : text}   # chat
    clientSock.send(json.dumps(dic).encode('utf-8'))
clientSock.close()
# elif option == '\list':
#     dic = {'option' : '3'}
#     clientSock.send(json.dumps(dic).encode('utf-8'))
# elif option == '\dm':
#     dic = {'option' : 'dm'}
#     clientSock.send(json.dumps(dic).encode('utf-8'))




    










#.reverse()