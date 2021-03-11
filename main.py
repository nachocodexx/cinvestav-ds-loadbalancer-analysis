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
        SAMPLES         = str(os.environ.get("TRACE_SAMPLES", 10000))
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
        RESULT_FILENAME = str(os.environ.get("RESULT_FILENAME","prueba_00.csv"))
        RESULT_PATH     = "./results/{}".format(RESULT_FILENAME)
        TEST_ID         = int(os.environ.get("TEST_ID",0))

        # Spawn workers.
        spawner(workers=WORKERS,name=WORKERS_NAME,base_port=WORKERS_PORT)
        # Process trace.
        data  = processTrace() 
        data  = list(map(lambda x: x/1000,data))
        # Load balancer data. 
        _data = {'data':data,'workers':WORKERS,'loadBalancer':LOAD_BALANCER,'basePort':WORKERS_PORT}
        with socket(AF_INET,SOCK_STREAM) as S:
            S.connect((HOST,PORT))
            S.sendall('{}\n'.format(json.dumps(_data)).encode("utf-8"))
            response = U.readAll(S)
            response = json.loads(response)
            response = list(map(U.unpackBins,response))
            #print(response)
            with open(RESULT_PATH,'a') as f:
                for index,node in enumerate(response):
                    balls           = node['bins']
                    ballsLen        = len(balls)
                    avgInterArrival = U.getAvgInterArrival(balls)
                    ND              = ballsLen
                    data            = {'avgInterArrival':avgInterArrival,'serviceTime':SERVICE_TIME,'numDelays':ND}
                    _node           = node['node']
                    port            = int(_node['port'])
                    host            = _node['url']
                    print("Node on port {}:{}".format(host,port))
                    print('_'*20)
                    name = '{}-{}'.format(WORKERS_NAME,index)
                    with socket(AF_INET,SOCK_STREAM) as SS:
                        SS.connect((host,port))
                        SS.sendall('{}\n'.format(json.dumps(data)).encode('utf-8'))
                        res               = U.readAll(SS)
                        _res              = list(map(lambda x:float(x),res.split(',')))
                        loadBalancerStr   = U.loadBalancerToStr(LOAD_BALANCER)
                        distributionToStr = U.distributionToStr(DISTRIBUTION)
                        csvText = [name,ballsLen,
                                WORKERS,loadBalancerStr,
                                res,SAMPLES,
                                SIZE,INTER_ARRIVAL,
                                READ_RATIO,SAS_SIZE,
                                distributionToStr,MEAN,
                                STD,CONCURRENCY,
                                SERVICE_TIME,avgInterArrival,ND,
                                TEST_ID]
                        csvText = list(map(lambda x:str(x),csvText))
                        csvText = ','.join(csvText)



                        print("NUM. REQUESTS: {}\nAVG.INTERARRIVAL: {} sec\nSERVICE TIME: {} sec\nAVG. DELAY IN QUEUE: {} sec\nNUM. IN QUEUE: {}\nSERVER UTILIZATION:{}%\nSIMULATION TIME: {} sec".format(len(balls),avgInterArrival/1000,SERVICE_TIME/1000,_res[0]/1000,_res[1],_res[2]*100,_res[3]/1000))
                        print('_'*20)
                        f.write(csvText+"\n")
                    time.sleep(.5)
    except Exception as e:
        print(e)
        L.error("{}".format(e))
