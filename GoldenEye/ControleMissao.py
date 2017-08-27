import math
import time
from dronekit import Command, CommandSequence, Vehicle, mavutil, VehicleMode, LocationGlobalRelative, LocationGlobal


class ControleMissao(object):
    def __init__(self, vehicle):
        print "Controle de Missao iniciado!"
        #temp
        self.__altitude = 10
        self.__maxMission = 9
        self.__commandSequence = vehicle.commands
        self.__commandSequence.clear()
        self.fillCommandList()
        self.uploadCommandList()


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
            if vehicle.location.global_relative_frame.alt >= self.__altitude * 0.95:
                print "Reached target altitude"
                break
            time.sleep(1)

            # arm and takeoff done!

    def fillCommandList(self):
        #Complexo Penitenciario do Estado (COPE) - Sao Pedro de Alcantara
        self.__commandSequence.add((Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                      0, 0, 0, 0, 0, 0,-27.580731, -48.753591, self.__altitude)))
        #Presidio Regional de Tijucas
        self.__commandSequence.add((Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                     0, 0, 0, 0, 0, 0,-27.271229, -48.681675, self.__altitude)))
        #Colonia Penal Agricola de Palhoca
        self.__commandSequence.add((Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                     0, 0, 0, 0, 0, 0, -27.649402, -48.696245, self.__altitude)))
        #Penitenciaria de Florianopolis
        self.__commandSequence.add((Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                     0, 0, 0, 0, 0, 0, -27.577589, -48.526740, self.__altitude)))
        #Casa do Albergado de Florianopolis
        self.__commandSequence.add((Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                     0, 0, 0, 0, 0, 0, -27.588148, -48.523054, self.__altitude)))
        #Hospital de Custodia e Tratamento Psiquiatrico (HCTP)
        self.__commandSequence.add((Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                     0, 0, 0, 0, 0, 0, -27.577930, -48.527043, self.__altitude)))
        #Presidio Regional de Biguacu
        self.__commandSequence.add((Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                     0, 0, 0, 0, 0, 0, -27.496380, -48.654360, self.__altitude)))
        #Presidio Masculino de Florianopolis
        self.__commandSequence.add((Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                     0, 0, 0, 0, 0, 0, -27.580185, -48.526691, self.__altitude)))
        #Presidio Feminino de Florianopolis
        self.__commandSequence.add((Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                     0, 0, 0, 0, 0, 0, -27.588129, -48.523043, self.__altitude)))

    def uploadCommandList(self):
        print "Enviando missoes para veiculo..."
        self.__commandSequence.upload()
        self.__commandSequence.wait_ready()
        print "Missoes enviadas com sucesso!"

    def startMission(self, vehicle):
        print "Mission started!"
        vehicle.commands.next=0
        vehicle.mode = VehicleMode("AUTO")

    def updateMission(self, vehicle):
        nextwaypoint = vehicle.commands.next
        while (nextwaypoint < self.__maxMission):
            print 'At waypoint: %s | Mission completion: %s' % (nextwaypoint, (100*nextwaypoint)/(self.__maxMission-1))
            print 'Distance to waypoint (%s): %s' % (nextwaypoint, self.distance_to_current_waypoint(vehicle))
            time.sleep(1)
        print "Mission completed successfully!"

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
        return distancetopoint

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