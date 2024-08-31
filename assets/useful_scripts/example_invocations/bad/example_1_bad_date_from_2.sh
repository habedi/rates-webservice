#!/bin/bash

# Loading the environment variables
source .env

# Set default values if the environment variables are not set
FLASK_HOST=${FLASK_HOST:-localhost}
FLASK_PORT=${FLASK_PORT:-5000}

# Example for port to port
# Sending a request using HTTPie
url="http://$FLASK_HOST:$FLASK_PORT/rates?date_from=2017-01-01&date_to=2016-01-10&origin=CNSGH&destination=EETLL"
echo "Invocation of the rates webservice with URL: $url"
http GET "$url"
