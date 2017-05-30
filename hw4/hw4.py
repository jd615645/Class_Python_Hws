# -*- coding:UTF-8 -*-
import csv
import sys
import pandas as pd
import math
import numpy as np
import uniout
from sklearn.metrics.pairwise import euclidean_distances
import warnings
warnings.filterwarnings('ignore')

np.seterr(divide='ignore', invalid='ignore')
airPollution = ''
sites = {}

def readData():
  global airPollution, sites

  airPollution = pd.read_csv('2015taiwan.csv')
  airPollution = airPollution[airPollution['測項'] == 'PM2.5']

  siteName = list(set().union(airPollution['測站']))

  for site in siteName:
    sites[site] = airPollution[airPollution['測站'] == site]

  for site in sites:
    for i in range(24):
      hr = str(i).zfill(2)
      sites[site][hr] = pd.to_numeric(sites[site][hr].astype(str), errors='coerce').fillna('-1').astype(int)

      noData = 0
      totPollution = 0
      for j in sites[site][hr]:
        if (j == -1):
          noData += 1
        else:
          totPollution += j
      
      avgAirPollution = format(totPollution / float(len(sites[site][hr]) - noData), '.2f')

      sites[site][hr] = pd.to_numeric(sites[site][hr].astype(str).str.replace('-1', avgAirPollution)).astype(int)

  airPollution = pd.concat(sites, ignore_index=True)

  file_name = 'output.csv'
  airPollution.to_csv(file_name, encoding='utf-8')


def knn1(siteName, date, k):
  global airPollution, sites
  rowLenght = airPollution.shape[0]
  dists = []
  needFind = sites[siteName][sites[siteName]['日期'] == date]

  for i in range(rowLenght):
    dist = euclidean_distances(needFind.iloc[0, 3:], airPollution.iloc[i, 3:])[0][0]
    dists.append(dist)

  npDist = np.array(dists)
  near = npDist.argsort()[1:k+1].tolist()
  # print(near)

  print('歐式距離')
  for i in near:
    print(airPollution.iloc[i, 0], 
          airPollution.iloc[i, 1])

def knn2(siteName, date, k):
  global airPollution, sites
  rowLenght = airPollution.shape[0]
  dists = []
  needFind = sites[siteName][sites[siteName]['日期'] == date]

  for i in range(rowLenght):
    place1 = needFind.iloc[0, 3:].tolist()
    place2 = airPollution.iloc[i, 3:].tolist()
    x = np.dot(np.array(place1), np.array(place2))
    y = squareNum(place1)
    z = squareNum(place2)

    dists.append(x / (y * z))

  npDist = np.array(dists)
  near = npDist.argsort()[1:k+1].tolist()
  # print(near)

  print('相似度')
  for i in near:
    print(airPollution.iloc[i, 0],
          airPollution.iloc[i, 1])

def squareNum(ary):
  sumNum = 0
  for i in ary:
    sumNum += i ** 2
  
  return sumNum ** 0.5

if __name__ == '__main__':
  readData()
  knn1('龍潭', '2015/01/01', 5)
  knn2('龍潭', '2015/01/01', 5)
  siteName = raw_input('請輸入地區: ')
  date = raw_input('請輸入日期(ex: 2015/01/01): ')
  k = raw_input('請輸入k值: ')
  knn1(siteName, date, k)
  knn2(siteName, date, k)
