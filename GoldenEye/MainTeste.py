#!/usr/bin/python2
# coding: utf-8
"""Classe que controla a Bateria"""

from dronekit import connect, Vehicle, VehicleMode
import time
import ControleVoo
import ControleMissao
import Sensor
import GEVehicle

# Set up option parsing to get connection string
import argparse

parser = argparse.ArgumentParser(description='Print out vehicle state information. Connects to SITL on local PC by default.')
parser.add_argument('--connect',help="vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None

# Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl

    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()

# Connect to the Vehicle.
#   Set `wait_ready=True` to ensure default attributes are populated before `connect()` returns.
print ("\nConnecting to vehicle on: %s" % connection_string)
vehicle = connect(connection_string, wait_ready=True, vehicle_class=GEVehicle.GEVehicle)
#cv = ControleVoo()
#cv.arm_and_takeoff(vehicle)
#vehicle.arm_and_takeoff(5)

controleMissao = ControleMissao.ControleMissao(vehicle)

print("Completed")