from dronekit import Vehicle, VehicleMode, Battery, mavutil
import time

class GEVehicle(Vehicle):
    def __init__(self, *args):
        super(GEVehicle, self).__init__(*args)
        print("GOLDEN EYE vehicle initialized")
        self.__maxBattery = 3600
        battery = Battery(0, 0, self.__maxBattery)
        self.__airspeed = 3000 #28 m/s
        #self.groundspeed = 30
        #autonomia: 60 minutos de voo
        #velocidade maxima: 100 km/h
        #autonomia em velocidade maxima: 100 km

    def getAirspeed(self):
        return self.__airspeed

    def getBattery(self):
        return Battery.level

    def consumeBattery(self, consumption = 1):
        self.battery.level = self.battery.level - consumption

    def rechargeBattery(self):
        self.__battery = Battery(0, 0, self.__maxBattery)