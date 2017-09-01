#!/usr/bin/python2
# coding: utf-8
"""Classe que controla a Bateria"""

from dronekit import connect, Vehicle, VehicleMode
import time
import GELocationGlobal
import ControleMissao
import Sensor
import GEVehicle
import math

# Set up option parsing to get connection string
import argparse

# pA = [-27.271229, -48.681675]
# pB = [-27.496380, -48.654360]
# dlat = pB[0] - pA[0]
# dlong = pB[1] - pA[1]
# print "Distance is"
# print round(math.sqrt((dlat * dlat) + (dlong * dlong)) * 1.113195e5, 0)*0.001 #return kilometers

parser = argparse.ArgumentParser(description='Print out vehicle state information. Connects to SITL on local PC by default.')
parser.add_argument('--connect',help="vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None

# Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl

    #sitl = dronekit_sitl.start_default(-27.271229, -48.681675) #original
    sitl = dronekit_sitl.start_default(-27.588129, -48.523043) #testing
    connection_string = sitl.connection_string()

# Connect to the Vehicle.
#   Set `wait_ready=True` to ensure default attributes are populated before `connect()` returns.
print ("\nConnecting to vehicle on: %s" % connection_string)
vehicle = connect(connection_string, wait_ready=True, vehicle_class=GEVehicle.GEVehicle)
#controleMissao = ControleMissao.ControleMissao(vehicle)
#controleMissao.armAndTakeoff(vehicle)
#controleMissao.startGoToMission()
#controleMissao.startMission(vehicle)
#controleMissao.updateMission(vehicle)

print("Completed")
