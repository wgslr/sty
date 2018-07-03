#!/usr/bin/env python3

import yaml
import os
import datetime


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
