# -*- coding: utf-8 -*-
from __future__ import print_function
import random
import json
import os
import socket
from Tkinter import *

poker = []
pokerUsed = 0

class Player:
  def __init__(self, cards, points, safe):
    self.id = id
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

def main():
  shuffle()
  players = []
  # creat banker
  players.append(Player([], 0, True))
  # creat player
  players.append(Player([], 0, True))

  # start game
  for player in players:
    for i in range(2):
      player.hit()
    print('player')
    print(player.cards)
    print(player.points)
  
  for i in range(len(players)):
    print('player' + str(i))
    while True:
      askHit = raw_input('hit?')
      if (askHit == 'y'):
        players[i].hit()
        print(players[i].cards)
        print(players[i].points)
      else:
        players[i].stand()
        print(players[i].cards)
        print(players[i].points)
        break
      if (not players[i].safe):
        break
      

if __name__ == '__main__':
  main()
