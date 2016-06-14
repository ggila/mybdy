import pytest
import xml.etree.ElementTree as ET
import random
from datetime import datetime
import re

from activity import gpx

acti = ["gpx_file/run_garmin.gpx",
        "gpx_file/run_strava.gpx",
        "gpx_file/ride_garmin.gpx"]

acti_root = [ET.parse(a).getroot() for a in acti]
acti_read = [gpx.read(a) for a in acti]

runs = [r for r in acti if 'run' in r]
rides =[r for r in acti if 'ride' in r]

garmin_runs = [r for r in runs if 'garmin' in r]

ns = gpx._xml_namespace
garm_tf = gpx.garmin.time_format
strava_tf = gpx.strava.time_format

@pytest.fixture()
def random_xml_tree():
    gpx_f = random.choice(acti)
    return gpx_f, ET.parse(gpx_f).getroot()

@pytest.fixture()
def run_xml_tree():
    gpx_f = random.choice(runs)
    return gpx_f, ET.parse(gpx_f).getroot()

@pytest.fixture()
def garmin_run_xml_tree():
    gpx_f = random.choice(garmin_runs)
    return gpx_f, ET.parse(gpx_f).getroot()

def get_hours(xml_tree):
    gpx_f, (metadata, _) = xml_tree
    tf = garm_tf if 'garmin' in gpx_f else strava_tf
    gpx_time = gpx._readTime(metadata, tf)
    with open(gpx_f) as f:
        re_meta = re.search('<metadata>.*</metadata>', f.read(), re.DOTALL).group(0)
    re_time = re.search('<time>(.*)</time>', re_meta, re.DOTALL).group(1)
    return gpx_time, datetime.strptime(re_time, tf)

def test_hours():
    for a in acti:
        h1, h2 = get_hours((a, ET.parse(a).getroot()))
        assert h1 == h2

def test_trklen():
    for a, b in zip(acti_read, acti_root):
        len1 = a['track']['size']
        len2 = len(b[1][1])
        assert len1 == len2 == len(a['track']['lst'])

def test_version():
    for a in acti_root:
        assert a.attrib['version'] == '1.1'

def test_creator():
    for a in acti_root:
        assert a.attrib['creator'] in ['Garmin Connect', 'StravaGPX']
