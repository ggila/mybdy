import pytest
import xml.etree.ElementTree as ET
import random

from activity import gpx

runs = ["gpx_file/run_garmin.gpx",
        "gpx_file/run_strava.gpx"]
swims = ["gpx_file/ride_garmin.gpx"]

ns = gpx._xml_namespace
garm_tf = gpx.garmin.time_format
strav_tf = gpx.strava.time_format

@pytest.fixture()
def run_xml_tree():
    gpx_f = random.choice(runs)
    return gpx_f, ET.parse(gpx_f).getroot()

def test_hours_garmin(run_xml_tree):
    gpx_f, metadata, _ = run_xml_tree
    time = gpx._readTime(metadata)
    assert time ==
