#!/usr/bin/env python
# #####################################################################################################
# SENDING/RECEIVING APPLICATION THREADS - add your business logic here!
## Note: you can use a single thread, if you prefer, but be carefully when dealing with concurrency.
#######################################################################################################
from socket import MsgFlag
import time
from ITS_core import update_rsu_info
from ITS_core import update_au_info
from ITS_core import update_obu_info

from application.message_handler import *
from application.self_driving_test import *
from in_vehicle_network.location_functions import position_read



# #####################################################################################################
# constants
warm_up_time = 10


#-----------------------------------------------------------------------------------------
# Thread: application transmission. In this example user triggers CA and DEN messages. 
#		CA message generation requires the sender identification and the inter-generation time.
#		DEN message generarion requires the sender identification, and all the parameters of the event.
#		Note: the sender is needed if you run multiple instances in the same system to allow the 
#             application to identify the intended recipiient of the user message.
#		TIPS: i) You may want to add more data to the messages, by adding more fields to the dictionary
# 			  ii)  user interface is useful to allow the user to control your system execution.
#-----------------------------------------------------------------------------------------
def application_txd(node, node_type, start_flag, my_system_rxd_queue, ca_service_txd_queue, den_service_txd_queue, au_info, obu_info, rsu_info):
	
	while not start_flag.isSet():
		time.sleep (1)
	print('STATUS: Ready to start - THREAD: application_txd - NODE: {}'.format(node), '\n')
	time.sleep(warm_up_time)
	
	if node_type == 'OBU':
		ca_user_data  = trigger_ca(node, obu_info)
		#print('STATUS: Message from user - THREAD: application_txd - NODE: {}'.format(node),' - MSG: {}'.format(ca_user_data),'\n')
		ca_service_txd_queue.put(ca_user_data)

	i=0
	while True:
		i=i+1
		den_user_data = trigger_event(node, node_type, au_info, obu_info, rsu_info)

		if (node_type == 'OBU'):
			obu_info = update_obu_info(obu_info, den_user_data['name'], obu_info['destination'], den_user_data['capacity'], den_user_data['free space'])

		#print('STATUS: Message from user - THREAD: application_txd - NODE: {}'.format(node),' - MSG: {}'.format(den_user_data ),'\n')
		den_service_txd_queue.put(den_user_data)
	return


#-----------------------------------------------------------------------------------------
# Thread: application reception. In this example it receives CA and DEN messages. 
# 		Incoming messages are send to the user and my_system thread, where the logic of your system must be executed
# 		CA messages have 1-hop transmission and DEN messages may have multiple hops and validity time
#		Note: current version does not support multihop and time validity. 
#		TIPS: i) if you want to add multihop, you need to change the thread structure and add 
#       		the den_service_txd_queue so that the node can relay the DEN message. 
# 				Do not forget to this also at IST_core.py
#-----------------------------------------------------------------------------------------
def application_rxd(node, node_type, start_flag, services_rxd_queue, my_system_rxd_queue, au_info, obu_info, rsu_info):
	
	while not start_flag.isSet():
		time.sleep (1)
	print('STATUS: Ready to start - THREAD: application_rxd - NODE: {}'.format(node),'\n')

	while True :
		msg_rxd=services_rxd_queue.get()
		#print('STATUS: Message received/send - THREAD: application_rxd - NODE: {}'.format(node),' - MSG: {}'.format(msg_rxd),'\n')
		if msg_rxd['node']!=node:
			my_system_rxd_queue.put(msg_rxd)

	return


#-----------------------------------------------------------------------------------------
# Thread: my_system - implements the business logic of your system. This is a very straightforward use case 
# 			to illustrate how to use cooperation to control the vehicle speed. 
# 			The assumption is that the vehicles are moving in the opposite direction, in the same lane.
#			In this case, the system receives CA messages from neigbour nodes and, 
# 			if the distance is smaller than a warning distance, it moves slower, 
# 			and the distance is smaller that the emergency distance, it stops.
#		TIPS: i) we can add DEN messages or process CAM messages in other ways. 
#			  ii) we can interact with other sensors and actuators to decid the actions to execute.
#			  iii) based on your business logic, your system may also generate events. In this case, 
# 				you need to create an event with the same structure that is used for the user and 
#               change the thread structure by adding the den_service_txd_queue so that this thread can send th DEN message. 
# 				Do not forget to this also at IST_core.py
#-----------------------------------------------------------------------------------------
def my_system(node, node_type, start_flag, coordinates, obd_2_interface, my_system_rxd_queue, den_service_txd_queue, movement_control_txd_queue, au_info, obu_info, rsu_info):

	safety_emergency_distance = 20
	safety_warning_distance = 50


	while not start_flag.isSet():
		time.sleep (1)
	print('STATUS: Ready to start - THREAD: my_system - NODE: {}'.format(node),'\n')

	au_temp = au_info
	obu_temp = obu_info
	rsu_temp = rsu_info

	if (obu_info != {}):
		obu_temp = update_obu_info(obu_temp, obu_info['name'], obu_info['destination'], obu_info['max_capacity'], obu_info['free'])


	enter_car(movement_control_txd_queue)
	turn_on_car(movement_control_txd_queue)
	car_move_forward(movement_control_txd_queue)
	
	while True :
		msg_rxd=my_system_rxd_queue.get()

		if (msg_rxd['msg_type']=='CA'):
			nodes_distance=distance (coordinates, obd_2_interface, msg_rxd)
			print ('CA --- >   nodes_ distance ', nodes_distance)

			print('-----------------------------------------')
			print('-----------------------------------------\n AU:\n', au_temp)
			print('-----------------------------------------\n OBU:\n', obu_temp)
			print('-----------------------------------------\n RSU:\n', rsu_temp)
			print('-----------------------------------------\n')
			
			obu_temp = update_obu_info(obu_temp, msg_rxd['obu_name'], msg_rxd['obu_destination'], msg_rxd['obu_capacity'], msg_rxd['obu_free'])
			rsu_temp = update_rsu_info(rsu_temp['id'], obu_temp)

			

			#if (nodes_distance < safety_emergency_distance):
			#	print ('----------------STOP-------------------')
			#	stop_car (movement_control_txd_queue)
			#	print(coordinates)
			#elif (nodes_distance < safety_warning_distance):
			#	print ('----------------SLOW DOWN  ------------------------------')
			#	car_move_slower(movement_control_txd_queue)
			#	print(coordinates)
		#if (msg_rxd == "MOVE"):
			#car_test_drive (movement_control_txd_queue)
			#print('STATUS: self-driving car - THREAD: my_system - NODE: {}'.format(node),' - MSG: {}'.format(msg_rxd),'\n')

		if msg_rxd['msg_type']=='DEN':

			# Messages received by RSU
			if node_type == 'RSU' and msg_rxd['event']['receiver_node_type'] == 'RSU':

				# AU -> RSU: request trip
				if (msg_rxd['event']['sender_node_type'] == 'AU'):

					au_temp = update_au_info(msg_rxd['event']['name'], msg_rxd['event']['destination'], msg_rxd['event']['num_passengers'])
					print('Received trip request')

					# RSU -> OBU: book seats
					type = 'OBU'
					den_user_data = {'node':node, 'sender_node_type': node_type, 'receiver_node_type': type, 'au_name': msg_rxd['event']['name'], 'destination': msg_rxd['event']['destination'], 'num_passengers': msg_rxd['event']['num_passengers'], 'msg_type': 'booking'}
					den_service_txd_queue.put(den_user_data)

				# OBU -> RSU: accepts/rejects booking
				if (msg_rxd['event']['sender_node_type'] == 'OBU' and msg_rxd['event']['msg_type'] == 'booking'):
					print('Received OBU confirmation')

					# RSU -> AU: trip confirmation
					confirmation = msg_rxd['event']['confirmation']
					type = 'AU'
					den_user_data = {'node':node, 'sender_node_type': node_type, 'receiver_node_type': type, 'obu_name': obu_temp['name'], 'confirmation': confirmation}
					den_service_txd_queue.put(den_user_data)

				# OBU -> RSU: AU entered OBU
				if (msg_rxd['event']['sender_node_type'] == 'OBU' and msg_rxd['event']['msg_type'] == 'entered'):
					print('AU entered OBU')

					# update OBU free space
					obu_temp = update_obu_info(obu_temp, obu_temp['name'], obu_temp['destination'], obu_temp['max_capacity'], msg_rxd['event']['free space'])
					rsu_temp = update_rsu_info(rsu_temp['id'], obu_temp)
					print('OBU\'s free space is now:   ')
					print(obu_temp['free'])

					# RSU -> OBU: AU entered OBU (ACK)
					type = 'OBU'
					den_user_data = {'node':node, 'sender_node_type': node_type, 'receiver_node_type': type, 'free space': obu_temp['free'], 'msg_type': 'entered'}
					den_service_txd_queue.put(den_user_data)
					
				# OBU -> RSU: AU left OBU
				if (msg_rxd['event']['sender_node_type'] == 'OBU' and msg_rxd['event']['msg_type'] == 'left'):
					print('AU left OBU')

					# update OBU free space
					obu_temp = update_obu_info(obu_temp, obu_temp['name'], obu_temp['destination'], obu_temp['max_capacity'], msg_rxd['event']['free space'])
					rsu_temp = update_rsu_info(rsu_temp['id'], obu_temp)
					print('OBU\'s free space is now:   ')
					print(obu_temp['free'])

					# RSU -> OBU: AU left OBU (ACK)
					type = 'OBU'
					den_user_data = {'node':node, 'sender_node_type': node_type, 'receiver_node_type': type, 'free space': obu_temp['free'], 'msg_type': 'left'}
					den_service_txd_queue.put(den_user_data)

			# Messages received by AU
			if node_type == 'AU' and msg_rxd['event']['receiver_node_type'] == 'AU':

				# RSU -> AU: trip confirmation
				if (msg_rxd['event']['sender_node_type'] == 'RSU'):
					print('Received trip confirmation:   ')
					if (msg_rxd['event']['confirmation'] == 'OK'):
						print('Trip confirmed successfully! :)')
					if (msg_rxd['event']['confirmation'] == 'NOT OK'):
						print('Trip canceled, no seats available or no OBU going to your destination :(')

			# Messages received by OBU
			if node_type == 'OBU' and msg_rxd['event']['receiver_node_type'] == 'OBU':

				# RSU -> OBU: book seats
				if (msg_rxd['event']['sender_node_type'] == 'RSU' and msg_rxd['event']['msg_type'] == 'booking'):
					au_temp = update_au_info(msg_rxd['event']['au_name'], msg_rxd['event']['destination'], msg_rxd['event']['num_passengers'])
					print('Received booking request')
					
					# booking NOT OK
					res = int(obu_temp['free']) - int(msg_rxd['event']['num_passengers'])
					if (obu_temp['free'] == 0 or obu_temp['destination'] != au_temp['destination'] or res < 0):
						print('Booking request NOT OK')

						# OBU -> RSU: rejects booking
						confirmation = 'NOT OK'
						type = 'RSU'
						den_user_data = {'node':node, 'sender_node_type': node_type, 'receiver_node_type': type, 'obu_name': obu_temp['name'], 'confirmation': confirmation, 'msg_type': 'booking'}
						den_service_txd_queue.put(den_user_data)
					else:
						#booking OK
						print('Booking request OK')

						# OBU -> RSU: accepts booking
						confirmation = 'OK'
						type = 'RSU'
						den_user_data = {'node':node, 'sender_node_type': node_type, 'receiver_node_type': type, 'obu_name': obu_temp['name'], 'confirmation': confirmation, 'msg_type': 'booking'}
						den_service_txd_queue.put(den_user_data)
				
				# RSU -> OBU: AU entered/left OBU (ACK)
				if (msg_rxd['event']['sender_node_type'] == 'RSU' and (msg_rxd['event']['msg_type'] == 'entered' or msg_rxd['event']['msg_type'] == 'left')):
					obu_temp = update_obu_info(obu_temp, obu_temp['name'], obu_temp['destination'], obu_temp['max_capacity'], msg_rxd['event']['free space'])
		
		if (node_type == 'OBU'):
			obu_info = update_obu_info(obu_temp, obu_temp['name'], obu_temp['destination'], obu_temp['max_capacity'], obu_temp['free'])

		if (node_type == 'AU'):
			au_info = update_au_info(au_temp['name'], au_temp['destination'], au_temp['num_passengers'])

		if (node_type == 'RSU'):
			obu_info = update_obu_info(obu_temp, obu_temp['name'], obu_temp['destination'], obu_temp['max_capacity'], obu_temp['free'])
			rsu_info = update_rsu_info(rsu_temp['id'], rsu_temp['obu'])

			if (au_info != {}):
				au_info = update_au_info(au_temp['name'], au_temp['destination'], au_temp['num_passengers'])

	return

