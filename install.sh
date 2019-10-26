#!/bin/bash

python3 -m venv ./mmm_venv
source ./mmm_venv/bin/activate
pip install -r requirements.txt
pip install -e --force .

