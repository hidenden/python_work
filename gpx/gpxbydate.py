#!/usr/bin/env python3
#
# GPX file separator by local date
#
# gpxbydate <gpx-file> [<gpx-files>...]
import sys
import gpxpy
import gpxpy.gpx
from datetime import datetime, timezone
import argparse
import os

def valid_dir(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"Directory {path} does not exist.")

def gpxbydate_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prefix", help='prefix for output gpx files.', default="out_")
    parser.add_argument("-d", "--dir", help='output directory.', default=".", type=valid_dir)
    parser.add_argument("gpxfiles", help='input gpx files', nargs="+")
    args = parser.parse_args()

    point_dir = {}
    for arg_file in args.gpxfiles:
        parse_a_gpx(arg_file, point_dir)

    out_gpxfiles(point_dir, args.dir, args.prefix)

def out_gpxfiles(pdir:dict[str, list], savedir:str, prefix:str):
    for date_str in pdir.keys():
        out_a_gpxfile(date_str, pdir[date_str], savedir, prefix)

def out_a_gpxfile(date_str:str, points:list, savedir:str, prefix:str):
    # Create a new GPX file
    gpx = gpxpy.gpx.GPX()

    # Create track in GPX
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx_track.name = date_str
    gpx.tracks.append(gpx_track)

    # Create segment in the GPX track
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    # Sort the points
    points.sort(key=lambda x: x.time)

    # Set all points
    for p in points:
        gpx_segment.points.append(p)

    new_file_name = f"{savedir}/{prefix}{date_str}.gpx"
    print(f"new file:{new_file_name}")
    with open(new_file_name, "w", encoding="utf-8") as file:
        file.write(gpx.to_xml())


def parse_a_gpx(fname:str, point_dir:dict[str, list]):
    with open(fname, 'r') as file:
        gpx = gpxpy.parse(file.read())

        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    x = point.time.astimezone().strftime('%Y-%m-%d')
                    if not(x in point_dir):
                        point_dir[x] = []
                    point_dir[x].append(point)
    

if __name__ == '__main__':
    gpxbydate_main()
    sys.exit(0)


