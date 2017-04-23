# -*- coding: utf-8 -*-
from __future__ import print_function
import socket

def connectServer():
  HOST = '127.0.0.1'
  PORT = 8001

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((HOST, PORT))
  while True:
    cmd = raw_input("Please input msg:")
    s.send(cmd)
    data = s.recv(1024)
    print(data)

      #s.close()

def init():
  print('hi')

def main():
  init()

if __name__ == '__main__':
  main()