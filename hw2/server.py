# -*- coding: utf-8 -*-
from __future__ import print_function
import socket
import random
import Tkinter as tk

poker = []
pokerUsed = 0

havePoker = 0
banker = []

def windowInit():
  blackjack = tk.Tk()
  blackjack.title('blackjack')
  blackjack.geometry('400x300')

  hit = tk.Button(blackjack, text='hit')
  stand = tk.Button(blackjack, text='stand')

  hit.grid(column=0, row=0)
  stand.grid(column=1, row=0)
  blackjack.mainloop()

def serverOn():
  HOST = '127.0.0.1'
  PORT = 8001

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((HOST, PORT))
  s.listen(5)

  print('Server start at: %s:%s' %(HOST, PORT))
  print('wait for connection...')

  while True:
    conn, addr = s.accept()
    print('Connected by ', addr)

  while True:
    data = conn.recv(1024)
    print(data)

    conn.send("server received you message.")

  conn.close()

def checkPoker(num):
  pokerNum = num % 13
  if (pokerNum == 0):
    pokerNum = 13

  pokerType = ''
  pokerTypeCalc = num / 13
  if (pokerTypeCalc == 0):
    # ♠
    pokerType = 's'
  elif (pokerTypeCalc == 1):
    # ♥
    pokerType = 'h'
  elif (pokerTypeCalc == 2):
    # ♦
    pokerType = 'd'
  elif (pokerTypeCalc >= 3):
    # ♣
    pokerType = 'c'
  return {'type': pokerType, 'num': pokerNum}

def init():
  for i in range(1, 53):
    poker.append(i)

  # Shuffle
  for i in range(52):
    pokerRand = random.randint(0, 51)
    poker[i], poker[pokerRand] = poker[pokerRand], poker[i]
    # print(checkPoker(poker[i]))

def needPoker():
  global pokerUsed
  banker.append(poker[pokerUsed])
  pokerUsed += 1
def getStart():

  for i in range(2):
      needPoker()

def main():
  init()
  windowInit()

if __name__ == '__main__':
  main()
