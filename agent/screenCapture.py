import inceptionV3.dirDef as gDir
import time
from PIL import ImageGrab
import schedule

#pip install -i https://pypi.doubanio.com/simple/  schedule
def imgCrab():
    ct = int(time.time())
    #print(ct)
    a=ImageGrab.grab()
    a.save(gDir.TEST_IMG +str(ct)+'.jpg')

if __name__ == '__main__':
    schedule.every(1).minutes.do(imgCrab)
    while True:
        schedule.run_pending()
        time.sleep(1)