#!/usr/bin/env python
# ##########################################################################
## FUNCTIONS USED BY APPLICATION LAYER TO TRIGGER C-ITS MESSAGE GENERATION
# ##########################################################################


#------------------------------------------------------------------------------------------------
# trigger_ca -trigger the generation of CA messages
#       (out) - time between ca message generation
#-------------------------------------------------------------------------------------------------
def trigger_ca(node):
	trigger_node = node # CA message - node id
	ca_user_data  = 10 # generation interval	
	return int(ca_user_data)

#------------------------------------------------------------------------------------------------
# trigger_even -trigger an event that will generate a DEN messsge
#       (out) - event message payload with: 
#						type: 'start' - event detection OU + 'stop'  - event termination 
#						rep_interval - repetition interval of the same DEN message; 0 for no repetiion
#						n_hops - maximum number of hops that the message can reach
#						(roi_x, roi_y) 
#-------------------------------------------------------------------------------------------------

def trigger_event(node, node_type, au_info, obu_info, rsu_info):
	trigger_node  = node # CA message - node id

	# Messages sent by RSU -> triggered by other events (application.py)
	if node_type == "RSU":
		event_type = input (' DEN message - Waiting for events   ')


	# Messages sent by AU
	if node_type == "AU":

		# AU -> RSU: request trip
		event_type = input (' DEN message - Request trip (y/n) >   ')
		if (event_type == 'y'):
			type = 'RSU'
			msg = {'node':node, 'sender_node_type': node_type, 'receiver_node_type': type, 'name': au_info['name'], 'num_passengers': au_info['num_passengers'], 'destination': au_info['destination']}
			return msg

	# Messages sent by OBU
	if node_type == "OBU":

		# OBU -> RSU: AU entered OBU
		event_type = input (' DEN message - AU entered (y/n) >   ')
		type = 'RSU'
		if (event_type == 'y'):
			obu_info['free'] -= 1
			msg = {'node':node, 'sender_node_type': node_type, 'receiver_node_type': type, 'name': obu_info['name'], 'capacity': obu_info['max_capacity'], 'free space': obu_info['free'], 'msg_type': 'entered'}
			return msg
		if (event_type == 'n'):
		# OBU -> RSU: AU left OBU
			event_type2 = input ('DEN message - AU left (y/n) >   ')
			if (event_type2 == 'y'):
				obu_info['free'] += 1
				msg = {'node':node, 'sender_node_type': node_type, 'receiver_node_type': type, 'name': obu_info['name'], 'capacity': obu_info['max_capacity'], 'free space': obu_info['free'], 'msg_type': 'left'}
				return msg

		


#------------------------------------------------------------------------------------------------
# position_node - retrieve nodes's position from the message
#------------------------------------------------------------------------------------------------
def position_node(msg):
	
	x=msg['pos_x']
	y=msg['pos_y']
	t=msg['time']

	return x, y, t


#------------------------------------------------------------------------------------------------
# movement_node - retrieve nodes's dynamic information from the message
#------------------------------------------------------------------------------------------------
def movement_node(msg):
	
	s=msg['speed']
	d=msg['dir']
	h=msg['heading']

	return s, d, h


