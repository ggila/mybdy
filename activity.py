from datetime import datetime
from collections import namedtuple, defaultdict
from geopy import distance

from gpx import gpx

Point = namedtuple('Point', ['lon', 'lat', 'alt'])

class Activities(object):
    '''Advance toolkit for sport activity analyse'''

    def __init__(self,
                origin='manual',
                name='New',
                time=None,
                track=None):
        self.name = name
        self.origin = origin
        self.time = time
        if track:
            self.track = Track(track)
            self.point = [Point(a['lon'], a['lat'], a['alt']) for a in track['lst']]
            self.progression = [a['time'] - time for a in track['lst']]

    @staticmethod
    def from_gpx(gpx_file=''):
        activity_data = gpx.read(gpx_file)
        return Activities(**activity_data)

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
        return "Activities({}, {})".format(self.name, self.time.strftime('%d-%m-%Y %H:%M'))

class Track(object):
    '''Contains and compute info about segmented data'''

    def __init__(self, trkList):
        init = defaultdict(list, [])
        for d in trkList:
            init['Point'].append(Point(trkList.pop('lon'), trkList.pop('lat'), trkList.pop('alt')))
            for k, v in d.items():
                init[k].append(v)
        for k, v in init.items():
             self.k = v
        

class tcx(object):
    '''tcx file interface'''
    pass
