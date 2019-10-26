#!/bin/bash
export FLASK_APP=mmm_back
export FLASK_ENV=development
export FLASK_DEBUG=1

source ./mmm_venv/bin/activate

exec 0>&- # close stdin
exec 1>&- # close stdout
exec 2>&- # close stderr
python3 -m flask run --host=0.0.0.0
