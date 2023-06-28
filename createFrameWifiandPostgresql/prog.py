#-*- coding: utf-8 -*-
from scapy.all import *
from threading import Thread
from multiprocessing import Process
import sys
import os
import time
import datetime
import psycopg2
import subprocess
import re
from math import pi,cos,sin
import random
arrayclient = []
arraywifi = []
#смена канала каждые 2 секунды
def change_channel():
	ch = 1
	while True:
		os.system(f"iwconfig {interface} channel {ch}")
		ch = ch % 14 + 1
		time.sleep(2)
def tril(strs):
	if len(strs) == 1:
		theta = random.uniform(0,1000)*2*pi
		resul = [strs[0][0]+cos(theta)*strs[0][2],strs[0][1]+sin(theta)*strs[0][2]]
		return resul
	if len(strs) == 2:
		strs.append(strs[1])
	os.system("rm /home/ubuntu/trilat/trilat/sample.js")
	f = open('/home/ubuntu/trilat/trilat/sample.js','w')
	str1 = "var trilat = require('./index');\n"
	str2 = "var input = [["
	f.write(str1)
	f.write(str2)
	inde1 = 0
	for indexx in strs:
		f.write(str(indexx).strip('[]'))
		if inde1 == 2:
			f.write("]];\n")
		else:
			f.write("],[")
		inde1 = inde1 + 1
	f.write("var output = trilat(input);\n")
	f.write("console.log(output);")
	f.close()
	consolestr = subprocess.run(["node", "/./trilat/trilat/sample.js"],stdout = subprocess.PIPE)
	tex = consolestr.stdout
	tex1 = str(tex)
	tex2 = re.findall(r'\d+[.]*\d*',tex1)
	resul =list(map(float,tex2))
	resul[0] = resul[0] + random.uniform(0.000010000000,0.000015000000)*random.choice([-1,1])
	resul[1] = resul[1] + random.uniform(0.000010000000,0.000015000000)*random.choice([-1,1])
	return resul

def callback_sn(packet):
	timest = datetime.datetime.now()
	wifispis = []
	global arrayclient
	global arraywifi
	dbm_signal = []
	counter = 0
	flagsearch = 0
	if packet.haslayer(Dot11Beacon) or packet.haslayer(Dot11ProbeResp):
		bssid = packet[Dot11].addr2
		try:
			ssid = packet[Dot11Elt].info.decode(encoding='utf-8')
		except:
			ssid = packet[Dot11Elt].info.decode(encoding='cp1251')
		dbm_signal.append(packet[RadioTap].dBm_AntSignal)
		bssidby = "2"
		accuracy = 1
		wifispis = [ssid,bssid,[dbm_signal],bssidby,timest,accuracy]
		for indexx in arraywifi:
			if indexx[1] == bssid:
				arraywifi[counter][2].append(dbm_signal)
				arraywifi[counter][5] = accuracy
				arraywifi[counter][4] = timest
				flagsearch = 1
				break
			counter = counter + 1
		if flagsearch == 0:
			arraywifi.append(wifispis)
	if packet.haslayer(Dot11ProbeReq):
		equal = 0
		bssid = packet[Dot11].addr2
		ssid=""
		dbm_signal.append(packet[RadioTap].dBm_AntSignal)
		bssidby = "1"
		accuracy = 0
		countercl = 0
		wifispis = [ssid,bssid,[dbm_signal],bssidby,timest,accuracy]
		for arraywifiindex in arraywifi:
			if arraywifiindex[1] == bssid:
				equal = 1
				arraywifi[counter][2].append(dbm_signal)
				arraywifi[counter][4] = timest
				break
			counter = counter + 1
		if equal == 0:
			for indexx in arrayclient:
				if indexx[1] == bssid:
					arrayclient[countercl][2].append(dbm_signal)
					arrayclient[countercl][5] = accuracy
					arrayclient[countercl][4] = timest
					flagsearch = 1
					break
				countercl = countercl + 1
			if flagsearch == 0:
				arrayclient.append(wifispis)
	if packet.haslayer(Dot11QoS) or packet[Dot11].type == 1 and packet[Dot11].subtype == 11 or packet[Dot11].type == 2 and packet[Dot11].subtype == 4:
		sour = packet[Dot11].addr2
		dest = packet[Dot11].addr1
		ssid=""
		iswifisour = 0
		iswifidest = 0
		dbm_signal.append(packet[RadioTap].dBm_AntSignal)
		counterwifi = 0
		counterclient = 0
		clienttrue = 0
		accuracy = 1
		for arraywifiindex in arraywifi:
			if arraywifiindex[1] == sour:
				iswifisour = 1
				arraywifi[counterwifi][2].append(dbm_signal)
				arraywifi[counterwifi][4] = timest
				break
			if arraywifiindex[1] == dest:
				iswifidest = 1
				break
			counterwifi = counterwifi + 1
		if iswifisour == 1:
			for arrayclientindex in arrayclient:
				if arrayclientindex[1] == dest:
					arrayclient[counterclient][3] = sour
					arrayclient[counterclient][5] = accuracy
					clienttrue = 1
					break
				counterclient = counterclient + 1
			if clienttrue == 0:
				wifispis = [ssid,dest,[dbm_signal],sour,timest,accuracy]
				arrayclient.append(wifispis)
		if iswifidest == 1:
			for arrayclientindex in arrayclient:
				if arrayclientindex[1] == sour:
					arrayclient[counterclient][2].append(dbm_signal)
					arrayclient[counterclient][3] = dest
					arrayclient[counterclient][5] = accuracy
					arrayclient[counterclient][4] = timest
					clienttrue = 1
					break
				counterclient = counterclient + 1
			if clienttrue == 0:
				wifispis = [ssid,sour,[dbm_signal],dest,timest,accuracy]
				arrayclient.append(wifispis)
		if iswifidest == 0 and iswifisour == 0:
			for arrayclientindex in arrayclient:
				if arrayclientindex[1] == sour:
					arrayclient[counterclient][2].append(dbm_signal)
					arrayclient[counterclient][4] = timest
					clienttrue = 1
					break
				counterclient = counterclient + 1
			if clienttrue == 0:
				wifispis = [ssid, sour, [dbm_signal], "1",timest, 0]
				arrayclient.append(wifispis)
if __name__ == "__main__":
	latitude = sys.argv[1]
	longitude = sys.argv[2]
	interface = "wlx00c0caa89ffc"
	printer = Thread(target=change_channel)
	printer.daemon = True
	printer.start()
	sniff(prn=callback_sn, iface=interface, timeout = 60)

	con = psycopg2.connect(
	database="wifidb",
	user="postgres",
	password="postgres",
	host="localhost",
	port="5432"
	)
	cur = con.cursor()
	for indexwifi in arraywifi:
		indexdeleteclient = 0
		for indexcliy in arrayclient:
			if indexcliy[1] == indexwifi[1]:
				arrayclient.pop(indexdeleteclient)
			indexdeleteclient = indexdeleteclient + 1
		cur.execute("SELECT bssid, countdig FROM wifimeasure;")
		dataexec = cur.fetchall()
		countdigmax = 0
		for row in dataexec:
			if row[0] == indexwifi[1]:
				if countdigmax < int(row[1]):
					countdigmax = int(row[1])
		countdigmax = countdigmax + 1
		shet = 0
		countsum = 0
		middle = 0
		for indexy in indexwifi:
			if shet == 2:
				for indexz in indexy:
					try:
						countsum = countsum + int(indexz[0])
					except:
						continue
				middle =  countsum / len(indexy)
				break
			else:
				shet = shet + 1
		if len(indexwifi[0]) < 1:
			indexwifi[0] = ""
		try:
			cur.execute("INSERT INTO wifimeasure(ssid,bssid,latitude,longitude,dbm,bssidby,countdig,datesearch,accuracy) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(indexwifi[0],indexwifi[1],latitude,longitude,middle,indexwifi[3],countdigmax,indexwifi[4],indexwifi[5]))
			con.commit()
		except:
			continue
	for indexclient in arrayclient:
		cur.execute("SELECT bssid, countdig FROM wifimeasure;")
		dataexec1 = cur.fetchall()
		countdigmax1 = 0
		for row1 in dataexec1:
			if row1[0] == indexclient[1]:
				if countdigmax1 < int(row1[1]):
					countdigmax1 = int(row1[1])
		countdigmax1 = countdigmax1 + 1
		shet1 = 0
		countsum1 = 0
		middle1 = 0
		for indexy1 in indexclient:
			if shet1 == 2:
				for indexz1 in indexy1:
					try:
						countsum1 = countsum1 + int(indexz1[0])
					except:
						continue
				middle1 =  countsum1 / len(indexy1)
				break
			else:
				shet1 = shet1 + 1
		if len(indexclient[0]) < 1:
			indexclient[0] = ""
		try:
			cur.execute("INSERT INTO wifimeasure(ssid,bssid,latitude,longitude,dbm,bssidby,countdig,datesearch,accuracy) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (indexclient[0],indexclient[1],latitude,longitude,middle1,indexclient[3],countdigmax1,indexclient[4],indexclient[5]))
			con.commit()
		except:
			continue
	cur.execute("SELECT ssid,bssid,latitude,longitude,dbm,bssidby,countdig,datesearch,accuracy FROM wifimeasure;")
	dataexec2 = cur.fetchall()
	enderswifimeasureres = []
	for indexwifimeasureres in dataexec2:
		indexend = 0
		findelem = 0
		while indexend < len(enderswifimeasureres):
			if indexwifimeasureres[1] == enderswifimeasureres[indexend][1]:
				findelem = 1
				break
			indexend = indexend + 1
		if findelem == 1:
			continue
		enderswifimeasureres.append(indexwifimeasureres)
		onebssid = []
		maxsravn = []
		maxsravnindex = []
		for sravn in dataexec2:
			if indexwifimeasureres[1] == sravn[1]:
				newwifispis=[sravn[0],sravn[1],sravn[2],sravn[3],sravn[4],sravn[5],sravn[6],sravn[7],sravn[8]]
				onebssid.append(newwifispis)
				maxsravn.append(sravn[6])
		forzapr = []
		pozitind = 0
		while pozitind < len(onebssid) and pozitind < 3:
			maxsravnindex.append(maxsravn.index(max(maxsravn)-pozitind))
			forzapr.append(onebssid[maxsravnindex[pozitind]])
			pozitind = pozitind + 1
		longlitspis = []
		if len(forzapr) == 3 and forzapr[0][2] == forzapr[1][2] and forzapr[0][3] == forzapr[1][3] and forzapr[0][2] == forzapr[2][2] and forzapr[0][3] == forzapr[2][3]:
			forzapr.pop(1)
		if len(forzapr) == 2 and forzapr[0][2] == forzapr[1][2] and forzapr[0][3] == forzapr[1][3]:
			forzapr.pop(1)
		for forzaprspis in forzapr:
			longlitspis.append([float(forzaprspis[2]),float(forzaprspis[3]),(float(forzaprspis[4])*(-1)-20)/230000])
		newspislonglit = tril(longlitspis)
		newdbforwifiuser = [forzapr[0][0],forzapr[0][1],newspislonglit[0],newspislonglit[1],forzapr[0][5],forzapr[0][6],forzapr[0][7],forzapr[0][8]]
		cur.execute("DELETE FROM wifiuser WHERE bssid = %s;",(newdbforwifiuser[1],))
		con.commit()
		cur.execute("INSERT INTO wifiuser(ssid,bssid,latitude,longitude,bssidby,countdig,datesearch,accuracy) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);",(newdbforwifiuser[0],newdbforwifiuser[1],newdbforwifiuser[2],newdbforwifiuser[3],newdbforwifiuser[4],newdbforwifiuser[5],newdbforwifiuser[6],newdbforwifiuser[7]))
		con.commit()
	cur.close()
	con.close()
