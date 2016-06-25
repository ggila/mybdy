from datetime import datetime
from collections import namedtuple, defaultdict
from functools import reduce

from geopy import distance

from gpx import gpx
from tcx import tcx

Point = namedtuple('Point', ['lon', 'lat', 'alt'])

class Activity(object):
    '''
        Advance toolkit for sport activity analyse
    
        Activity can be:
            - load from gpx or tcx file
            - be build from scratch
    '''

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
#            self.point = [Point(a['lon'], a['lat'], a['alt']) for a in track['lst']]
#            self.progression = [a['time'] - time for a in track['lst']]

    @staticmethod
    def from_gpx(gpx_file=''):
        activity_data = gpx.read(gpx_file)
        return Activity(**activity_data)

    @staticmethod
    def to_gpx(gpx_file=''):
        pass

    @classmethod
    def from_tcx(cls, tcx_file=''):
        activity_data = tcx.read(gpx_file)
        return Activity(**activity_data)

    @staticmethod
    def to_tcx(tcx_file=''):
        pass

    def __repr__(self):
        pass

    def setTime(self, date):
        self.time = date

    def setDuration(self, delta):
        self.track.setDuration(delta)
#    @property
#    def track(self):
#        return self._track

#    @track.setter
#    def track(self, value):
#        pass

    def __str__(self):
        return "Activity({}, {})".format(self.name, self.time.strftime('%d-%m-%Y %H:%M'))

class Track(object):
    '''Contains and compute info about segmented data'''

    def __init__(self, trkList):
        self.length = len(trkList)

        # For keeping tracks of field info
        self.field = ['point']
        for k in trkList[0]:
            if k not in ['lat', 'lon', 'alt']: self.field.append(k)

        # Set up list od data
        init = defaultdict(list, [])
        for d in trkList:
            init['point'].append(Point(d.pop('lon'), d.pop('lat'), d.pop('alt')))
            for k, v in d.items():
                init[k].append(v)

        self.point = init['point']
        for k, v in init.items():
            setattr(self, k, v)

    def __repr__(self):
        pass

    def __getitem__(self, position):
        d = dict()
        for f in self.field:
            d[f] = getattr(self, f)[position]
        return d

    def setDuration(self, delta):
        self.time = [i/(self.length - 1) * delta for i in range(self.length)]
