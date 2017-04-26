# -*- coding: utf-8 -*-
from __future__ import print_function
import select, random, json, os, socket

poker = []
pokerUsed = 0

def broadcast_data (sock, message):
  for socket in CONNECTION_LIST:
    if socket != server_socket :
      try :
        socket.send(message)
      except :
        socket.close()
        CONNECTION_LIST.remove(socket)

def checkPoker(num):
  pokerNum = num % 13
  pokerNumSign = ''

  if (pokerNum == 11):
    pokerNumSign = 'J'
  elif (pokerNum == 12):
    pokerNumSign = 'Q'
  elif (pokerNum == 0):
    pokerNumSign = 'K'
  else:
    pokerNumSign = str(pokerNum)

  pokerType = ''
  pokerTypeCalc = num / 13
  if (pokerTypeCalc == 0):
    pokerType = u'♠ '
  elif (pokerTypeCalc == 1):
    pokerType = u'♥ '
  elif (pokerTypeCalc == 2):
    pokerType = u'♦ '
  elif (pokerTypeCalc >= 3):
    pokerType = u'♣ '
  
  sign = pokerType + pokerNumSign

  return sign

class Player:
  def __init__(self, cards, points, safe):
    self.cards = cards
    self.points = points
    self.safe = safe

  def __new___(cls, cards, points, safe):
    return object.__new__(cls)

  def hit(self):
    global pokerUsed
    if (self.safe):
      self.cards.append(poker[pokerUsed])
      pokerUsed += 1

      self.calcPoint()

      if (self.points > 21):
        self.safe = False

  def stand(self):
    self.safe = False

  def calcPoint(self):
    totNum = 0

    for num in self.cards:
      pokerNum = num % 13
      if (pokerNum == 0):
        pokerNum = 13
      if (pokerNum >= 10):
        totNum += 10
      elif (pokerNum == 1):
        totNum += 11
      else:
        totNum += pokerNum
    
    for num in self.cards:
      if (totNum > 21 and (num % 13) == 1):
        totNum -= 10
      
    self.points = totNum

  def getData(self):
    return {
      'cards': self.cards,
      'point': self.points
    }

def shuffle():
  global pokerUsed, poker
  pokerUsed = 0
  poker = []
  for i in range(1, 53):
    poker.append(i)

  # Shuffle
  for i in range(52):
    pokerRand = random.randint(0, 51)
    poker[i], poker[pokerRand] = poker[pokerRand], poker[i]

if __name__ == '__main__':

  # List to keep track of socket descriptors
  CONNECTION_LIST = []
  RECV_BUFFER = 4096
  # Advisable to keep it as an exponent of 2
  PORT = 5000

  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # this has no effect, why ?
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server_socket.bind(('0.0.0.0', PORT))
  server_socket.listen(10)

  # Add server socket to the list of readable connections
  CONNECTION_LIST.append(server_socket)

  print('server started on port ' + str(PORT))
  players = []
  ready = 0
  whoPlay = 1
  start = False

  # creat banker
  players.append(Player([], 0, True))

  
  while 1:
    # Get the list sockets which are ready to be read through select
    read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])

    for sock in read_sockets:
      #New connection
      if sock == server_socket:
        # Handle the case in which there is a new connection recieved through server_socket
        sockfd, addr = server_socket.accept()
        CONNECTION_LIST.append(sockfd)

        # print('Client (%s, %s) connected' % addr)
        playerID = len(players)
        if (playerID <= 3):
          sockfd.send(str(playerID))
          players.append(Player([], 0, True))

      #Some incoming message from a client
      else:
        # Data recieved from client, process it
        try:
          # In Windows, sometimes when a TCP program closes abruptly, a 'Connection reset by peer' exception will be thrown
          data = sock.recv(RECV_BUFFER)

          if data:
            if (data == 'ready'):
              ready += 1

            if (len(players)-1 == ready and (not start)):
              shuffle()
              for player in players:
                for i in range(2):
                  player.hit()
              start = True
              broadcast_data(sock, 'start')

            if (data == 'hit'):
              players[whoPlay].hit()
              data = 'sendData'

            if (data == 'stand'):
              whoPlay += 1
              # banker turn
              if (whoPlay > len(players)-1):
                while True:
                  if (players[0].points < 17):
                    players[0].hit()
                  else:
                    break
                data = 'endGame'
              else:
                broadcast_data(sock, str(whoPlay))
                data = 'sendData'
            
            if (data == 'sendData'):
              sendData = []
              for player in players:
                sendData.append(player.getData())
              # print(json.dumps(sendData))
              broadcast_data(sock, json.dumps(sendData))

            if (data == 'endGame'):
              broadcast_data(sock, 'gameover')
              print('---遊戲結果---')
              pointList = []
              
              playerNum = 0
              for player in players:
                cards = player.cards
                points = player.points
                if (playerNum == 0):
                  print('Banker Point ', str(points))
                else:
                  print('Player' + str(playerNum) + ' Point ', str(points))
                for num in cards:
                  print(checkPoker(num), end='')
                print('')

                if (points > 21):
                  pointList.append(0)
                else:
                  pointList.append(points)
                playerNum += 1

              bankerPoint = pointList[0]
              playerNum = 1
              print('')

              for point in range(1, len(pointList)):
                if (bankerPoint >= pointList[point]):
                  print('Player ' + str(playerNum) + ' vs 莊家 莊家勝利')
                else:
                  print('Player' + str(playerNum) + ' vs 莊家 Player' + playerNum + '勝利')
                playerNum += 1
              print('請重開連線重新開始')
              print('--------------')

        except:
          broadcast_data(sock, 'Client (%s, %s) is offline' % addr)
          print('Client (%s, %s) is offline' % addr)
          whoPlay -= 1
          sock.close()
          CONNECTION_LIST.remove(sock)
          continue

  server_socket.close()