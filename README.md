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
