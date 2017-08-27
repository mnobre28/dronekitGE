#!/usr/bin/python2
# coding: utf-8
"""Classe que controla Vôo"""
from dronekit import Vehicle, VehicleMode
import time


class ControleVoo(object):
    def __init__(self):
        self._velocidade = 5 #m/s
        self._aceleracao
        self._altitude = 5
        print "controle de voo inicializado"

    def arm_and_takeoff(self, vehicle):
        """
        Arms vehicle and fly to aTargetAltitude.
        """

        print "Basic pre-arm checks"
        # Don't try to arm until autopilot is ready
        while not vehicle.is_armable:
            print " Waiting for vehicle to initialise..."
            time.sleep(1)

        print "Arming motors"
        # Copter should arm in GUIDED mode
        vehicle.mode = VehicleMode("GUIDED")
        vehicle.armed = True

        # Confirm vehicle armed before attempting to take off
        while not vehicle.armed:
            print " Waiting for arming..."
            time.sleep(1)

        print "Taking off!"
        vehicle.simple_takeoff(self._altitude)  # Take off to target altitude

        # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
        #  after Vehicle.simple_takeoff will execute immediately).
        while True:
            print " Altitude: ", vehicle.location.global_relative_frame.alt
            # Break and return from function just below target altitude.
            if vehicle.location.global_relative_frame.alt >= self._altitude * 0.95:
                print "Reached target altitude"
                break
            time.sleep(1)

            # arm and takeoff done!
