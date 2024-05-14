#!/bin/bash -e

rm -rf emon.dat

source /opt/intel/sep/sep_vars.sh

python3 multi_ins_test_srf.py
