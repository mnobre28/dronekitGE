import math
import GELocationGlobal
import time
from dronekit import Command, CommandSequence, Vehicle, mavutil, VehicleMode, LocationGlobalRelative, LocationGlobal, mavlink


class ControleMissao(object):
    def __init__(self, vehicle):
        print "Mission control started!"
        #temp
        self.__vehicle = vehicle
        self.__altitude = 10
        self.__waypointList = self.startWaypointList()
        self.__maxMissions = 8
        self.__commandSequence = vehicle.commands #deprecated
        self.__commandSequence.clear()            #deprecated
        self.fillCommandList()                    #deprecated
        self.uploadCommandList()                  #deprecated

    def armAndTakeoff(self, vehicle):
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
        #vehicle.parameters['WPNAV_SPEED'] = vehicle.getGESpeed()

        # Confirm vehicle armed before attempting to take off
        while not vehicle.armed:
            print " Waiting for arming..."
            time.sleep(1)

        print "Taking off!"
        vehicle.simple_takeoff(self.__altitude)  # Take off to target altitude
        # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
        #  after Vehicle.simple_takeoff will execute immediately).
        while True:
            #print " Altitude: ", vehicle.location.global_relative_frame.alt
            # Break and return from function just below target altitude.
            print "Going up!"
            if vehicle.location.global_relative_frame.alt >= self.__altitude * 0.95:
                print "Reached target altitude"
                break
            else:
                vehicle.consumeBattery()
            time.sleep(1)

            # arm and takeoff done!
    #======================================
    def startWaypointList(self):
        waypointList = []
        waypointList.append(GELocationGlobal.GELocationGlobal(-27.271229, -48.681675, self.__altitude))
        waypointList.append(GELocationGlobal.GELocationGlobal(-27.496380, -48.654360, self.__altitude))
        waypointList.append(GELocationGlobal.GELocationGlobal(-27.580731, -48.753591, self.__altitude))
        waypointList.append(GELocationGlobal.GELocationGlobal(-27.649402, -48.696245, self.__altitude))
        waypointList.append(GELocationGlobal.GELocationGlobal(-27.588148, -48.523054, self.__altitude))
        waypointList.append(GELocationGlobal.GELocationGlobal(-27.580185, -48.526691, self.__altitude))
        waypointList.append(GELocationGlobal.GELocationGlobal(-27.577930, -48.527043, self.__altitude))
        waypointList.append(GELocationGlobal.GELocationGlobal(-27.588129, -48.523043, self.__altitude))
        waypointList.append(GELocationGlobal.GELocationGlobal(-27.577589, -48.526740, self.__altitude))
        return waypointList

    def startGoToMission(self):
        print "Starting goto operation!"
        #self.goToWaypoint(0) is the initial position
        print "Going to waypoint 1..."
        self.goToWaypoint(1)

    def goToWaypoint(self, currentWaypoint):
        location = self.__waypointList[currentWaypoint]
        timer = 0
        distance = self.getDistanceKilometers(self.__waypointList[currentWaypoint-1], location)
        while (distance > 1):
            self.__vehicle.simple_goto(location, self.__vehicle.getAirspeed(), 0)
            while (timer < 30):
                print 'At waypoint: %s | Mission completion: %s/%s' % (currentWaypoint, currentWaypoint, self.__waypointList.__len__())
                print 'Distance to waypoint (%s): %s (km)' % (currentWaypoint, self.getDistanceKilometers(self.__waypointList[currentWaypoint-1], location))
                #time.sleep(1)
                timer = timer + 1
                if (distance <= 1):
                    break
                time.sleep(30)
            timer = 0
        print "Waypoint reached"
    #======================================

    def fillCommandList(self):
        #self.__commandSequence.add((Command(0, 0, 0, mavutil.mavlink.MAV_cmd_go
        # 1 Presidio Regional de Tijucas
        #self.__commandSequence.add((Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
         #            0, 0, 0, 0, 0, 0, -27.271229, -48.681675, self.__altitude)))
        #2 Presidio Regional de Biguacu
        self.__commandSequence.add((Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                     0, 0, 0, 0, 0, 0, -27.496380, -48.654360, self.__altitude)))
        #3 Complexo Penitenciario do Estado (COPE) - Sao Pedro de Alcantara
        self.__commandSequence.add((Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                      0, 0, 0, 0, 0, 0,-27.580731, -48.753591, self.__altitude)))
        #4 Colonia Penal Agricola de Palhoca
        self.__commandSequence.add((Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                     0, 0, 0, 0, 0, 0, -27.649402, -48.696245, self.__altitude)))
        #5 Casa do Albergado de Florianopolis
        self.__commandSequence.add((Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                     0, 0, 0, 0, 0, 0, -27.588148, -48.523054, self.__altitude)))
        # 6 Presidio Masculino de Florianopolis
        self.__commandSequence.add((Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                     0, 0, 0, 0, 0, 0, -27.580185, -48.526691, self.__altitude)))
        #7 Hospital de Custodia e Tratamento Psiquiatrico (HCTP)
        self.__commandSequence.add((Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                     0, 0, 0, 0, 0, 0, -27.577930, -48.527043, self.__altitude)))
        #8 Presidio Feminino de Florianopolis
        self.__commandSequence.add((Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                     0, 0, 0, 0, 0, 0, -27.588129, -48.523043, self.__altitude)))
        #9 Penitenciaria de Florianopolis
        self.__commandSequence.add((Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                     0, 0, 0, 0, 0, 0, -27.577589, -48.526740, self.__altitude)))

    def uploadCommandList(self):
        print "Sending coordinates to vehicle..."
        self.__commandSequence.upload()
        self.__commandSequence.wait_ready()
        print "Coordinates uploaded successfully!"

    def startMission(self, vehicle):
        print "Mission started!"
        #print vehicle.location.global_frame
        vehicle.commands.next=0
        vehicle.mode = VehicleMode("AUTO")

    def updateMission(self, vehicle):
        while (self.__commandSequence.count > 0):
            nextwaypoint = vehicle.commands.next
            print 'At waypoint: %s | Mission completion: %s/%s' % (nextwaypoint, self.__commandSequence.count, self.__maxMissions)
            print 'Distance to waypoint (%s): %s (km)' % (nextwaypoint, self.distance_to_current_waypoint(vehicle))
            vehicle.consumeBattery()
            time.sleep(1)
            nextwaypoint = vehicle.commands.next
        print "Mission completed successfully!"

    def messageMissionCompleted(self, waypointTracker, vehicle):
        if waypointTracker > 0:
            print 'Arrived at waypoint %s' % (waypointTracker)
            vehicle.rechargeBattery
            print "Refueling..."
            print "Ready to go!"
    #copied
    def distance_to_current_waypoint(self, vehicle):
        """
        Gets distance in metres to the current waypoint.
        It returns None for the first waypoint (Home location).
        """
        nextwaypoint = vehicle.commands.next
        if nextwaypoint == 0:
            return None
        missionitem = vehicle.commands[nextwaypoint - 1]  # commands are zero indexed
        lat = missionitem.x
        lon = missionitem.y
        alt = missionitem.z
        targetWaypointLocation = LocationGlobalRelative(lat, lon, 30)
        distancetopoint = self.get_distance_metres(vehicle.location.global_frame, targetWaypointLocation)
        return round(distancetopoint*0.001, 3)

    def getDistanceKilometers(self, pointA, poinB):
        dlat = poinB.lat - pointA.lat
        dlong = poinB.lon - pointA.lon
        distance = math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5
        return round(distance*0.001, 2)

    #copied
    def get_distance_metres(self, aLocation1, aLocation2):
        """
        Returns the ground distance in metres between two LocationGlobal objects.

        This method is an approximation, and will not be accurate over large distances and close to the
        earth's poles. It comes from the ArduPilot test code:
        https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
        """
        dlat = aLocation2.lat - aLocation1.lat
        dlong = aLocation2.lon - aLocation1.lon
        return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5