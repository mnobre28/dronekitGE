from dronekit import LocationGlobalRelative

class GELocationGlobal(LocationGlobalRelative):
    def __init__(self, lat, lon, alt=None):
        super(GELocationGlobal, self).__init__(lat, lon, alt)

    def getX(self):
        return self.lat

    def getY(self):
        return self.lon