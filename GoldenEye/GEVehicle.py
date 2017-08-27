from dronekit import Vehicle, VehicleMode, Battery
import time

class GEVehicle(Vehicle):
    def __init__(self, *args):
        super(GEVehicle, self).__init__(*args)
        print("GOLDEN EYE vehicle initialized")
        battery = Battery(0, 0, 60)
        self.airspeed = 300000000 #28 m/s TEST
        #autonomia: 60 minutos de voo
        #velocidade maxima: 100 km/h
        #autonomia em velocidade maxima: 100 km

    def arm_and_takeoff(self, altitude):
        """
        Arms vehicle and fly to aTargetAltitude.
        """

        print "Basic pre-arm checks"
        # Don't try to arm until autopilot is ready
        while not self.is_armable:
            print " Waiting for vehicle to initialise..."
            time.sleep(1)

        print "Arming motors"
        # Copter should arm in GUIDED mode
        self.mode = VehicleMode("GUIDED")
        self.armed = True

        # Confirm vehicle armed before attempting to take off
        while not self.armed:
            print " Waiting for arming..."
            time.sleep(1)

        print "Taking off!"
        self.simple_takeoff(altitude)  # Take off to target altitude

        # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
        #  after Vehicle.simple_takeoff will execute immediately).
        while True:
            print " Altitude: ", self.location.global_relative_frame.alt
            # Break and return from function just below target altitude.
            if self.location.global_relative_frame.alt >= altitude * 0.95:
                print "Reached target altitude"
                break
            time.sleep(1)

            # arm and takeoff done!

    def getBattery(self):
        return Battery.level