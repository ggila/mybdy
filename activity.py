import xml.etree.ElementTree as ET

class Activities(object):
    '''Advance toolkit for sport activity analyse'''

    def __init__(self, sport=None, track=None):
        self.sport = sport
        self.track = track

    @classmethod
    def from_gpx(cls, gpx_file=''):
        activity_data = gpx.read(gpx_file)
        return cls(**activity_data)

    @classmethod
    def from_tcx(cls, tcx_file=''):
        pass

#    @property
#    def track(self):
#        return self._track

#    @track.setter
#    def track(self, value):
#        pass

    def __str__(self):
        return "sport:{} track:{}".format(self.sport, self.track)

class gpx(object):
    '''gpx file interface'''

    @staticmethod
    def read(gpx_file):
        tree = ET.parse(gpx_file)
        root = tree.getroot()
        metadata, trk = list(root)
        return {**self._readMetadata(metadata), **self._readTrk(trk)}

class tcx(object):
    '''tcx file interface'''
    pass

def test():

    f = ["run_garmin.gpx",
            "run_strava.gpx",
            "ride_garmin.gpx"]

    for t in f: 
