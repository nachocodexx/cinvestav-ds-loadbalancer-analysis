from subprocess import Popen,PIPE,call
import os
BASE_PATH = os.getcwd()
def spawner(*args,**kwargs):
    try:
        workers     = kwargs.get("workers",1)
        worker_name = kwargs.get("name","worker")
        base_port   = kwargs.get("base_port",6000)
        os.environ['WORKERS']=str(workers)
        os.environ['WORKERS_NAME']=str(worker_name)
        os.environ['WORKERS_PORT']=str(base_port)

        call(BASE_PATH+"/cinvestav-ds-spawner-0.1/bin/cinvestav-ds-spawner",shell=True)
    except Exception as e:
        print("ERROR: "+e)


if __name__ =='__main__':
    spawner(workers=2,name='worker',base_port=6000)



