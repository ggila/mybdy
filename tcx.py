import xml.etree.ElementTree as ET
from datetime import datetime

class tcx(object):
    '''
        tcx file interface

        Training Center XML (TCX) is a data exchange format introduced in 2007 as part of Garmin's Training Center product. The XML is similar to GPX since it exchanges GPS tracks, but treats a track as an Activity rather than simply a series of GPS points. TCX provides standards for transferring heart rate, running cadence, bicycle cadence, calories in the detailed track. It also provides summary data in the form of laps.
        This class has read() and write() methods for reading and writing tcx file.

        See doc/tcx_format.xml for insights
    '''

    _xml_namespace = '{http://www.topografix.com/GPX/1/1}'

    class garmin(object):
        time_format = '%Y-%m-%dT%H:%M:%S.000Z'

    @staticmethod
    def read(tcx_file):
        '''return a dict describing activities'''
        # parse xml file
        tree = ET.parse(tcx_file)
        root = tree.getroot()
        origin = tcx.strava() if root.attrib['creator'] == 'StravaGPX' else tcx.garmin() # garmin and strava don't have the same format. tcx tag has an attrib creator which tell us file origin.

        #unpack xml (for now, we consider only tcx only for swim activity)
        activity, author = list(root)
        
        #get info
        time = tcx._readTime(metadata, origin.time_format)
        trk_lst = []
        for seg in trkSeg:
            trk_lst.append(tcx._readTrkSeg(seg, origin.time_format))
        
        return {'origin': origin.__class__.__name__,
                'name': trkName.text,
                'time': time,
                'track': trk_lst}

    def _readTime(meta, time_format):
        '''return datetime from metadata xml element'''
        time = meta.find('{}time'.format(tcx._xml_namespace)).text
        return datetime.strptime(time, time_format)

    def _readTrkSeg(seg, time_format):
        '''setup track points list from trkseg xml element'''
        lat, lon = float(seg.attrib['lon']), float(seg.attrib['lat'])
        alt, time, *hr = seg
        segDict = {'alt': float(alt.text),
                      'time': datetime.strptime(time.text, time_format)}
        segDict['hr'] = int(hr[0][0][0].text)    # this should be change (when new watch, just hr right now)
        return {**segDict, 'lat':lat, 'lon':lon}
