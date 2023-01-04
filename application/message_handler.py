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

	if node_type == "RSU":
		event_type = input (' DEN message - djfhskladsfd >   ')
		type = 'AU'
		msg = {'node':node, 'sender_node_type': node_type, 'receiver_node_type': type, 'id': rsu_info['id']}

		return msg


		
	#	event_type = input (' DEN message - Event type >   ')
	#	event_status = input (' DEN message - Event status (start | update | stop) >   ')
	#	event_id = input (' DEN message - Event identifier >   ')
	#	if event_status == 'start':
	#		rep_interval = input (' DEN message - repetition interval (0 if single event) >   ')
	#		n_hops = input (' DEN message - Maximum hop number >   ')
	#		roi_x  = input (' DEN message - ROI x coordinates (0 if none)>   ')
	#		roi_y  = input (' DEN message - ROI y coordinates (0 if none) >   ')
	#		latency = input (' DEN message - maximum latency >   ')
	#	event_msg={'event_type':event_type, 'event_status': event_status, 'event_id': int(event_id), 'rep_interval':int(rep_interval), 'n_hops': int(n_hops), 'roi_x':int(roi_x), 'roi_y': int(roi_y), 'latency':int(latency)}
	#	return event_msg
	
	if node_type == "AU":

		event_type = input (' DEN message - Request trip (y/n) >   ')
		if (event_type == 'n'):
			return
		type = 'RSU'
		msg = {'node':node, 'sender_node_type': node_type, 'receiver_node_type': type, 'name': au_info['name'], 'num_passengers': au_info['num_passengers'], 'destination': au_info['destination']}
		return msg

	if node_type == "OBU":
		event_type = input (' DEN message - coisa >   ')
		type = 'RSU'
		msg = {'node':node, 'sender_node_type': node_type, 'receiver_node_type': type, 'name': obu_info['name'], 'capacity': obu_info['max_capacity'], 'free space': obu_info['free']}
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


