import xml.etree.ElementTree as ET
from datetime import datetime
import random   # for test
import ipdb

class Activities(object):
    '''Advance toolkit for sport activity analyse'''

    def __init__(self,
                name=None,
                time=None,
                track=None,
                version=None,
                creator=None):
        self.name = name
        self.time = time
        self.track = track

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
        return "sport:{} track:{}".format(self.sport, self.track)

class gpx(object):
    '''
        gpx file interface

        gpx is an XML schema designed as a common GPS data format for software applications.
        This class has read() and write() methods for reading and writing gpx file.

    '''

    _xml_namespace = '{http://www.topografix.com/GPX/1/1}'
    _func = dict()

    class garmin(object):
        _xml_datetime = '%Y-%m-%dT%H:%M:%S.000Z'

    class strava(object):
        _xml_datetime= '%Y-%m-%dT%H:%M:%SZ'

    @staticmethod
    def read(gpx_file):
        '''
            from gps 1.1 doc:

            <gpx
            version="1.1 [1]"
            creator="xsd:string [1]"> 
                <metadata> metadataType </metadata> [0..1] 
                <wpt> wptType </wpt> [0..*] 
                <rte> rteType </rte> [0..*] 
                <trk> trkType </trk> [0..*] 
                <extensions> extensionsType </extensions> [0..1] 
            </gpx>
        '''
        gpx_dict = dict()
        tree = ET.parse(gpx_file)
        root = tree.getroot()
        for e in ('version', 'creator'):
            gpx_dict[e] = root.attrib[e]
        meta, trk = list(root)
        return {**gpx_dict, **gpx._readMetadata(meta), **gpx._readTrk(trk)}

    def _readMetadata(meta):
        '''
            from gps 1.1 doc:

            <...> 
                <name> xsd:string </name> [0..1] 
                <desc> xsd:string </desc> [0..1] 
                <author> personType </author> [0..1] 
                <copyright> copyrightType </copyright> [0..1] 
                <link> linkType </link> [0..*] 
                <time> xsd:dateTime </time> [0..1]
                <keywords> xsd:string </keywords> [0..1] 
                <bounds> boundsType </bounds> [0..1] 
                <extensions> extensionsType </extensions> [0..1] 
            </metadata>

            note that datetime format depends on creator
        '''
        time = meta.find('{}time'.format(gpx._xml_namespace)).text
        return {'time':datetime.strptime(time, gpx._xml_datetime_garmin)}

    def _getBaliseText(bal):
        pass

    def _getBaliseAttr(bal):
        pass

    def _readTrk(trk):
        '''
            from gps 1.1 doc:

            <trk> 
                <name> xsd:string </name> [0..1] 
                <cmt> xsd:string </cmt> [0..1] 
                <desc> xsd:string </desc> [0..1] 
                <src> xsd:string </src> [0..1] 
                <link> linkType </link> [0..*] 
                <number> xsd:nonNegativeInteger </number> [0..1] 
                <type> xsd:string </type> [0..1] 
                <extensions> extensionsType </extensions> [0..1] 
                <trkseg> trksegType </trkseg> [0..*] 
            </trk>

            <trkseg> 
                <trkpt> wptType </trkpt> [0..*] 
                <extensions> extensionsType </extensions> [0..1] 
            </trkseg>
        '''
        name, trkseg = trk

        trk_lst = []
        for seg in trkseg:
            trk_lst.append(gpx._readTrkSeg(seg))

        return {'name': name.text, 'track' :{'size': len(trk_lst), 'lst': trk_lst}}



    def _readTrkSeg(trkSeg):

        elevation, time, hr = trkSeg

        trkSegDict = {'elevation': float(elevation.text),
                        'time': datetime.strptime(time.text, gpx._xml_datetime_garmin),
                        'hr': (hr[0][0].text)}

        return {**trkSegDict, **trkSeg.attrib}



class tcx(object):
    '''tcx file interface'''
    pass

class test(object):

    runs = ["test/run_garmin.gpx",
            "test/run_strava.gpx"]

    swims = ["test/ride_garmin.gpx"]

    @classmethod
    def runRand(cls):
        run = random.choice(cls.runs)
        gpx.read(run)

    @classmethod
    def runGarmin(cls):
        run = "test/run_garmin.gpx"
        return gpx.read(run)

#test.runRand()
