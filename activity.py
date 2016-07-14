from datetime import datetime
from collections import namedtuple, defaultdict
from functools import reduce

from geopy.distance import vincenty

from gpx import gpx
from tcx import tcx

Point = namedtuple('Point', ['lat', 'lon', 'alt'])

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

    def to_gpx(self, gpx_file=''):
        if gpx_file == '':
            if self.name: gpx_file = "{}.gpx".format(self.name)
            elif self.time: gpx_file = "{}.gpx".format(self.time.strftime('%d-%m-%Y_%H:%M'))
            else:
                timestr = time.strftime("%d/%m/%Y_%H:%M/%S", time.localtime())
                gpx_file = "Activity_{}.gpx".format(timestr)
        gpx.write(self, gpx_file)

    @classmethod
    def from_tcx(cls, tcx_file=''):
        activity_data = tcx.read(gpx_file)
        return Activity(**activity_data)

    @staticmethod
    def to_tcx(tcx_file=''):
        pass

    def __repr__(self):
        return "Activity({}, {})".format(self.name, self.time.strftime('%d-%m-%Y %H:%M'))

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

class Track(object):
    '''Contains and compute info about segmented data'''

    def __init__(self, trkList):
        self.length = len(trkList)

        # Keeping tracks of suscriptable field
        self.field = ['point', 'dist']
#        self.field = ['point', 'dist', 'speed']
        for k in trkList[0]:            #specific field
            if k not in ['lat', 'lon', 'alt']: self.field.append(k)

        # Set up list of data
        init = defaultdict(list, [])
        for d in trkList:
            init['point'].append(Point(d.pop('lat'), d.pop('lon'), d.pop('alt')))
            init['dist'].append(0 if len(init['point']) == 1 else vincenty(init['point'][-1], init['point'][-2]).km)
#            print(init['dist'])
            for k, v in d.items():
                init[k].append(v)

        self.point = init['point']
        for k, v in init.items():
            setattr(self, k, v)

        self.Dist = sum(init['dist'])

    def __repr__(self):
        pass

    def __getitem__(self, position):
        d = dict()
        for f in self.field:
            d[f] = getattr(self, f)[position]
        return d

    def setDuration(self, delta):
        self.time, sum_dist = [], 0
        for i in range(self.length):
            sum_dist += self.dist[i]
            self.time.append(sum_dist/self.Dist * delta)
