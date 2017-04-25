# -*- coding: utf-8 -*-
from __future__ import print_function
import select, random, json, os, socket

poker = []
pokerUsed = 0
playerLimit = 4

def broadcast_data (sock, message):
  for socket in CONNECTION_LIST:
    if socket != server_socket :
      try :
        socket.send(message)
      except :
        socket.close()
        CONNECTION_LIST.remove(socket)

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

      getPoker = poker[pokerUsed]
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
        if (totNum+11 > 21):
          totNum += 1
        else:
          totNum += 11
      else:
        totNum += pokerNum
    self.points = totNum

  def getData(self):
    return {
      'cards': self.cards,
      'point': self.points
    }

def shuffle():
  pokerUsed = 0
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


  print('Chat server started on port ' + str(PORT))
  players = []
  ready = 0
  whoPlay = 1
  start = False
  while 1:
    # Get the list sockets which are ready to be read through select
    read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])

    for sock in read_sockets:
      #New connection
      if sock == server_socket:
        # Handle the case in which there is a new connection recieved through server_socket
        sockfd, addr = server_socket.accept()
        CONNECTION_LIST.append(sockfd)

        print('Client (%s, %s) connected' % addr)
        if (len(players) <= 5):
          sockfd.send(str(len(players)))
          players.append(Player([], 0, True))

        # broadcast_data(sockfd, '[%s:%s] entered roomn\n' % addr)

      #Some incoming message from a client
      else:
        # Data recieved from client, process it
        try:
          # In Windows, sometimes when a TCP program closes abruptly,
          # a 'Connection reset by peer' exception will be thrown
          data = sock.recv(RECV_BUFFER)

          if data:
            print('data: ' + data)

            if (data == 'ready'):
              ready += 1

            if (len(players) == ready and ready > 1 and (not start)):
              shuffle()
              broadcast_data(sock, 'start')
              for player in players:
                for i in range(2):
                  player.hit()
              start = True
              print('whoPlay: ' + str(whoPlay))

            if (data == 'hit'):
              if (players[whoPlay].safe):
                print('hit')
                players[whoPlay].hit()
                data = 'sendData'
              else:
                print('stand')
                data = 'stand'
            
            if (data == 'stand'):
              if (whoPlay ==0):
                # use endGame fun
                data = 'endGame'
              else:
                whoPlay += 1
                if (whoPlay > len(players)-1):
                  whoPlay = 0
                broadcast_data(sock, str(whoPlay))
                data = 'sendData'
            
            if (data == 'sendData'):
              print('sendData')
              sendData = []
              for player in players:
                sendData.append(player.getData())
              print(str(sendData))
              broadcast_data(sock, str(sendData))

            if (data == 'endGame'):
              print('---遊戲結果---')
              pointList = []
              for player in players:
                if (player.points > 21):
                  pointList.append(0)
                else:
                  pointList.append(player.points)
              bankerPoint = pointList[0]
              playerNum = 1
              for point in range(1, len(pointList)):
                if (bankerPoint >= point):
                  print('Player' + playerNum + 'vs 莊家 莊家勝利')
                else:
                  print('Player' + playerNum + 'vs 莊家 Player' + playerNum + '勝利')
                playerNum += 1
              print('--------------')
                

        except:
          broadcast_data(sock, 'Client (%s, %s) is offline' % addr)
          print('Client (%s, %s) is offline' % addr)
          whoPlay -= 1
          sock.close()
          CONNECTION_LIST.remove(sock)
          continue

  server_socket.close()