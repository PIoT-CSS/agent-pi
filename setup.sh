#!/bin/bash

IP="$(curl icanhazip.com)"

echo "BROKER_IP=$IP
BROKER_PORT=8080" > .env
