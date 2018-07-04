# **S**ysbench **t**o **Y**AML

This script is a wrapper for the [sysbench](https://github.com/akopytov/sysbench) tool.
It's main purpose is parsing fileio benchmark results, decorating them with environment information passed in command args and retrieved from teh system and storing them in a machine-readable (currently yaml) for easier processing.

# Sample usage 
```bash
wrapper.py -s 30G -m rndrw --disk hdd --fs btrfs --raid simple -o ~/reports.yaml
```