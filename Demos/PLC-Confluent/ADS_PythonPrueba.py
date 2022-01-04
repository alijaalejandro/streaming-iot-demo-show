# EJEMPLO DE LECTURA Y ESCRITURA DE VARIABLES POR ADS
#https://pyads.readthedocs.io/en/latest/quickstart.html

#pip install pyads

import pyads
import time
import paho.mqtt.client as paho
from queue import Queue

# IP del CX
PLC_IP = '127.0.0.1'

# AMS NET ID de PC de Twincat I/O
PLC_AMS_ID = '192.168.2.19.1.1'
PLC_AMS_PORT = 851

# Config MQTT
broker="192.168.2.23"
port=1883

def on_publish(client,userdata,result):              #create function for callback
    #print("data published \n")
    pass
def on_message(client, userdata, message):
   q.put(message)

client1= paho.Client("PC")                           #create client object
client1.on_publish = on_publish                      #assign function to callback
client1.connect(broker,port)                         #establish connection
client1.on_message = on_message
client1.subscribe("#")
client1.loop_start()

# Inicializacion AMS
adr = pyads.AmsAddr (PLC_AMS_ID, PLC_AMS_PORT)

plc = pyads.Connection (PLC_AMS_ID, PLC_AMS_PORT, PLC_IP)
plc.open ()
print (plc.is_open)


q=Queue()
InputRegisters_old = 0
HoldingRegisters_old = 0

while True:
	# SUBIDA DE DATOS
	InputRegisters = plc.read_by_name ('MAIN.salida_pyads_InputRegisters', pyads.PLCTYPE_UINT*10)
	#print(InputRegisters)
	#HoldingRegisters = plc.read_by_name ('MAIN.salida_pyads_HoldingsRegisters', pyads.PLCTYPE_UINT*9)
	#print(HoldingRegisters)

	if InputRegisters != InputRegisters_old:
		ret= client1.publish("FSM_State_Outlet1",InputRegisters[0])
		ret= client1.publish("Power_Outlet1",InputRegisters[1])
		ret= client1.publish("Energy_Outlet1",InputRegisters[2])
		ret= client1.publish("FSM_State_Outlet2",InputRegisters[3])
		ret= client1.publish("Power_Outlet2",InputRegisters[4])
		ret= client1.publish("Energy_Outlet2",InputRegisters[5])
		ret= client1.publish("Power_Phase1_Total",InputRegisters[6])
		ret= client1.publish("Power_Phase2_Total",InputRegisters[7])
		ret= client1.publish("Power_Phase3_Total",InputRegisters[8])
		ret= client1.publish("Number_Available_CPs",InputRegisters[9])
		print("InputRegisters -> " + str(InputRegisters))
	InputRegisters_old = InputRegisters

	'''
	if HoldingRegisters != HoldingRegisters_old:
		ret= client1.publish("Power_Phase1_Max_Outlet1",HoldingRegisters[0]) 
		ret= client1.publish("Power_Phase2_Max_Outlet1",HoldingRegisters[1]) 
		ret= client1.publish("Power_Phase3_Max_Outlet1",HoldingRegisters[2]) 
		ret= client1.publish("Power_Phase1_Max_Outlet2",HoldingRegisters[3]) 
		ret= client1.publish("Power_Phase2_Max_Outlet2",HoldingRegisters[4]) 
		ret= client1.publish("Power_Phase3_Max_Outlet2",HoldingRegisters[5]) 
		ret= client1.publish("Power_Phase1_Total_Max",HoldingRegisters[6]) 
		ret= client1.publish("Power_Phase2_Total_Max",HoldingRegisters[7]) 
		ret= client1.publish("Power_Phase3_Total_Max",HoldingRegisters[8]) 
		print("HoldingRegisters -> " + str(HoldingRegisters))
	HoldingRegisters_old = HoldingRegisters
	'''

	# BAJADA DE DATOS
	while not q.empty():
	   	message = q.get()
	   	flag = 0
	   	if message is None:
	   		continue
	   	else:
		   	if message.topic == "Power_Phase1_Max_Outlet1_write":
		   		print(int(message.payload.decode("utf-8")))
		   		plc.write_by_name ('MAIN.entrada_pyads[1]',(int(message.payload.decode("utf-8"))), pyads.PLCTYPE_UINT)
		   		flag = 1
		   	if message.topic == "Power_Phase2_Max_Outlet1_write":
		   		plc.write_by_name ('MAIN.entrada_pyads[2]',(int(message.payload.decode("utf-8"))), pyads.PLCTYPE_UINT)
		   		flag = 1
		   	if message.topic == "Power_Phase3_Max_Outlet1_write":
		   		plc.write_by_name ('MAIN.entrada_pyads[3]',(int(message.payload.decode("utf-8"))), pyads.PLCTYPE_UINT)
		   		flag = 1
		   	if message.topic == "Power_Phase1_Max_Outlet2_write":
		   		plc.write_by_name ('MAIN.entrada_pyads[4]',(int(message.payload.decode("utf-8"))), pyads.PLCTYPE_UINT)
		   		flag = 1
		   	if message.topic == "Power_Phase2_Max_Outlet2_write":
		   		plc.write_by_name ('MAIN.entrada_pyads[5]',(int(message.payload.decode("utf-8"))), pyads.PLCTYPE_UINT)		
		   		flag = 1
		   	if message.topic == "Power_Phase3_Max_Outlet2_write":
		   		plc.write_by_name ('MAIN.entrada_pyads[6]',(int(message.payload.decode("utf-8"))), pyads.PLCTYPE_UINT)
		   		flag = 1
		   	if message.topic == "Power_Phase1_Total_Max_write"	:
		   		plc.write_by_name ('MAIN.entrada_pyads[7]',(int(message.payload.decode("utf-8"))), pyads.PLCTYPE_UINT)
		   		flag = 1
		   	if message.topic == "Power_Phase2_Total_Max_write"	:
		   		plc.write_by_name ('MAIN.entrada_pyads[8]',(int(message.payload.decode("utf-8"))), pyads.PLCTYPE_UINT)
		   		flag = 1
		   	if message.topic == "Power_Phase3_Total_Max_write"	:
		   		plc.write_by_name ('MAIN.entrada_pyads[9]',(int(message.payload.decode("utf-8"))), pyads.PLCTYPE_UINT)
		   		flag = 1

		   	if flag == 1:
		   		print(plc.write_by_name ('MAIN.flag_entrada_pyads',(1), pyads.PLCTYPE_BOOL))
		   		flag = 0
	   	
	time.sleep(1)