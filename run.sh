#!/bin/bash
export FLASK_APP=mmm_back
export FLASK_ENV=development
export FLASK_DEBUG=1

source ./mmm_venv/bin/activate


#!/bin/bash

##
## Shell Daemon For: Backup /root/
## (poorly coded, quick and dirty, example)
##

PIDFILE="flask.pid"
LOGFILE="flask.log"
case $1 in
start)
    exec 0>&- # close stdin
    exec 1>&- # close stdout
    exec 2>&- # close stderr
    nohup $0 run &
    ;;
stop)
    kill $(cat $PIDFILE) || true
    ;;
run)
    python3 -m flask run --host=0.0.0.0 --port=5001 > $LOGFILE 2>&1
    ;;
*)
    echo "$0 [ start | stop ]"
    exit 0
    ;;
esac