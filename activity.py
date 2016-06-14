import xml.etree.ElementTree as ET
from datetime import datetime
import ipdb

class Activities(object):
    '''Advance toolkit for sport activity analyse'''

    def __init__(self,
                name=None,
                time=None,
                track=None):
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
        from gps 1.1 doc:
            <metadata> 
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

        from gps 1.1 doc:
            <trkseg> 
                <trkpt> wptType </trkpt> [0..*] 
                <extensions> extensionsType </extensions> [0..1] 
            </trkseg>
    '''

    _xml_namespace = '{http://www.topografix.com/GPX/1/1}'

    class garmin(object):
        time_format = '%Y-%m-%dT%H:%M:%S.000Z'

    class strava(object):
        time_format = '%Y-%m-%dT%H:%M:%SZ'

    @staticmethod
    def read(gpx_file):
        '''return a dict describing activities'''
        # parse xml file
        tree = ET.parse(gpx_file)
        root = tree.getroot()
        origin = gpx.strava() if root.attrib['creator'] == 'StravaGPX' else gpx.garmin() # garmin and strava don't have the same format. gpx tag has an attrib creator which tell us file origin.

        #unpack xml (for now, we consider only gpx with one track)
        metadata, (trkName, trkSeg) = list(root)
        
        #get info
        time = gpx._readTime(metadata, origin.time_format)
        trk_lst = []
        for seg in trkSeg:
            trk_lst.append(gpx._readTrkSeg(seg, origin.time_format))

        return {'origin': origin.__class__.__name__,
                'name':trkName.text,
                'time':time,
                'track':{'size':len(trk_lst), 'lst':trk_lst}}

    def _readTime(meta, time_format):
        '''return datetime from metadata xml element'''
        time = meta.find('{}time'.format(gpx._xml_namespace)).text
        return datetime.strptime(time, time_format)

    def _readTrkSeg(trkSeg, time_format):
        '''setup track points list from trkseg xml element'''
        elevation, time, *hr = trkSeg
        trkSegDict = {'elevation': float(elevation.text),
                      'time': datetime.strptime(time.text, time_format)}
        if hr: trkSegDict['hr'] = (hr[0][0].text)
        return {**trkSegDict, **trkSeg.attrib}

class tcx(object):
    '''tcx file interface'''
    pass

class test(object):
    @classmethod
    def runRand(cls):
        run = random.choice(cls.runs)
        gpx.read(run)

    @classmethod
    def runGarmin(cls):
        run = "test/run_garmin.gpx"
        return gpx.read(run)

#test.runRand()
