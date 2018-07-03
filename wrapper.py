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
parser.add_argument('-n', '--file-num',
                    action='store', type=int, dest='file_num', default=128)
parser.add_argument('-m', '--file-test-mode',
                    action='store', dest='test_mode', choices=TEST_MODES, default=DEFAULT_MODE)
parser.add_argument('-t', '--time',
                    action='store', type=int, dest='time', default=300)

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

print(args)
print(passthru_args)

def make_sysbench_args():
    result = passthru_args
    result.append('--file-total-size={}'.format(args.total_size))
    result.append('--file-test-mode={}'.format(args.test_mode))
    result.append('--time={}'.format(args.time))
    result.append('--file-num={}'.format(args.file_num))
    return result


def parse(lines):
    # strip non-yaml compatbiel
    lines = lines[22:]
    lines = [l.lower() for l in lines]
    return yaml.load('\n'.join(lines))


def run(bench_args):
    print("Running ", ['sysbench', 'fileio', 'prepare'] + bench_args)
    o1 = sp.check_output(['sysbench', 'fileio', 'prepare'] + bench_args, encoding='utf8')
    print(o1)
    o2 = sp.check_output(['sysbench', 'fileio', 'run'] + bench_args, encoding='utf8')
    print(o2)
    o3 = sp.check_output(['sysbench', 'fileio', 'cleanup'] + bench_args, encoding='utf8')
    print(o3)




if __name__ == '__main__':
    bench_args = make_sysbench_args()
    run(bench_args)



    # name = 'report.txt'
    # with open(name) as f:
    #     lines = f.readlines()
    #     results = parse(lines)

    #     timestamp = datetime.datetime.now().isoformat()

    #     # TODO test mode and time

    #     record = {
    #         'timestamp': timestamp,
    #         'path': os.getcwd(),
    #         'filesystem': '',
    #         'compression': 'none'
    #     }
    #     record['results'] = results

    #     print(yaml.dump([record], default_flow_style=False))
