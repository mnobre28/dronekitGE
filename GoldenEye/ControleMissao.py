import math
import time
from dronekit import Command, CommandSequence, Vehicle, mavutil

class ControleMissao(object):
    def __init__(self, vehicle):
        print "Controle de Missao iniciado!"
        #temp
        self.__altitude = 30
        self.__commandSequence = vehicle.commands
        self.__commandSequence.clear()
        self.__missionList = []
        self.fillMissionList()
        self.uploadMissionList()



    def fillMissionList(self):
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

    def uploadMissionList(self):
        print "Enviando missoes para veiculo..."
        self.__commandSequence.upload()
        print "Missoes enviadas com sucesso!"


#copied
    def get_distance_metres(aLocation1, aLocation2):
        """
        Returns the ground distance in metres between two LocationGlobal objects.

        This method is an approximation, and will not be accurate over large distances and close to the
        earth's poles. It comes from the ArduPilot test code:
        https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
        """
        dlat = aLocation2.lat - aLocation1.lat
        dlong = aLocation2.lon - aLocation1.lon
        return math.sqrt((dlat * dlat) + (dlong * dlong)) * 1.113195e5