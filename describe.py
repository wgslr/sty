#!/usr/bin/env python3

import yaml


def parse(lines):
    # strip non-yaml compatbiel
    lines = lines[22:]
    return yaml.load('\n'.join(lines))

    
if __name__ == '__main__':
    name = 'report.mod.txt'
    with open(name) as f:
        lines = [l.strip() for l in f.readlines()]
        results = parse(lines)
        print(results)
        print(yaml.dump(results, default_flow_style=False))
