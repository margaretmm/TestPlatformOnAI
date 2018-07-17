# -*- coding: UTF-8 -*-
import requests
import os
import datetime
import tarfile
import fnmatch
from queue import Queue
from PIL import ImageGrab
import time
import schedule
import threading
import logging
import logging.config

log_filename = "screenAgent.log"
logging.basicConfig(level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filemode='a')

gFileDir = ".\\test\\"
gRarDir = ".\\"

#pip install -i https://pypi.doubanio.com/simple/  schedule
class tarFileTransfer():
    def __init__(self,desIP,desPort):
      #self.gQueue = Queue()  # 创建队列对象
      self.desIP=desIP
      self.desPort=desPort

    def imgCrab(self):
        ct = int(time.time())
        # print(ct)
        a = ImageGrab.grab()
        a.save(gFileDir + str(ct) + '.jpg')
        #self.gQueue.put(ct)

    def count_file(self,path):
        count=0
        ls = os.listdir(path)
        for i in ls:
            count+=1
        return count

    def del_file(self,path):
        ls = os.listdir(path)
        for i in ls:
            c_path = os.path.join(path, i)
            if os.path.isdir(c_path):
                self.del_file(c_path)
            else:
                os.remove(c_path)

    def find_spe_file(self,root, patterns=['*'], non_cludedir=[]):
        for root, dirnames, filenames in os.walk(root):
            for pattern in patterns:
                for filename in filenames:
                    if fnmatch.fnmatch(filename, pattern):
                        #print(filename)
                        yield os.path.join(root, filename)

    def cre_tarfile(self,fileDir):
        args = ["*.jpg", "*.jepg"]
        if self.count_file(fileDir)==0:
            return
        now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        filename = "all_img_{0}.tar.gz".format(now)
        with tarfile.open(filename, mode='w:gz') as f:
            ret=self.find_spe_file(fileDir, args)
            for item in ret:
                #print(item)
                f.add(item)
        if(len(f.members)==0):
            self.del_file('./'+filename)
            return

        ret=1
        count=0
        while (ret>0):
            if (count>=5):
                logging.error("sent file retry times is >5 ")
                break;
            ret=self.tarSend(self.desIP,self.desPort,gRarDir+filename)
            if 0==ret:
                #删除已经打包的图片文件
                self.del_file(gFileDir)
            count+=1
        return

    def tarSend(self,desIP,desPort,rarFile):
        url = 'http://'+ desIP +':'+str(desPort)
        print(rarFile)
        files = {'file': open(rarFile, 'rb')}
        return 0
        '''
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
        '''

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

if __name__ == "__main__":
    a = tarFileTransfer('127.0.0.1','8080')

    schedule.every(50).seconds.do(a.imgCrab)

    schedule.every(3).minutes.do(a.cre_tarfile,gFileDir)
    while True:
        schedule.run_pending()
        time.sleep(1)
    '''
    t1 = threading.Thread(target=a.imgCrabIimer, args=(1,))
    t1.start()
    t1.setDaemon(True)
    #a.imgCrabIimer(1)
    a.tarSendTimer(10)
    t1.join()
    '''