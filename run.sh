#!/bin/bash
export FLASK_APP=mmm_back
export FLASK_ENV=development
export FLASK_DEBUG=1

source ./mmm_venv/bin/activate

flask run --host=0.0.0.0
