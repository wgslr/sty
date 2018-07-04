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

RAID_TYPES = ['none', 'simple', '0', '1', '5', '6', '10']

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
parser.add_argument('--no-validate',
                    action='store_false',  dest='validate')

# metadata
parser.add_argument('--disk',
                    action='store', choices=DISK_TYPES, required=True)
parser.add_argument('--fs',
                    action='store', dest='filesystem', required=True)
parser.add_argument('-c', '--compression',
                    action='store', default='none')
parser.add_argument('--encryption',
                    action='store', default='none')
parser.add_argument('--raid',
                    action='store', default='none', choices=RAID_TYPES)
parser.add_argument('--host',
                    action='store', default=os.uname().nodename,
                    help='Computer performing the benchmark')


[args, passthru_args] = parser.parse_known_args()


def run(bench_args):
    print("Running ", ' '.join(['sysbench', 'fileio', 'prepare'] + bench_args))
    sp.check_call(['sysbench', 'fileio', 'prepare'] +
                  bench_args, encoding='utf8')

    print("Running ", ' '.join(['sysbench', 'fileio', 'run'] + bench_args))
    output = sp.check_output(
        ['sysbench', 'fileio', 'run'] + bench_args, encoding='utf8')

    print("Running ", ' '.join(['sysbench', 'fileio', 'cleanup'] + bench_args))
    sp.check_call(['sysbench', 'fileio', 'cleanup'] +
                  bench_args, encoding='utf8')

    return output


def make_sysbench_args():
    result = [] + passthru_args
    result.append('--file-total-size={}'.format(args.total_size))
    result.append('--file-test-mode={}'.format(args.test_mode))
    result.append('--time={}'.format(args.time))
    result.append('--file-num={}'.format(args.file_num))
    if args.validate:
        result.append('--validate')
    return result


def parse(output):
    parts = output.lower().split('\n\n')

    yamlish = parts[-5:]

    return yaml.load('\n\n'.join(yamlish))


def gather_metadata():
    timestamp = datetime.datetime.now().isoformat()
    path = os.getcwd()

    return {
        'timestamp': timestamp,
        'path': path,
        'host': args.host,
        'filesystem': args.filesystem,
        'compression': args.compression,
        'raid': args.raid,
        'disk': args.disk,
        'encryption': args.encryption
    }


def gather_params():
    return {
        'file-total-size': args.total_size,
        'file-test-mode': args.test_mode,
        'time': args.time,
        'file-num': args.file_num,
        'validate': args.validate,
        'other': passthru_args
    }


if __name__ == '__main__':
    bench_args = make_sysbench_args()
    output = run(bench_args)

    record = {
        'results': parse(output),
        'metadata': gather_metadata(),
        'params': gather_params()
    }

    yml = yaml.dump([record], default_flow_style=False)
    args.output.write(yml)
