#!/usr/bin/env python
# VARIABLES  -  shared by different threads
# coordinates - dictionary with node's location in the format (x,y,time)
# obd_2_interface - dictionary with the vehicle's dynamic in the format (speed, direction, heading)
coordinates = dict()
current_destination = dict()
obd_2_interface = dict()
obu_info = dict()  # (name, destination, max_capacity, free)
au_info = dict()  # (name, destination, number of passengers)
rsu_info = dict()  # (id, obu_list)
