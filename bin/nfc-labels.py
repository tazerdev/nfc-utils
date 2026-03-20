#!/usr/bin/python3

import os
import csv
import sys
import signal
import argparse
from pathlib import Path

from datetime import timedelta
from datetime import datetime as dt

class TalonWAVFile:
    def __init__(self, filename, debug=False):
        self.metadata = {}
        self._filename = filename
        self._debug = debug

        self.events = []
        self._get_events()

        self._write_labels()

    def _write_labels(self):
        au_ext = '_audacity.txt'

        dest_path, filename = os.path.split(self._filename)
        filename, extension = os.path.splitext(filename)

        au_file = os.path.join(dest_path, str(filename) + au_ext)

        if self._debug:
            for e in self.events:
                print(f"{e['start']:0.2f}\t{e['stop']:0.2f}\t{e['common_name']} ({e['engine']} / {e['probability']:0.2f}%)")
        else:
            with open(au_file, 'w') as f:
                for e in self.events:
                    f.write(f"{e['start']:0.2f}\t{e['stop']:0.2f}\t{e['common_name']} ({e['engine']} / {e['probability']:0.2f}%)\n")

    def _get_events(self, force=False):
        nh_ext = '_detections.csv'
        bn_ext ='.BirdNET.selection.table.txt'

        dest_path, filename = os.path.split(self._filename)
        filename, extension = os.path.splitext(filename)

        bn_file = os.path.join(dest_path, str(filename) + bn_ext)
        nh_file = os.path.join(dest_path, str(filename) + nh_ext)

        self._get_nh_events(nh_file)
        self._get_bn_events(bn_file)

        self.events = sorted(self.events, key=lambda d: d['start'])

    def _get_nh_events(self, nh_file):
        if os.path.exists(nh_file):
            with open(nh_file) as f:
                for det in [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]:
                    try:
                        self.events.append(
                            { 
                                'filename': str(self._filename),
                                'start': float(det['start_sec']),
                                'stop': float(det['end_sec']),
                                'engine': 'nh',
                                'species_code': det['predicted_category'],
                                'common_name': det['predicted_category'],
                                'probability': float(det['prob']) * 100
                            }
                        )

                    except TypeError as e:
                        print(f"TypeError: {e}")
        else:
            if self._debug:
                print(f"Unable to locate: {nh_file}")

    def _get_bn_events(self, bn_file):
        if os.path.exists(bn_file):
            with open(bn_file) as f:
                for det in [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True, delimiter='\t')]:
                    try:
                        self.events.append(
                            {
                                'filename': str(self._filename),
                                'start': float(det['Begin Time (s)']),
                                'stop': float(det['End Time (s)']),
                                'engine': 'bn',
                                'species_code': det['Species Code'],
                                'common_name': det['Common Name'],
                                'probability': float(det['Confidence']) * 100
                            }
                        )

                    except TypeError as e:
                        print(f"TypeError: {e}")
                        print(det)
        else:
            if self._debug:
                print(f"Unable to locate: {bn_file}")

def signal_handler(signum, frame):
    signal.signal(signum, signal.SIG_IGN)
    sys.exit(0)

def ParseCommandLineArguments():
    arg_parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="tsplit is a utility for extracting one channel from a WAV file.")
    arg_parser.add_argument('-i', '--input', type=str, help="Path to the wave file to split.")
    arg_parser.add_argument('-d', '--debug', action='store_true', help='Print extra debugging information.')
    arg_parser.add_argument('-q', '--quiet', action='store_true', help="Don't display progress indicator.")

    return arg_parser

def main():
    arg_parser = ParseCommandLineArguments()
    args = arg_parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)
    file_list = []

    if args.input:
        if os.path.exists(args.input):
            file_list = [ args.input ]
        else:
            print(f"Input file does not exist.")
    else:
        file_list = list(Path(".", case_sensitive=False).glob("*.wav"))

    for f in file_list:
        TalonWAVFile(f, args.debug)


if __name__ == "__main__":
    main()
