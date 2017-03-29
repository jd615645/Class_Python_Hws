# -*- coding: utf-8 -*-
from __future__ import print_function
from colorclass import Color, Windows
from terminaltables import SingleTable
import os, random

maxItem = 10
gameBoard = []

def getItem(num):
  item = [
    Color('{autoblack}A{/black}'),
    Color('{autored}B{/red}'),
    Color('{autogreen}C{/green}'),
    Color('{autoyellow}D{/yellow}'),
    Color('{autoblue}E{/blue}'),
    Color('{automagenta}F{/magenta}'),
    Color('{autocyan}G{/cyan}'),
    Color('{autowhite}H{/white}'),
    Color('{autobgred}{autoblack}I{/black}{/bgred}'),
    Color('{autobgred}{autored}J{/red}{/bgred}'),
    Color('{autobgred}{autogreen}K{/green}{/bgred}'),
    Color('{autobgred}{autoyellow}L{/yellow}{/bgred}'),
    Color('{autobgred}{autoblue}M{/blue}{/bgred}'),
    Color('{autobgred}{automagenta}N{/magenta}{/bgred}'),
    Color('{autobgred}{autocyan}O{/cyan}{/bgred}'),
    Color('{autobgred}{autowhite}P{/white}{/bgred}'),
    Color('{autobggreen}{autoblack}Q{/black}{/bggreen}'),
    Color('{autobggreen}{autored}R{/red}{/bggreen}'),
    Color('{autobggreen}{autogreen}S{/green}{/bggreen}'),
    Color('{autobggreen}{autoyellow}T{/yellow}{/bggreen}'),
    Color('{autobggreen}{autoblue}U{/blue}{/bggreen}'),
    Color('{autobggreen}{automagenta}V{/magenta}{/bggreen}'),
    Color('{autobggreen}{autocyan}W{/cyan}{/bggreen}'),
    Color('{autobggreen}{autowhite}X{/white}{/bggreen}'),
    Color('{autobgyellow}{autoblack}Y{/black}{/bgyellow}'),
    Color('{autobgyellow}{autored}Z{/red}{/bgyellow}')
  ]
  print(num)
  return item[int(num)]

def tableNum(num):
  return get_color_string(bcolors.WHITE, num)

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
  print('right: ', gameBoard[row][col], gameBoard[row][col-1], gameBoard[row][col-2], sep=',')
  print('down: ', gameBoard[row][col], gameBoard[row-1][col], gameBoard[row-2][col], sep=',')
  if (gameBoard[row][col] == gameBoard[row][col-1] == gameBoard[row][col-2]):
    return False
  # down
  if (gameBoard[row][col] == gameBoard[row-1][col] == gameBoard[row-2][col]):
    return False
  else:
    return True

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
          print(gameBoard[row-1][col-1])
          ary.append(getItem(gameBoard[row-1][col-1]))
    uiTable.append(ary)

  showTable = SingleTable(uiTable, 'Candy Crash')
  showTable.inner_heading_row_border = False
  showTable.inner_row_border = True
  print(showTable.table)

def main():
  global maxItem
  maxItem = input('想要幾種顏色(1-26)？')
  initTable()
  drawTable()

if __name__ == '__main__':
  main()