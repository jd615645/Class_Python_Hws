# -*- coding: utf-8 -*-
from __future__ import print_function
import socket
import random
import json
from Tkinter import *

poker = []
pokerUsed = 0

havePoker = 0
banker = []

cardPath = []
bankerCards = []
bankerPoints = 0

class player:
  def __init__(self, card, point, stop):
    self.card = []
    self.point = 0
    self.stop = FALSE

  def hit():
    global pokerUsed
    if (not self.stop):
      nowcard = len(banker)
      banker.append(poker[pokerUsed])

      getPoker = poker[pokerUsed]

      # Label(text=checkPoker(getPoker)).grid(row=0, column=nowcard)
      # img = PhotoImage(file='./card/bg.png')

      pokerUsed += 1
      bankerPoints = calc(banker)
      # Label(text=bankerPoints).grid(row=0, column=1)
      print(bankerPoints)
    else:
      print()


def windowInit():
  blackjack = Tk()
  blackjack.title('blackjack')
  blackjack.geometry('400x300')

  Label(blackjack, text='莊家').grid(row=0, column=0)
  Label(blackjack, text='0').grid(row=0, column=1)

  cardPath = [
    PhotoImage(file='./card/bg.png'),
    PhotoImage(file='./card/1.png'),
    PhotoImage(file='./card/2.png'),
    PhotoImage(file='./card/3.png'),
    PhotoImage(file='./card/4.png'),
    PhotoImage(file='./card/5.png'),
    PhotoImage(file='./card/6.png'),
    PhotoImage(file='./card/7.png'),
    PhotoImage(file='./card/8.png'),
    PhotoImage(file='./card/9.png'),
    PhotoImage(file='./card/10.png'),
    PhotoImage(file='./card/11.png'),
    PhotoImage(file='./card/12.png'),
    PhotoImage(file='./card/13.png'),
    PhotoImage(file='./card/14.png'),
    PhotoImage(file='./card/15.png'),
    PhotoImage(file='./card/16.png'),
    PhotoImage(file='./card/17.png'),
    PhotoImage(file='./card/18.png'),
    PhotoImage(file='./card/19.png'),
    PhotoImage(file='./card/20.png'),
    PhotoImage(file='./card/21.png'),
    PhotoImage(file='./card/22.png'),
    PhotoImage(file='./card/23.png'),
    PhotoImage(file='./card/24.png'),
    PhotoImage(file='./card/25.png'),
    PhotoImage(file='./card/26.png'),
    PhotoImage(file='./card/27.png'),
    PhotoImage(file='./card/28.png'),
    PhotoImage(file='./card/29.png'),
    PhotoImage(file='./card/30.png'),
    PhotoImage(file='./card/31.png'),
    PhotoImage(file='./card/32.png'),
    PhotoImage(file='./card/33.png'),
    PhotoImage(file='./card/34.png'),
    PhotoImage(file='./card/35.png'),
    PhotoImage(file='./card/36.png'),
    PhotoImage(file='./card/37.png'),
    PhotoImage(file='./card/38.png'),
    PhotoImage(file='./card/39.png'),
    PhotoImage(file='./card/40.png'),
    PhotoImage(file='./card/41.png'),
    PhotoImage(file='./card/42.png'),
    PhotoImage(file='./card/43.png'),
    PhotoImage(file='./card/44.png'),
    PhotoImage(file='./card/45.png'),
    PhotoImage(file='./card/46.png'),
    PhotoImage(file='./card/47.png'),
    PhotoImage(file='./card/48.png'),
    PhotoImage(file='./card/49.png'),
    PhotoImage(file='./card/50.png'),
    PhotoImage(file='./card/51.png'),
    PhotoImage(file='./card/52.png')
  ]

  bankerCards = [
    # Label(image=cardPath[1]).grid(row=0, column=0),
    # Label(image=cardPath[2]).grid(row=0, column=1),
    # Label(image=cardPath[3]).grid(row=0, column=2),
    # Label(image=cardPath[4]).grid(row=0, column=3),
    # Label(image=cardPath[5]).grid(row=0, column=4)
  ]

  Button(blackjack, text='hit', command=hit).grid(row=2, column=0)
  Button(blackjack, text='stand', command=stand).grid(row=2, column=1)

  Label(blackjack, text='閒家1').grid(row=3, column=0)

  cardImg = PhotoImage('./card/1.png')
  photo = Label(blackjack, image=cardImg).grid(row=4, column=0)
  
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

def shuffle():
  pokerUsed = 0
  for i in range(1, 53):
    poker.append(i)

  # Shuffle
  for i in range(52):
    pokerRand = random.randint(0, 51)
    poker[i], poker[pokerRand] = poker[pokerRand], poker[i]

def hit():
  global pokerUsed, bankerPoints
  if (bankerPoints <= 21):
    nowcard = len(banker)
    banker.append(poker[pokerUsed])

    getPoker = poker[pokerUsed]

    # Label(text=checkPoker(getPoker)).grid(row=0, column=nowcard)
    # img = PhotoImage(file='./card/bg.png')

    pokerUsed += 1
    bankerPoints = calc(banker)
    # Label(text=bankerPoints).grid(row=0, column=1)
    print(bankerPoints)
  else:
    print()

def stand():
  print('stand')

def calc(pokerStack):
  print(pokerStack)
  totNum = 0

  for num in pokerStack:
    pokerNum = num % 13
    if (pokerNum == 0):
      pokerNum = 13
    
    print(pokerNum)

    if (pokerNum >= 10):
      totNum += 10
    elif (pokerNum == 1):
      if (totNum+11 > 21):
        totNum += 1
      else:
        totNum += 11
    else:
      totNum += pokerNum
    
    print(totNum)
  return totNum

def getStart():
  for i in range(2):
    hit()

def main():
  shuffle()
  # windowInit()
  getStart()

if __name__ == '__main__':
  main()
