import os 
import sys
import time
from datetime import datetime as DT
import logging as L
from _utils import Utils as U
from subprocess import Popen, PIPE 
from socket import socket,AF_INET,SOCK_STREAM
from spawner import spawner
import json


def processTrace():
        traceGenerator = Popen([GENERATOR_PATH, SAMPLES, SIZE, INTER_ARRIVAL,READ_RATIO, SAS_SIZE, DISTRIBUTION, MEAN, STD, CONCURRENCY], stdout=PIPE)
        text = None
        while traceGenerator.poll() is None:
            text  = traceGenerator.stdout.read().decode('utf-8')
            text  = U.removeWhiteSpaces(text.split("\n"))
            text2 = U.convertToCSVFormat(text)
            data  = list(map(lambda x: x.split(','), text))
            data  = U.getInterArrival(data)
            return data

if __name__ == '__main__':
    try:
        FORMAT = '%(asctime)-15s [%(levelname)s] %(message)s'
        L.basicConfig(filename="output.log",format=FORMAT,level=L.DEBUG)
        #
        GENERATOR_PATH  = "{}/bins/generator".format(os.getcwd())
        SAMPLES         = str(os.environ.get("TRACE_SAMPLES", 1000))
        SIZE            = str(os.environ.get("TRACE_SIZE", 500))
        INTER_ARRIVAL   = str(os.environ.get("TRACE_INTER_ARRIVAL", 1))
        READ_RATIO      = str(os.environ.get("TRACE_READ_RATIO", 80))
        SAS_SIZE        = str(os.environ.get("TRACE_SAS_SIZE", 549093))
        DISTRIBUTION    = str(os.environ.get("TRACE_DISTRIBUTION", 1))
        MEAN            = str(os.environ.get("TRACE_MEAN", 0))
        STD             = str(os.environ.get("TRACE_STD", 1))
        CONCURRENCY     = str(os.environ.get("TRACE_CONCURRENCY", 1))
        HOST            = os.environ.get("HOST","localhost")
        PORT            = int(os.environ.get("PORT",6665))
        WORKERS_PORT    = int(os.environ.get("WORKERS_PORT",6000))
        WORKERS         = int(os.environ.get('WORKERS',2))
        WORKERS_NAME    = os.environ.get('WORKERS_NAME','worker')
        LOAD_BALANCER   = int(os.environ.get("LOAD_BALANCER",0))
        SERVICE_TIME    = int(os.environ.get("SERVICE_TIME",1000))
        NUM_DELAYS      = int(os.environ.get("NUM_DELAYS",10))
        RESULT_FILENAME = str(os.environ.get("RESULT_PATH","prueba_00.csv"))
        RESULT_PATH     = "./results/{}".format(RESULT_FILENAME)

        # Spawn workers.
        spawner(workers=WORKERS,name=WORKERS_NAME,base_port=WORKERS_PORT)
        # Process trace.
        data  = processTrace() 
        # Load balancer data. 
        _data = {'data':data,'workers':WORKERS,'loadBalancer':LOAD_BALANCER,'basePort':WORKERS_PORT}
        with socket(AF_INET,SOCK_STREAM) as S:
            S.connect((HOST,PORT))
            S.sendall('{}\n'.format(json.dumps(_data)).encode("utf-8"))
            response = U.readAll(S)
            response = json.loads(response)
            response = list(map(U.unpackBins,response))
            with open(RESULT_PATH,'a') as f:
                for index,node in enumerate(response):
                    avgInterArrival = U.getAvgInterArrival(node['bins'])
                    data            = {'avgInterArrival':avgInterArrival,'serviceTime':SERVICE_TIME,'numDelays':NUM_DELAYS}
                    _node           = node['node']
                    port            = int(_node['port'])
                    host            = _node['url']
                    print("Node on port {}:{}".format(host,port))
                    name = '{}-{}'.format(WORKERS_NAME,index)
                    with socket(AF_INET,SOCK_STREAM) as SS:
                        SS.connect((host,port))
                        SS.sendall('{}\n'.format(json.dumps(data)).encode('utf-8'))
                        res = U.readAll(SS)
                        f.write('{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(name,WORKERS,U.loadBalancerToStr(LOAD_BALANCER),res,SAMPLES,SIZE,INTER_ARRIVAL,READ_RATIO,SAS_SIZE,U.distributionToStr(DISTRIBUTION), MEAN,STD,CONCURRENCY,SERVICE_TIME,NUM_DELAYS))
                        #L.info("SEND DATA TO NODE on {}:{}".format(host,port))
                    time.sleep(1)
    except Exception as e:
        print(e)
        L.error("{}".format(e))
