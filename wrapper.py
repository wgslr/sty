#!/usr/bin/env python3

import yaml
import os
import sys
import datetime
import argparse
import subprocess as sp

TEST_MODES = ['seqwr', 'seqrewr', 'seqrd', 'rndrd', 'rndwr', 'rndrw']
DEFAULT_MODE = 'rndrw'

DISK_TYPES = ['hdd', 'ssd', 'ram']

parser = argparse.ArgumentParser()

parser.add_argument('-o', '--output',
                    type=argparse.FileType('a'), default=sys.stdout)

# sysbench params
parser.add_argument('-s', '--file-total-size',
                    action='store', dest='total_size', required=True)
parser.add_argument('-m', '--file-test-mode',
                    action='store', dest='test_mode', choices=TEST_MODES, default=DEFAULT_MODE)
parser.add_argument('-t', '--time',
                    action='store', dest='time', default=300)

# metadata
parser.add_argument('--disk',
                    action='store', choices=DISK_TYPES, required=True)
parser.add_argument('--fs',
                    action='store', required=True)
parser.add_argument('-c', '--compression',
                    action='store', default=None)
parser.add_argument('--raid',
                    action='store', default=None)
parser.add_argument('--host',
                    action='store', default=None,
                    help='Computer performing the benchmark')


[args, passthru_args] = parser.parse_known_args()




def parse(lines):
    # strip non-yaml compatbiel
    lines = lines[22:]
    lines = [l.lower() for l in lines]
    return yaml.load('\n'.join(lines))

    
if __name__ == '__main__':
    name = 'report.txt'
    with open(name) as f:
        lines = f.readlines()
        results = parse(lines)

        timestamp = datetime.datetime.now().isoformat()

        record = {
            'timestamp': timestamp,
            'path': os.getcwd(),
            'filesystem': '',
            'compression': 'none'
        }
        record['results'] = results

        print(yaml.dump([record], default_flow_style=False))
