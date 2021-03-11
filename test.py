from subprocess import call
import os
import sys
import time

def runTest(*args,**kwargs):
    # TRACE GENERATOR
    os.environ['TRACE_SAMPLES']       = str(kwargs.get('samples',100))
    os.environ['TRACE_SIZE']          = str(kwargs.get('size',500))
    os.environ['TRACE_INTER_ARRIVAL'] = str(kwargs.get('inter_arrival',100))
    os.environ['TRACE_READ_RATIO']    = str(kwargs.get('read_ratio',80))
    os.environ['TRACE_SAS_SIZE']      = str(kwargs.get('sas_size',549093))
    os.environ['TRACE_MEAN']          = str(kwargs.get('mean',10))
    os.environ['TRACE_STD']           = str(kwargs.get('std',5))
    os.environ['TRACE_CONCURRENCY']   = str(kwargs.get('concurrency',1))
    os.environ['TRACE_DISTRIBUTION']  = str(kwargs.get('distribution', 1))
    # QUEUE SIMULATOR
    os.environ['SERVICE_TIME']        = str(kwargs.get('service_time',1000))
    os.environ['NUM_DELAYS']          = str(kwargs.get('num_delays',50))
    # 
    os.environ['RESULT_FILENAME']     = str(kwargs.get('result_filename','data_00.csv'))
    os.environ['WORKERS']             = str(kwargs.get('workers',2))
    os.environ['WORKERS_PORT']        = str(kwargs.get('workers_port',6000))
    os.environ['LOAD_BALANCER']       = str(kwargs.get('load_balancer',0))
    os.environ['TEST_ID']             = str(kwargs.get('test_id',0))
    call('python3 main.py',shell=True)

if __name__ =='__main__':
    # DISTRIBUTION,LOAD_BALANCER , WORKERS , SAMPLES , IA , ST , FILE, TEST_ID
    LB = 0
    D  = 3 
    F  = 'data_01.csv'
    IA = 3
    ST = 1.45
    tests = [
            (D,LB,1,1000,IA,ST,F,0),
            (D,LB,2,1000,IA,ST,F,1),
            (D,LB,3,1000,IA,ST,F,2),
            (D,LB,4,1000,IA,ST,F,3),
            (D,LB,5,1000,IA,ST,F,4),
           # ________ 
            (D,LB+1,1,1000,IA,ST,F,0),
            (D,LB+1,2,1000,IA,ST,F,1),
            (D,LB+1,3,1000,IA,ST,F,2),
            (D,LB+1,4,1000,IA,ST,F,3),
            (D,LB+1,5,1000,IA,ST,F,4),
            #______________
            (D,LB+2,1,1000,IA,ST,F,0),
            (D,LB+2,2,1000,IA,ST,F,1),
            (D,LB+2,3,1000,IA,ST,F,2),
            (D,LB+2,4,1000,IA,ST,F,3),
            (D,LB+2,5,1000,IA,ST,F,4),
    ]
    for (distribution,load_balancer,workers,samples,inter_arrival,service_time,result_filename,test_id) in tests:
        runTest(load_balancer=load_balancer,
                workers=workers,
                samples =samples,
                inter_arrival=int(inter_arrival*1000),
                service_time=int(service_time*1000),
                result_filename=result_filename,
                test_id=test_id,
                distribution=distribution
                )
        time.sleep(0.5)

