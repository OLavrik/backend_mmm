#!/bin/bash
export FLASK_APP=mmm_back
export FLASK_ENV=development
export FLASK_DEBUG=1

export MEDIA_BASE_URL="http://127.0.0.1/"
#export MEDIA_BASE_URL="http://185.91.53.50/"

flask run --host=0.0.0.0
