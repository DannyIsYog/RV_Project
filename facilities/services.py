#!/usr/bin/env python
# #################################################
## FUNCTIONS USED BY FACILITITES LAYER  - COMMMON SERVICES
#################################################
import time
from in_vehicle_network.car_motor_functions import *
from in_vehicle_network.location_functions import *

#------------------------------------------------------------------------------------------------
# create_CA_message - create a cooperative awareness message based on the vehicle's informatiom
#                    - node: node that generates the event
#                    - msg_id: identification of the event used to discard duplicated DEN messages received
#                    - coordinates: real-time position (x,y) at the instant (t) when the message is created
#                    - obd_2_interface: vehicle's dynamic information (speed, direction and heading).
#-------------------------------------------------------------------------------------------------

def create_ca_message(node, node_type, msg_id, coordinates, obd_2_interface, obu_info):
	
	x,y,t = position_read(coordinates)
	s,d,h = get_vehicle_info(obd_2_interface)
	name = obu_info['name']
	dest = obu_info['destination']
	cap = obu_info['max_capacity']
	free = obu_info['free']
	ca_msg= {'msg_type':'CA', 'node':node, 'node_type':node_type, 'msg_id':msg_id,'pos_x': x,'pos_y': y,'time':t,'speed': s, 'dir':d, 'heading':h, 'obu_name': name, 'obu_destination': dest, 'obu_capacity': cap, 'obu_free': free}
	return ca_msg

#------------------------------------------------------------------------------------------------
# create_DEN_message - create an event message (DEN) based on information received from application layer
#                    - node: node that generates the event
#                    - msg_id: identification of the event used to discard duplicated DEN messages received
#                    - coordinates: real-time position (x,y) at the instant (t) when the message is created
#                    - event: event information received from application layer.
#-------------------------------------------------------------------------------------------------
def create_den_message(node, msg_id, coordinates, event):
	x,y,t = position_read(coordinates)
	den_msg= {'msg_type':'DEN', 'node':node, 'msg_id':msg_id,'pos_x': x,'pos_y':y, 'time':t, 'event': event}
	return den_msg
