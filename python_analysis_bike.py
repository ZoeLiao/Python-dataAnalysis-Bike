# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import csv
import datetime

#讀取資料
f = open(raw_input(), 'r')
x = [int(x) for x in raw_input().split()]
other_id = [] #用於儲存其他站點的站名
lat = [] #用於儲存其他站點的緯度
lon = [] #用於儲存其他站點的經度
rate = [] #用於儲存其他站車位數的資料
available_bike = [] #用於儲存其他站bike的資料
result = dict()#用於儲存符合條件的站點與距離（key:距離；value：站點）

#計算距離的公式
from math import radians, cos, sin, asin, sqrt
def haversine(lat1,lon1,lat2,lon2):
	lon1,lat1,lon2,lat2 = map(radians,[lon1,lat1,lon2,lat2])
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon/2) ** 2
	return 6367 * (2 * asin(sqrt(a)))

#處理資料的時間已與題目的格式符合
for row in csv.DictReader(f):
	row_time = str(row["time"])
	dd = datetime.datetime.strptime(row_time,"%Y/%m/%d %H:%M")#將資料中的字串轉換成時間
	date = datetime.datetime.strftime(dd,"%Y%m%d")#再將時間轉換成字串以去除「時，分」
	date_m = datetime.datetime.strftime(dd,"%H")#再將時間轉換成字串以去除「分」
	id = int(row["id"]) 
	bike = int(row["bike"])
	lot = int(row["lot"])
	latitude = float(row["latitude"])
	longtitude = float(row["longitude"])

#找出符合題目站點、日期的可租借數目、「良好狀態」車數
	if (int(date) == int(x[1])) and (int(date_m) == int(x[2])) and (int(id) == int(x[0])):
		rate_id = lot #該站點的車位數
		lat_id = latitude #該站點的緯度
		lon_id = longtitude #該站點的經度
		bike_id = bike #該站點的可租借車數
	if (int(date) == int(x[1])) and (int(date_m) == int(x[2])) and (int(id) != int(x[0])):
		other_id.append(id) #其他站點的站點名稱
		rate.append(lot) #其他站點的車位數
		lat.append(latitude) #其他站點的緯度
		lon.append(longtitude) #其他站點的經度
		available_bike.append(bike) #其他站點的可租借車數 


#如果該站符合低於「良好狀態」車數的情況：
for j in range(len(other_id)):
	if bike_id < float(rate_id * 0.2):
		if int(available_bike[j]) > float(int(rate[j]) * 0.6):
			result[haversine(lat_id,lon_id,lat[j],lon[j])] = other_id[j],available_bike[j] 
		else:
			pass		
#如果該站符合高於「良好狀態」車數的情況：
	elif bike_id > float(rate_id * 0.8):
		if int(available_bike[j]) < float(int(rate[j]) * 0.4):
			result[haversine(lat_id,lon_id,lat[j],lon[j])] = other_id[j],available_bike[j] 
		else:
			pass			
#如果該站符合「良好狀態」車數的情況：
	else:
		if (float(rate[j] * 0.2) > int(available_bike[j])) or (int(available_bike[j]) > float(int(rate[j])) * 0.8):
			result[haversine(lat_id,lon_id,lat[j],lon[j])] = other_id[j],available_bike[j] 
		else:
			pass			

#印出結果並關閉資料 
if len(result)!= 0:
	keys = result.keys()
	keys.sort()
	n = 0
	for key in keys:
		while n < 1:
			y = [str(y) for y in str(result[key]).split(",")]#將字典value形式的答案切割
			z = [str(z) for z in str(y[0]).split("(")]#去除括號
			zz = [str(zz) for zz in str(y[1]).split(")")]#去除括號
			print str(z[1])+str(zz[0])
			n += 1						

else:
	print -1
f.close()
