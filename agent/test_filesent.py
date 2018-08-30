import os

import logging
import platform

import requests

if platform.system() in ['Linux']:
    tarDir='./all_img_2018_07_13_17_28_29.tar.gz'
else:
    tarDir='.\\all_img_2018_07_13_17_28_29.tar.gz'

def tarSend( desIP, desPort, rarFile):
    url = 'http://' + desIP + ':' + str(desPort)+'/downloadImg'
    #print(rarFile)
    files = {'file': open(rarFile, 'rb')}
   # return 0

    try:
        r = requests.post(url, files=files)
        r.raise_for_status()
        return 0
    except requests.RequestException as e:
        print(e)
        logging.error("sent file to %s exception: %s ",url,e)
        return 1
    else:
        result = r.json()
        print(type(result), result, sep='\n')
        return 2


if __name__ == "__main__":
    #print("os.getcwd()=%s" % os.getcwd())
    a = tarSend('172.7.21.51','8080',tarDir)