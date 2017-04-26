# -*- coding: utf-8 -*-
from __future__ import print_function
import select, random, json, os, socket

# 0 => join game
# 1 => wait start
# 2 => wait playing
# 3 => playing
# 4 => wait ending
# 5 => end
nowStatus = 0
playerID = -1

def checkPoker(num):
  pokerNum = num % 13
  pokerNumSign = ''
  if (pokerNum == 11):
    pokerNumSign = 'J '
  elif (pokerNum == 12):
    pokerNumSign = 'Q '
  elif (pokerNum == 0):
    pokerNumSign = 'K '
  else:
    pokerNumSign = str(pokerNum) + ' '

  pokerType = ''
  pokerTypeCalc = num / 13
  if (pokerTypeCalc == 0):
    pokerType = '♠ '
  elif (pokerTypeCalc == 1):
    pokerType = '♥ '
  elif (pokerTypeCalc == 2):
    pokerType = '♦ '
  elif (pokerTypeCalc >= 3):
    pokerType = '♣ '

  return pokerType + pokerNumSign

def main():
  global nowStatus, getMsg

  host = '127.0.0.1'
  port = 5000
  gameData = []

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
          if (nowStatus == 0):
            playerID = int(data)
            nowStatus = 1
            print('player: ' + data)
            print('按任何按鍵準備遊戲')
          elif (nowStatus == 1 and data == 'start'):
            print('\n------開始遊戲------')
            if (playerID == 1):
              print('輪到你, 是否繼續要牌(y), 任意鍵取消')
              nowStatus = 3
              s.send('sendData')
            else:
              print('輪到 player1')
              nowStatus = 2
          elif (nowStatus == 2 and data == str(playerID)):
            print('輪到你, 是否繼續要牌(y), 任意鍵取消')
            nowStatus = 3
          elif (nowStatus == 3 and data == 'stand'):
            print('輪到下位玩家')
            nowStatus = 4

          elif (nowStatus == 3):
            try:
              gameData = json.loads(data)
              # banker
              cards = gameData[0][u'cards']
              print('\nBanker ')
              printCard = ''
              print('* ', end='')
              for num in range(1, len(cards)):
                print(checkPoker(cards[num]), end='')
              print('')
              # player
              cards = gameData[playerID][u'cards']
              points = gameData[playerID][u'point']
              print('Player ' + str(playerID) + ' Point ', str(points))
              printCard = ''
              for num in cards:
                print(checkPoker(num), end='')
              print('\n')
              if (points > 21):
                nowStatus == 4
                print('爆了, 按任意鍵繼續')
                # s.send('stand')
            except:
              print('', end='')

          elif (nowStatus == 4 and data == 'gameover'):
            print('\n---結束遊戲成績結算---')
            # banker
            bankerPoint = gameData[0][u'point']
            if (bankerPoint > 21):
              bankerPoint = 0
            cards = gameData[0][u'cards']
            print('\nBanker ')
            printCard = ''
            print('* ', end='')
            for num in range(1, len(cards)):
              print(checkPoker(cards[num]), end='')
            print('')
            # player
            cards = gameData[playerID][u'cards']
            points = gameData[playerID][u'point']
            if (points > 21):
              points = 0
            print('Player ' + str(playerID) + ' Point ', str(points))
            printCard = ''
            for num in cards:
              print(checkPoker(num), end='')
            print('\n')
            # game sol
            print('Player' + str(playerID) + ' vs 莊家! ', end='')
            if (bankerPoint >= points):
              print('莊家勝利')
            else:
              print('Player' + str(playerID) + '勝利')
            print('請斷線後重開連線重新開始')
          
      #user entered a message
      else :
        # 發送資料
        if (nowStatus == 1):
          msg = raw_input()
          print('等待其他玩家...')
          s.send('ready')
        elif (nowStatus == 2):
          msg = raw_input()
          print('還未輪到你\n')
        elif (nowStatus == 3):
          msg = raw_input()
          if (msg == 'y'):
            s.send('hit')
          else:
            print('輪到下位玩家')
            if (playerID != 0):
              s.send('stand')
            else:
              s.send('endGame')
            nowStatus = 4
            print('等待遊戲結束...')

#main function
if __name__ == '__main__':
  main()