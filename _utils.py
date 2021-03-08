import numpy as np
from functools import reduce
import sys
from subprocess import Popen,PIPE
class Utils:
    @staticmethod
    def getInterArrival(data):
        return list(map(lambda x: int(x[0]), data))

    @staticmethod
    def getAvgInterArrival(data):
        return np.diff(np.array(data)).mean()

    @staticmethod
    def removeWhiteSpaces(data):
        return list(filter(lambda x: not x == '', data))

    @staticmethod
    def convertToCSVFormat(data):
        if(len(data) == 0):
            print("ERROR: {}".format(data))
            sys.exit(0)
        return reduce(lambda x, y: x+"\n"+y, data)
    @staticmethod
    def distributionToStr(x):
        dis = {'1':'UNIFORM','2':'POISSON','3':'NORMAL'}
        return dis[str(x)]
    @staticmethod
    def loadBalancerToStr(x):
        lb = {'0':'ROUND-ROBIN','1':'RANDOM','2':'TWO-CHOICES'}
        return lb[str(x)]
    @staticmethod
    def unpackBins(node):
        bins = node['bins']
        bins = list(map(lambda x:x['value'],bins))
        node['bins']=bins
        return node

    @staticmethod
    def readAll(sock):
        data = ''
        BUFF_SIZE = 4096
        while True:
            _data = sock.recv(BUFF_SIZE)
            data += _data.decode('ascii')
            if(len(_data)<BUFF_SIZE):
                return data
