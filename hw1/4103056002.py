# -*- coding: utf-8 -*-
from __future__ import print_function
from colorclass import Color, Windows
from terminaltables import SingleTable
import os, random, re
import curses

maxItem = 0
gameBoard = []

def getItem(num):
  if (num == ''):
    return ''
  item = [
    Color('{autoblack}A{/black}'),
    Color('{autored}B{/red}'),
    Color('{autogreen}C{/green}'),
    Color('{autoyellow}D{/yellow}'),
    Color('{autoblue}E{/blue}'),
    Color('{automagenta}F{/magenta}'),
    Color('{autocyan}G{/cyan}'),
    Color('{autobgyellow}{autoblue}H{/blue}{/bgyellow}'),
    Color('{autobgred}{autoblack}I{/black}{/bgred}'),
    Color('{autobgblue}{autowhite}J{/red}{/bgred}'),
    Color('{autobgred}{autogreen}K{/green}{/bgred}'),
    Color('{autobgred}{autoyellow}L{/yellow}{/bgred}'),
    Color('{autobgred}{autoblue}M{/blue}{/bgred}'),
    Color('{autobgred}{automagenta}N{/magenta}{/bgred}'),
    Color('{autobgred}{autocyan}O{/cyan}{/bgred}'),
    Color('{autobgred}{autowhite}P{/white}{/bgred}'),
    Color('{autobggreen}{autoblack}Q{/black}{/bggreen}'),
    Color('{autobggreen}{autored}R{/red}{/bggreen}'),
    Color('{autobgblue}{autoyellow}S{/green}{/bggreen}'),
    Color('{autobggreen}{autoyellow}T{/yellow}{/bggreen}'),
    Color('{autobggreen}{autoblue}U{/blue}{/bggreen}'),
    Color('{autobggreen}{automagenta}V{/magenta}{/bggreen}'),
    Color('{autobggreen}{autocyan}W{/cyan}{/bggreen}'),
    Color('{autobggreen}{autowhite}X{/white}{/bggreen}'),
    Color('{autobgyellow}{autoblack}Y{/black}{/bgyellow}'),
    Color('{autobgyellow}{autored}Z{/red}{/bgyellow}')
  ]
  return item[int(num)]

def initTable():
  for row in range(10):
    ary = []
    for col in range(10):
      ary.append('')
    gameBoard.append(ary)
  
  for row in range(10):
    for col in range(10):
      while True:
        gameBoard[row][col] = random.randint(0, maxItem-1)
        if (not checkLine(row, col)):
          break
    
def checkLine(row, col):
  # right
  if(gameBoard[row][col-1] != ''):
    if (gameBoard[row][col] == gameBoard[row][col-1] == gameBoard[row][col-2]):
      return True
  # down
  if(gameBoard[row-1][col] != ''):
    if (gameBoard[row][col] == gameBoard[row-1][col] == gameBoard[row-2][col]):
      return True
  return False

def checkHaveLine():
  needremove = []
  # find col
  for row in range(10):
    repect = 0
    keyItem = gameBoard[row][0]
    for col in range(1, 10):
      if (gameBoard[row][col] == keyItem):
        repect += 1
        if (repect == 2):
          for i in range(3):
            needremove.append([row, col-i])
        elif (repect > 2):
          needremove.append([row, col])
      else:
        repect = 0
        keyItem = gameBoard[row][col]
  # find row
  for col in range(10):
    repect = 0
    keyItem = gameBoard[0][col]
    for row in range(1, 10):
      if (gameBoard[row][col] == keyItem):
        repect += 1
        if (repect == 2):
          for i in range(3):
            needremove.append([row-i, col])
        elif (repect > 2):
          needremove.append([row, col])
      else:
        repect = 0
        keyItem = gameBoard[row][col]
    
  if (len(needremove) != 0):
    return needremove
  else:
    return False


def drawTable():
  uiTable = []

  for row in range(11):
    ary = []
    for col in range(11):
      if (row == 0 or row == 10):
        if (col == 0 or col == 10):
          ary.append('')
        else:
          ary.append(col)
      else:
        if (col == 0 or col == 10):
          ary.append(row)
        else:
          ary.append(getItem(gameBoard[row-1][col-1]))
    uiTable.append(ary)

  showTable = SingleTable(uiTable, 'Candy Crash')
  showTable.inner_heading_row_border = False
  showTable.inner_row_border = True
  print(showTable.table)

def inputCoordinate():
  keyin = raw_input('請輸入座標(ex: 4,5): ')
  check = re.search('^\d,\d$', keyin)

  if (check):
    coordinate = check.group().split(',')
    row = int(coordinate[0])
    col = int(coordinate[1])
    if (row<1 or row>maxItem-1 or col<1 or col>maxItem-1 ):
      return False
    else:
      return [row, col]
  else:
    return False
    
def inputmove(coordinate):
  keyin = raw_input('請輸入移動方向(ex: w or a or s or d): ')
  check = re.search('^[wasd]$', keyin)

  row = coordinate[0]
  col = coordinate[1]
  if(check):
    if (keyin == 'w'):
      if (coordinate[0] > 1):
        return keyin
    elif (keyin == 'a'):
      if (coordinate[1] > 1):
        return keyin
    elif (keyin == 's'):
      if (coordinate[0] < 9):
        return keyin
    elif (keyin == 'd'):
      if (coordinate[1] < 9):
        return keyin
    return False
  else:
    return False

def moveCoordinate(coordinate, move):
  row = coordinate[0]
  col = coordinate[1]
  if (move == 'w'):
    return [row-1, col]
  elif (move == 'a'):
    return [row, col-1]
  elif (move == 's'):
    return [row+1, col]
  elif (move == 'd'):
    return [row, col+1]

def errorKeyin():
  msg = [u'請照格式輸入']
  showTable = SingleTable(msg)
  print(showTable.table)

def removeItem(needRemove):
  point = 0
  for i in needRemove:
    row = i[0]
    col = i[1]
    if (gameBoard[row][col] != ''):
      gameBoard[row][col] = ''
      point += 1
  return point

def showPoint(points, rounds):
  show = [
    ['Points', points],
    ['Last Round', rounds]
  ]
  showTable = SingleTable(show)
  print(showTable.table)

def dropDown():
  for col in range(10):
    for row in range(9, -1, -1):
      while True:
        if (gameBoard[row][col] == ''):
          for dropRow in range(row, 0, -1):
            gameBoard[dropRow][col] = gameBoard[dropRow-1][col]
          gameBoard[0][col] = random.randint(0, maxItem-1)
        else:
          break

def swap(coordinate, moveToCoordinate):
  row_1 = coordinate[0]-1
  col_1 = coordinate[1]-1
  row_2 = moveToCoordinate[0]-1
  col_2 = moveToCoordinate[1]-1

  gameBoard[row_1][col_1], gameBoard[row_2][col_2] = gameBoard[row_2][col_2], gameBoard[row_1][col_1]

def main():
  global maxItem 
  maxItem = input('想要幾種顏色(3-26)？')
  rounds = 20
  points = 0
  initTable()

  haveError = False



  while (rounds>0):
    drawTable()
    showPoint(points, rounds)
    if (haveError):
      haveError = False
      errorKeyin()
    
    coordinate = inputCoordinate()
    if (not coordinate):
      haveError = True
      continue

    move = inputmove(coordinate)
    if (not move):
      haveError = True
      continue
    
    moveTo = moveCoordinate(coordinate, move)

    swap(coordinate, moveTo)
    drawTable()
    haveLine = checkHaveLine()

    if (haveLine):
      points += removeItem(haveLine)
      dropDown()
      check = checkHaveLine()
      while (check):
        points += removeItem(check)
        dropDown()
        check = checkHaveLine()
      rounds -= 1
    else:
      swap(coordinate, moveTo)


if __name__ == '__main__':
  main()