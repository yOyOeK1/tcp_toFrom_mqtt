#!/usr/bin/env python2

import paho.mqtt.client as paho
#import mosquitto
import time
import thread
import socket
import os, signal
import sys


tcpIp = "127.0.0.1"
tcpPort = 2000
mqttpIp = "127.0.0.1"
mqttpPort = 1883
interpreters = []

def printOut(msg):
	strtime = time.strftime("%Y%m%d_%H%M%S")
	print "#[%s] %s" % ( strtime, msg)

class interpreterObj:
	def __init__(self, name):
		self.name = name

	def printCorrectInfo(self, pName):
		printOut( "found correct siqenc [%s]" % (pName) )

	def send(self,adress,msg):
		print "[%s]	[%s]" %( adress, msg)
		mqttSend("/des/%s"%adress, msg ) 

	def doit(self,msg):
		a=0

	def parse(self, msg):
		if msg[3:6] == self.name:
			self.printCorrectInfo(self.name)
			self.doit(msg)


class interpreterMWV(interpreterObj):
	def doit(self,msg):
		v = msg.split(",")
		self.send("sensors/AppWindAngle", v[1] ) 
		self.send("sensors/AppWindSpeed", v[3] )
class interpreterDPT(interpreterObj):
	def doit(self,msg):
		v = msg.split(",")
		self.send("sensors/DepthOfWater", v[1] )
class interpreterDBT(interpreterObj):
	def doit(self,msg):
		v = msg.split(",")
		self.send("sensors/Depth", v[1] ) 
class interpreterRMC(interpreterObj):
	def doit(self,msg):
		v = msg.split(",")
		#$SDRMC,,A,1802.921,N,7810.778,W,3.20,83,,,,A*41
		self.send("sensors/GPS/lat", v[3] ) 
		self.send("sensors/GPS/lon", v[5] )
		self.send("sensors/GPS/sog", v[7] )
		self.send("sensors/GPS/cog", v[8] )
class interpreterHDM(interpreterObj):
	def doit(self,msg):
		v = msg.split(",")
		self.send("sensors/flux", v[1] ) 
class interpreterRSA(interpreterObj):
	def doit(self,msg):
		v = msg.split(",")
		self.send("sensors/rudder", v[1] ) 
class interpreterAPD(interpreterObj):
	def doit(self,msg):
		v = msg.split(",")
		self.send("autopilot/course", v[1] )
		m = ""
		if v[3] == "0":
			m = "standby"
		elif v[3] == "2":
			m = "auto"
		elif v[3] == "6":
			m = "vane"
		elif v[3] == "8":
			m = "track"
		self.send("autopilot/status", m )



interpreters.append( interpreterMWV("MWV") )
interpreters.append( interpreterDPT("DPT") )
interpreters.append( interpreterDBT("DBT") )
interpreters.append( interpreterRMC("RMC") )
interpreters.append( interpreterHDM("HDM") )
interpreters.append( interpreterRSA("RSA") )
interpreters.append( interpreterAPD("APD") )






def pmqtt_on_message(client, userdata, message):
	toTcp = []

	msg = str(message.payload.decode("utf-8"))
	toTcp.append(msg)
	printOut( "recive on mqtt /des/mqttToTcp ["+msg+"]" )

	cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	cs.connect((tcpIp, tcpPort))

	if len( toTcp )>0:
		for l in toTcp:
			printOut( "pushing to tcp %s:%s [%s]" %( tcpIp, tcpPort, l) )
			cs.send(l+"\n\r")
		toTcp = []

	cs.close()

def mqtt_on_disconnect(client, userdata, message):
	print "on disconnect !"
	print "client[%s]"%client
	print "userdata[%s]" %userdata
	print "message[%s]" %message
	os.kill(os.getpid(), signal.SIGTERM)

def mqttSend( topic, msg ):
	mqtt.publish(topic, msg)

# tcp client 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((tcpIp, tcpPort))

# mqtt client 
mqtt = paho.Client("mqttPusherToMqtt")
mqtt.connect(mqttpIp)
mqtt.on_message=pmqtt_on_message
mqtt.on_disconnect=mqtt_on_disconnect
printOut( "connected to mqtt" )
mqtt.loop_start()
mqtt.subscribe("/des/mqttToTcp")

erro = 10

while True:
	time.sleep(0.01)
	response = client.recv(4096)
	for l in ("%s"%response).splitlines():
		for p in interpreters:
			p.parse(l)
			mqttSend("/des/raw",l)			
		
	
	if len(response) == 0:
		erro-= 1
		print "response == 0 !"
		time.sleep(.5)
	else:
		erro = 10
				
	if erro < 0:
		print "connection lost to tcp server - maby :P"
		os.kill(os.getpid(), signal.SIGTERM)

print "main DONE"
