# tcp_toFrom_mqtt tcp multiplexer no mqtt
Small multiplexer in python to connect tcp and mqtt. It transfer nmea commands from tcp server running on kplex and translating it to topics on mosquitto / mqtt server.
All so subscribe to topic and transmit data to tcp server runing on kplex.

plugin orientated code :P
easy to add new parser,
now known variables and translations:

$**MWV
$**DPT
$**DBT
$**RMC
$**HDM
$**RSA
$**APD,[int]heading,M,[a,s,v,t]mode,S*ff  - extra


configurable !
have fun.


Hardware: 
My setup from scraps :)
old autohelp 5000+ as a voltage level buffer uart 5v on arduino seatalk ~13v
arduino nano connected to IC on autohelm 5000+ to get data in UART console
  9bit read/write to seatalk bus
orangepizero main brain of operation running armbian on it mqtt broaker, kplex, 
  tcp_toFrom_mqtt, http server
power supply usb car charger
aditional capacitors :P


![Screenshot](hardware.jpg)
