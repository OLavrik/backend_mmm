#!/bin/bash

python3 -m venv ./mmm_venv
source ./mmm_venv/bin/activate
pip3 install -r requirements.txt
pip3 install -e .

