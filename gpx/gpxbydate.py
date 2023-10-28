#!/usr/bin/env python3
#
# GPX file separator by local date
#
# gpxbydate <gpx-file> [<gpx-files>...]
import sys
import gpxpy
from datetime import datetime, timezone

def showhow():
    print("gpbydate <gpx-file> [<gpx-file>...]")
    sys.exit(1)

def gpxbydate_main():
    arg_files = sys.argv[1:]
    print(f"arg_files:{arg_files}")
    parse_a_gpx(arg_files[0])

def parse_a_gpx(fname:str):
    date_dir = {}
    with open(fname, 'r') as file:
        gpx = gpxpy.parse(file.read())

        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    print('Point at ({}, {}) -> {}'.format(point.latitude, point.longitude, point.elevation))
                    the_time = point.time
                    x = the_time.astimezone().strftime('%Y-%m-%d')
                    if not(x in date_dir):
                        date_dir[x] = []
                    date_dir[x].append(point)
    
    for k in date_dir.keys():
        print(date_dir[k][0])

if __name__ == '__main__':
    gpxbydate_main()
    sys.exit(0)


