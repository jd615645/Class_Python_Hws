# -*- coding: utf-8 -*-
from __future__ import print_function
import select, random, json, os, socket
from Tkinter import *

# 0 => join game
# 1 => wait start
# 2 => wait playing
# 3 => playing
# 4 => wait ending
nowStatus = 0
playerID = -1

getMsg = False

def main():
  global nowStatus, getMsg

  host = '127.0.0.1'
  port = 5000

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.settimeout(2)

  # connect to remote host
  try :
    s.connect((host, port))
  except :
    print('Unable to connect')
    sys.exit()

  print('Connected to remote host. Start sending messages')

  while 1:
    socket_list = [sys.stdin, s]

    # Get the list sockets which are readable
    read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

    for sock in read_sockets:
      #incoming message from remote server

      if sock == s:
        # 接收資料
        data = sock.recv(4096)
        if not data :
          print('Disconnected from chat server')
          sys.exit()
        else :
          if (getMsg):
            print(data)
            getMsg = False
          
          if (nowStatus == 0):
            playerID = int(data)
            nowStatus = 1
            print('player: ' + data)
            print('按任何按鍵準備遊戲')
          elif (nowStatus == 1 and data == 'start'):
            print('開始遊戲')
            if (playerID == 1):
              print('輪到你了')
              print('是否繼續要牌')
              nowStatus = 3
              getMsg = True
              s.send('sendData')
            else:
              print('輪到 player1')
              nowStatus = 2
          elif (nowStatus == 2 and data == str(playerID)):
            print('輪到你了')
            print('是否繼續要牌')
            nowStatus = 3
          elif (nowStatus == 3 and data == 'stand'):
            nowStatus = 4

          print('-----')
          print('send: ' + data)
          print('nowStatus: ' + str(nowStatus))
          print('-----')
          
      #user entered a message
      else :
        # 發送資料
        if (nowStatus == 1):
          msg = raw_input()
          print('等待其他玩家')
          s.send('ready')
        elif (nowStatus == 2):
          msg = raw_input()
          print('還未輪到你')
        elif (nowStatus == 3):
          msg = raw_input()
          if (msg == 'y'):
            print('hit')
            s.send('hit')
            getMsg = True
          else:
            if (playerID != 0):
              s.send('stand')
            else:
              s.send('endGame')
            nowStatus = 4
            print('等待遊戲結束')
        elif (nowStatus == 4):
          print('等待遊戲結束')

#main function
if __name__ == '__main__':
  main()