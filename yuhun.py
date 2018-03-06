# coding = utf8
import random
import time
import PIL
import autopy
# 延迟
class sleeptime:
    def __init__(self):
        self.base_num = 1
        self.change_num = 0.1
    def sleep(self,base_num,change_num):
        time.sleep(random.uniform(base_num-change_num,base_num+change_num))

# 操作
class operation(sleeptime):
    def __init__(self):
        sleeptime.__init__()
        self.x = 0
        self.y = 0

    def move(self,x,y):
        autopy.mouse.smooth_move(x,y)
        self.sleep(0.5,0.1)

    def left_click(self,click_times=1):
        n = 0
        while n < click_times:
            n += 1
            autopy.mouse.toggle(True,LEFT_BUTTON)
            self.sleep(0.3,0.1)
            autopy.mouse.toggle(False,LEFT_BUTTON)
            self.sleep(0.5,0.1)


    def key_click(self,key,click_time=1):
        n = 0
        while n < click_time:
            n += 1
            autopy.key.toggle(key,True)
            self.sleep(0.3,0.1)
            autopy.key.toggle(key,False)
            self.sleep(0.5,0.1)

class
