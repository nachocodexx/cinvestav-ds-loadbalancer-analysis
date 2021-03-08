#!/bin/sh
export TRACE_SAMPLES=100
export TRACE_SIZE=500
export TRACE_INTER_ARRIVAL=100
export TRACE_READ_RATIO=80
export TRACE_SAS_SIZE=549093
export TRACE_DISTRIBUTION=3
export TRACE_MEAN=10
export TRACE_STD=5
export TRACE_CONCURRENCY=1
export SERVICE_TIME=90
export NUM_DELAYS=100
export RESULT_FILENAME=prueba_00.csv
export WORKERS=2
export WORKERS_NAME=worker
export WORKERS_PORT=6000
export LOAD_BALANCER=0
python3 main.py

