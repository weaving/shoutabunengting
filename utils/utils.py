import cv2 as cv
import easyocr
import numpy as np
import time
import pyautogui
import pywintypes
import win32api
import win32gui
import win32print
import win32con
import math
import random
import win32gui, win32com.client, pythoncom
import os
import threading
import ctypes
import pyautogui as pag
from utils.log import log
import psutil
from aip import AipOcr
from PIL import Image
import cv2 as cv2
import yaml


class UniverseUtils:
    def __init__(self):


        self.my_nd = win32gui.GetForegroundWindow()

        self.debug = 0

        # set_forground()
        # self.check_bonus = 1
        self._stop = 0
        self.time_cnt = 0  # 准备战斗 如果倒计时15秒还没开始，就换个房间
        self.recognize_cnt_max = 7  # 7代表 识别最多7次三个武将，因为武将有时候会闪闪的，导致识别不正确
        self.start_time = 0
        self.end_time = 0
        self.run_time = 0   # 本轮战斗运行时间
        self.refresh_cnt = 0    #统计刷新次数
        self.battle_cnt = 0 #统计这是第几个战斗循环
        self.battle_success_cnt = 0 # 统计成功刷了几次
        self.qiwang_battle_cnt = 99#
        self.hun_needed = 0
        self.beiT_cnt = 0

        self.name_readyToWork = '' # 要去准备干活的武将
        self.start_D_pai = 1 #默认值得是1 ，不然开始就不D排了
        self.battle_phase = 1 #刚开始是第一回合
        self.renkou_cur = 0     #当前人口 根据购买的卡来统计 不升级才会增加，增加是根据LV1 LV2 LV3里面的名单
        self.number_renkou_max = 0  # 最大人口 通过 ocr 识别
        self.battle_phase_final_deleted_flag = 0    # 最终阵容标志位

        self.verify_cnt = 0
        self.shuaxin_wujiang = ['a', 'b', 'c', 'd']
        self.shuaxin_wujiang_last = ['a', 'b', 'c', 'd']
        self.wujiang_recognize_cnt = 0
        self.refresh_cnt_max = [6,6,6,6,10,10,10,40,50,9999,9999]
        self.wuqi = [ 'chailangshou', 'chuanxinjian', 'chumoshu', 'dawangfu', 'duochonggong', 'duolingqiang',
                      'feihuadan', 'fengleibian', 'fulongsuo', 'fuxiqin', 'ganjiang', 'gongshouzhangu', 'guiguzi',
                      'haimohaojiao', 'hairenchui', 'hanbingzhou', 'hongyijupao', 'huifengzhenfa', 'huimoxinfa',
                      'huogongshu', 'jifengjian', 'jinshejian', 'jubaopeng', 'kaishanchui', 'kaitianfu', 'kongdongyin',
                      'kongmozhu', 'kuangfengfu', 'kunxianshu', 'lihunchui', 'lingshoudan', 'lingyuanhaojiao', 'longlin',
                      'lvshichunqiu', 'lvxing', 'miaofabaodian', 'mingdaotianzhu', 'mingleifazhang', 'moxie', 'nuguijian',
                      'pingtianguan', 'pojianujian', 'pozhen', 'qiankunfu', 'qiankunshan', 'qumoling', 'sanshiliuji',
                      'shamodao', 'shangjunshu', 'shaweibang', 'shishenling', 'suijinchui', 'sunzibingfa', 'taia', 'tianfajian',
                      'tianhuhaojiao', 'tulong', 'tumozhoufa', 'wolongshan', 'wudelv', 'wuduhulu', 'wuguihulu', 'xiangmobaozhang',
                      'xiangmoshu', 'xingtianfu', 'yangxinfa', 'yangxinshi', 'yinshejian', 'yinyangbian', 'yuanlingjian', 'yuchang',
                      'yumobian', 'yumochui', 'yumofu', 'zhinangjing','baojunfu','daodejing','feiyanzhu',]




        hwnd = win32gui.GetForegroundWindow()  # 根据当前活动窗口获取句柄
        # 获取屏幕的尺寸
        self.screen_max_x = 1920
        self.screen_max_y = 1080
        self.x0, self.y0, self.x1, self.y1 = win32gui.GetClientRect(hwnd)
        self.xx = self.x1 - self.x0
        self.yy = self.y1 - self.y0
        self.x0, self.y0, self.x1, self.y1 = win32gui.GetWindowRect(hwnd)

        self.full = self.x0 == 0 and self.y0 == 0
        self.x0 = max(0, self.x1 - self.xx) + 9 * self.full
        self.y0 = max(0, self.y1 - self.yy) + 9 * self.full
        if (self.xx == 1920 or self.yy == 1080) and self.xx >= 1920 and self.yy >= 1080:
            self.x0 += (self.xx - 1920) // 2
            self.y0 += (self.yy - 1080) // 2
            self.x1 -= (self.xx - 1920) // 2
            self.y1 -= (self.yy - 1080) // 2
            self.xx, self.yy = 1920, 1080



    def format_path(self, path):
        return f"./imgs/{path}.png"

    def format_path_wujiang(self, path):
        return f"./imgs/wujiang/{path}.png"
    def format_path_wujiang_bottom(self, path):
        return f"./imgs/wujiang_bottom/{path}.png"
    def format_path_wujiang_xinyuan(self, path):
        return f"./imgs/wujiang_xinyuan/{path}.png"
    def format_path_wujiang_share(self, path):
        return f"./imgs/wujiang_share/{path}.png"
    def format_path_wuqi(self, path):
        return f"./imgs/wuqi/{path}.png"
    def format_path_qianghua(self, path):
        return f"./imgs/qianghua/{path}.png"

    def changeWindow(self):
        # 先等待3秒
        time.sleep(0.3)

        # 查找窗口句柄
        hwnd = win32gui.FindWindow(0, u"M4DEAD")
        # print(hwnd)
        Text = win32gui.GetWindowText(hwnd)
        if hwnd != 0:
            # 若最小化，则将其显示，反之则最小化
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            else:

                win32gui.SetForegroundWindow(hwnd)

            # 关闭窗口
            # win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        if hwnd == 0:
            self.Recovery()
            log.info("没有打开游戏,你玩蛇皮")


    # 从全屏截屏中裁剪得到游戏窗口截屏
    def get_screen(self):
        i = 0
        if self.debug == 1:
            time.sleep(0.3)
        while True:
            try:
                screen_raw = pyautogui.screenshot(region=[self.x0, self.y0, self.xx, self.yy])
                screen_raw = np.array(screen_raw)
            except:
                print("截图失败!")
                time.sleep(0.1)
                continue
            if screen_raw.shape[0] > 3:
                break
            else:
                i = min(i + 1, 20)
                print("截图失败")
                time.sleep(0.2 * i)
        self.screen = cv.cvtColor(screen_raw, cv.COLOR_BGR2RGB)

        # cv.imwrite("imgs/screen.jpg", self.screen)
        return self.screen

    # def check(self, path, x, y, mask=None, threshold=None, large=True):
    def get_local(self, x0, x1, y0, y1,  large=True):

        return self.screen[
               y0:y1,
               x0:x1

               ]


    def check(self, path, x0=0, x1=1920, y0=0, y1=1080, threshold=None, large=True):
        if threshold is None:
            threshold = self.threshold
        path = self.format_path(path)
        target = cv.imread(path)  # 字节数组直接转字符串，不解码

        shape = target.shape
        local_screen = self.get_local(x0, x1, y0, y1)
        # cv.imshow("www",local_screen)
        # cv.waitKey(0)
        result = cv.matchTemplate(local_screen, target, cv.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        log.debug(path)
        log.debug(max_val)
        if max_val > threshold:


            self.location_x = max_loc[0]
            self.location_y = max_loc[1]
            self.location_x = self.location_x + x0
            self.location_y = self.location_y + y0
            log.debug("匹配到图片 %s,相似度 %f,阈值 %f, x:%d, y:%d" % (path, max_val, threshold,self.location_x,self.location_y))

            if path == 'yincang':
                timw_now = time.time()
                time_now = self.start_time - timw_now
                log.info("出现隐藏界面的时间：%d", time_now)
            if path == 'wozhidaole':
                timw_now = time.time()
                time_now = self.start_time - timw_now
                log.info("我知道了界面时间：%d", time_now)
        # cv.imshow("www",local_screen)
        # cv.waitKey(0)
        return max_val > threshold

    def check_wujiang_bottom(self, path, threshold=None):


        if threshold is None:
            threshold = self.threshold

        path = self.format_path_wujiang_bottom(path)
        if os.path.exists(path) == False:
            log.info("%s not found",(path))
            return
        target = cv.imread(path)  # 字节数组直接转字符串，不解码
        x0 = 550
        x1 = 1500
        y0 = 750
        y1 = 1080
        local_screen = self.get_local(x0, x1, y0, y1)

        # cv.imshow("www",local_screen)
        # cv.waitKey(0)

        result = cv.matchTemplate(local_screen, target, cv.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if max_val > threshold:
            log.debug("匹配到bottom图片 %s 相似度 %f 阈值 %f" % (path, max_val, threshold))
            self.location_bottom_x = max_loc[0] + x0
            self.location_bottom_y = max_loc[1] + y0
        # cv.imshow("www",local_screen)
        # cv.waitKey(0)
        if max_val > threshold:
            try:
                log.debug(self.wujiang_recognize_cnt)
            except:
                log.error("err")


        return max_val > threshold

    def check_wuqi(self, path,pos=1, threshold=None):

        if threshold is None:
            threshold = self.threshold

        path = self.format_path_wuqi(path)
        if os.path.exists(path) == False:
            log.info("%s not found", (path))
            return
        target = cv.imread(path)  # 字节数组直接转字符串，不解码
        if pos == 1 :
            x0 = 1200
            x1 = 1300
            y0 = 500
            y1 = 600
        if pos == 2 :
            x0 = 1324
            x1 = 1412
            y0 = 500
            y1 = 600
        if pos == 3 :
            x0 = 1434
            x1 = 1521
            y0 = 500
            y1 = 600
        if pos == 4 :
            x0 = 1543
            x1 = 1631
            y0 = 500
            y1 = 600
        if pos == 5 :
            x0 = 1200
            x1 = 1300
            y0 = 640
            y1 = 728
        if pos == 6 :
            x0 = 1324
            x1 = 1412
            y0 = 640
            y1 = 728
        if pos == 7 :
            x0 = 1434
            x1 = 1521
            y0 = 640
            y1 = 728
        if pos == 8 :
            x0 = 1543
            x1 = 1631
            y0 = 640
            y1 = 728
        local_screen = self.get_local(x0,x1,y0,y1)

        # cv.imshow("www",local_screen)
        # cv.waitKey(0)

        result = cv.matchTemplate(local_screen, target, cv.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        log.debug(max_val)
        if max_val > threshold:
            log.debug("匹配到wuqi图片 %s 相似度 %f 阈值 %f" % (path, max_val, threshold))
            self.location_x = max_loc[0] + x0
            self.location_y = max_loc[1] + y0
        # cv.imshow("www",local_screen)
        # cv.waitKey(0)
        if max_val > threshold:
            try:
                log.debug(self.wujiang_recognize_cnt)
            except:
                log.error("err")

        return max_val > threshold


    def check_qianghua(self, path, threshold=None):

        if threshold is None:
            threshold = self.threshold

        path = self.format_path_qianghua(path)
        if os.path.exists(path) == False:
            log.info("%s not found", (path))
            return
        target = cv.imread(path)  # 字节数组直接转字符串，不解码
        x0=0
        x1=1920
        y0=0
        y1 = 1080
        local_screen = self.get_local(x0,x1,y0,y1)

        # cv.imshow("www",local_screen)
        # cv.waitKey(0)

        result = cv.matchTemplate(local_screen, target, cv.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        log.debug(max_val)
        if max_val > threshold:
            log.debug("匹配到wuqi图片 %s 相似度 %f 阈值 %f" % (path, max_val, threshold))
            self.location_x = max_loc[0] + x0
            self.location_y = max_loc[1] + y0
        # cv.imshow("www",local_screen)
        # cv.waitKey(0)
        if max_val > threshold:
            try:
                log.debug(self.wujiang_recognize_cnt)
            except:
                log.error("err")


        return max_val > threshold

    def check_wujiang_xinyuan(self, path, threshold=None):


        if threshold is None:
            threshold = self.threshold

        path = self.format_path_wujiang_xinyuan(path)
        if os.path.exists(path) == False:
            log.info("%s not found",(path))
            return
        target = cv.imread(path)  # 字节数组直接转字符串，不解码
        x0 = 0
        x1 = 1920
        y0 = 350
        y1 = 1080
        local_screen = self.get_local(x0, x1, y0 , y1)

        # cv.imshow("www",local_screen)
        # cv.waitKey(0)

        result = cv.matchTemplate(local_screen, target, cv.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if max_val > threshold:
            log.debug("匹配到xinyuan图片 %s 相似度 %f 阈值 %f,x:%d,y:%d" % (path, max_val, threshold,max_loc[0],max_loc[1]))
            self.location_x = max_loc[0] + x0
            self.location_y = max_loc[1] + y0
        # cv.imshow("www",local_screen)
        # cv.waitKey(0)
        if max_val > threshold:
            try:
                log.debug(self.wujiang_recognize_cnt)
            except:
                log.error("err")

        self.click()
        return max_val > threshold

    def check_wujiang_share(self, path, threshold=None):


        if threshold is None:
            threshold = self.threshold

        path = self.format_path_wujiang_share(path)
        if os.path.exists(path) == False:
            log.info("%s not found",(path))
            return
        target = cv.imread(path)  # 字节数组直接转字符串，不解码
        x0 = 200
        x1 = 1200
        y0 = 500
        y1 = 750
        local_screen = self.get_local(x0, x1, y0, y1)

        # cv.imshow("www",local_screen)
        # cv.waitKey(0)

        result = cv.matchTemplate(local_screen, target, cv.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if max_val > threshold:
            log.debug("匹配到bottom图片 %s 相似度 %f 阈值 %f" % (path, max_val, threshold))
            self.location_x = max_loc[0] + x0
            self.location_y = max_loc[1] + y0
        # cv.imshow("www",local_screen)
        # cv.waitKey(0)
        if max_val > threshold:
            try:
                log.debug(self.wujiang_recognize_cnt)
            except:
                log.error("err")

        return max_val > threshold

    def check_wujiang(self, path, threshold=None, large=True):
        if threshold is None:
            threshold = self.threshold

        name = path
        path = self.format_path_wujiang(path)
        if os.path.exists(path) == False:
            # print("%s not found"%(path))
            return
        target = cv.imread(path)  # 字节数组直接转字符串，不解码

        shape = target.shape
        if self.tequan == 0:
            x0 = 350
            x1 = 1200
            y0 = 350
            y1 = 450
        if self.tequan == 1 :
            x0 = 350
            x1 = 1400
            y0 = 350
            y1 = 450

        local_screen = self.get_local(x0, x1, y0, y1)

        # cv.imshow("www",local_screen)
        # cv.waitKey(0)

        result = cv.matchTemplate(local_screen, target, cv.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if max_val > threshold:
            log.debug("匹配到图片 %s 相似度 %f 阈值 %f" % (path, max_val, threshold))
            self.location_x = max_loc[0] + x0
            self.location_y = max_loc[1] + y0
        # cv.imshow("www",local_screen)
        # cv.waitKey(0)
        if max_val > threshold:
            try:
                log.debug(self.wujiang_recognize_cnt)
            except:
                log.error("err")
            try:
                log.debug(self.shuaxin_wujiang[0])
            except:
                log.error("err2")



            self.shuaxin_wujiang[self.wujiang_recognize_cnt] = name
            self.shuaxin_wujiang_pos[self.wujiang_recognize_cnt][0] = max_loc[0] + 350
            self.shuaxin_wujiang_pos[self.wujiang_recognize_cnt][1] = max_loc[1] + 350
            self.wujiang_recognize_cnt = self.wujiang_recognize_cnt + 1

        return max_val > threshold

    def click(self, t=0):
        try:
            if self._stop == 0:
                win32api.SetCursorPos((self.location_x, self.location_y))
                time.sleep(0.1)
                pyautogui.click()
        except:
            log.error("click error")
        time.sleep(0.3)
        if self.debug == 0:
            time.sleep(t)
        self.get_screen()

    def press(self, c, t=0):
        if c not in '3r':
            log.debug(f"按下按钮 {c}，等待 {t} 秒后释放")
        if self._stop == 0:
            pyautogui.keyDown(c)
        time.sleep(t)
        pyautogui.keyUp(c)

    def Find_Priority_wujiang(self):
        if self.battle_phase == 1:
            list = self.battle_phase_lv1_list
        if self.battle_phase == 2:
            list = self.battle_phase_lv2_list
        if self.battle_phase == 3:
            list = self.battle_phase_lv3_list
        if self.battle_phase == 4:
            list = self.battle_phase_lv4_list
        if self.battle_phase == 5:
            list = self.battle_phase_lv5_list
        if self.battle_phase == 6:
            list = self.battle_phase_lv6_list
        if self.battle_phase == 7:
            list = self.battle_phase_lv7_list
        if self.battle_phase == 8:
            list = self.battle_phase_lv8_list
        if self.battle_phase == 9:
            list = self.battle_phase_lv9_list
        if self.battle_phase == 10:
            list = self.battle_phase_lv10_list
        if self.battle_phase == 11:
            list = self.battle_phase_lv11_list
        self.name_readyToWork = 'NA'
        min1 = 100
        min2 = 100
        min3 = 100
        min4 = 100
        self.shuaxin_wujiang_pos_idx = 0
        for j in range(len(list)):
            if self.shuaxin_wujiang[0] == list[j]:
                min1 = j
            if self.shuaxin_wujiang[1] == list[j]:
                min2 = j
            if self.shuaxin_wujiang[2] == list[j]:
                min3 = j
            if self.shuaxin_wujiang[3] == list[j]:
                min4 = j
        tmp = min(min1, min2, min3, min4)
        if tmp == min1:
            self.shuaxin_wujiang_pos_idx = 0
        if tmp == min2:
            self.shuaxin_wujiang_pos_idx = 1
        if tmp == min3:
            self.shuaxin_wujiang_pos_idx = 2
        if tmp == min4:
            self.shuaxin_wujiang_pos_idx = 3

        if self.buy_cnt[self.shuaxin_wujiang[0]] == 0 and \
              self.shuaxin_wujiang[0] in list:
            self.shuaxin_wujiang_pos_idx = 0

        if self.buy_cnt[self.shuaxin_wujiang[1]] == 0 and \
              self.shuaxin_wujiang[1] in list:
            self.shuaxin_wujiang_pos_idx = 1

        if self.buy_cnt[self.shuaxin_wujiang[2]] == 0 and \
              self.shuaxin_wujiang[2] in list:
            self.shuaxin_wujiang_pos_idx = 2

        try:
            if self.buy_cnt[self.shuaxin_wujiang[3]] == 0 :
                if self.shuaxin_wujiang[3] in list:
                    self.shuaxin_wujiang_pos_idx = 3
        except:
            log.debug("没有这个武将")

        if tmp != 100:
            self.name_readyToWork = self.shuaxin_wujiang[self.shuaxin_wujiang_pos_idx]
            log.info("战斗阶段:%d,找到了优先级武将 :%s,优先级:%d", self.battle_phase, self.name_readyToWork, tmp)
        else:
            log.info("战斗阶段:%d,没有找到优先级武将 :%s,优先级:%d", self.battle_phase, self.name_readyToWork, tmp)

    def drag_quick(self, abs_pos):
        self.location_x = self.location_bottom_x+30  # 武將位置
        self.location_y = self.location_bottom_y-30
        win32api.SetCursorPos((self.location_x, self.location_y))
        time.sleep(0.2)
        des_x = abs_pos[0]
        des_y = abs_pos[1]
        log.info("拖动出发地 --- 目的地 org_x:%d,org_y:%d, des_x:%d,des_y:%d",self.location_x,self.location_y,des_x,des_y)
        if self.location_x >= des_x and (self.location_x - des_x) < 20:
            des_x = abs_pos[0] - 20
        if self.location_y >= des_y and (self.location_y - des_y) < 20:
            des_y = abs_pos[1] - 20

        if self.location_x <= des_x and (des_x - self.location_x ) < 20:
            des_x = abs_pos[0] + 20
        if self.location_y <= des_y and (des_y - self.location_y ) < 20:
            des_y = abs_pos[1] + 20


        log.info("拖动出发地优化后 --- 目的地 org_x:%d,org_y:%d, des_x:%d,des_y:%d",self.location_x,self.location_y,des_x,des_y)

        pyautogui.dragTo(des_x, des_y, 1, button='left')  # 按住鼠标左键，用0.5s将鼠标拖拽至1230，458

    def drag_safe(self, abs_pos):
        timeout = 25
        while timeout>1:
            self.all_tiaozhan()
            self.get_screen()
            self.recognize_renkou()
            if self.renkou_cur + self.wujiang_renkou_delta <= self.number_renkou_max:

                break

            timeout = timeout - 1
            if timeout == 1:
                log.info("识别最大人口超时")
            log.info("卡人口了 当前人口 %d/%d",self.renkou_cur,self.number_renkou_max)


            # 即便拖武将卡人口了 社畜还是不能停下干活
            self.update_hun(1)
            self.click_update_renkou(1)

            time.sleep(1)
        self.checkAndClick('yincang', 0, 960, 540, self.screen_max_y)

        self.location_x = self.location_bottom_x+30  # 武將位置
        self.location_y = self.location_bottom_y-30
        win32api.SetCursorPos((self.location_x, self.location_y))
        time.sleep(0.2)
        des_x = abs_pos[0]
        des_y = abs_pos[1]
        log.info("拖动出发地 --- 目的地 org_x:%d,org_y:%d, des_x:%d,des_y:%d",self.location_x,self.location_y,des_x,des_y)
        if self.location_x >= des_x and (self.location_x - des_x) < 20:
            des_x = abs_pos[0] - 20
        if self.location_y >= des_y and (self.location_y - des_y) < 20:
            des_y = abs_pos[1] - 20

        if self.location_x <= des_x and (des_x - self.location_x ) < 20:
            des_x = abs_pos[0] + 20
        if self.location_y <= des_y and (des_y - self.location_y ) < 20:
            des_y = abs_pos[1] + 20


        log.info("拖动出发地优化后 --- 目的地 org_x:%d,org_y:%d, des_x:%d,des_y:%d",self.location_x,self.location_y,des_x,des_y)

        pyautogui.dragTo(des_x, des_y, 1, button='left')  # 按住鼠标左键，用0.5s将鼠标拖拽至1230，458

    def drag_debug(self, abs_pos):
        delay_cnt = 25

        self.location_x = self.location_bottom_x+30  # 武將位置
        self.location_y = self.location_bottom_y-30
        win32api.SetCursorPos((self.location_x, self.location_y))
        x = abs_pos[0]
        y = abs_pos[1]
        log.info("拖动出发地 --- 目的地 org_x:%d,org_y:%d, des_x:%d,des_y:%d",self.location_bottom_x,self.location_bottom_y,x,y)
        print(x)
        print(y)

        # pyautogui.dragTo(x, y, 2.8, button='left')  # 按住鼠标左键，用0.5s将鼠标拖拽至1230，458

    def dragForMainDataInit(self):
        x = 900  # 武將位置
        y = 800
        win32api.SetCursorPos((x, y))
        if self.location_left_right == 2:
            delta_x = self.ref_abs_pos_x - 777 # 黄金位置
            delta_y = self.ref_abs_pos_y - 440
            x = 900 - int(delta_x/1.84)
            y = 800 - int(delta_y)
        else:
            delta_x = self.ref_abs_pos_x - 564 # 黄金位置
            delta_y = self.ref_abs_pos_y - 440
            x = 900 - int(delta_x/1.84)
            y = 800 - int(delta_y)

        pyautogui.dragTo(x, y, 0.2, button='left')  # 按住鼠标左键，用0.5s将鼠标拖拽至1230，458
        time.sleep(0.5)
        pyautogui.dragTo(x, y, 0.2, button='left')  # 按住鼠标左键，用0.5s将鼠标拖拽至1230，458



    def getMousePos(self):
        while True:
            x, y = pag.position()  # 返回鼠标的坐标
            print(" Position : (%s, %s)\n" % (x, y))  # 打印坐标

            time.sleep(1)  # 每个1s中打印一次 , 并执行清屏
            os.system('cls')  # 执行系统清屏指令

    def main_data_init(self):
        self.start_time = time.time()
        self.end_time = 0
        self.run_time = 0
        self.last_time = 0
        self.run_time_last = 0
        self.refresh_cnt = 0  # 用来统计刷新次数
        self.renkou_cur = 0
        self.battle_phase8_deleted_flag = 0 # 8阶段要删除过度用的紫卡 只删一次
        self.start_D_pai =1
        self.battle_phase = 1 #刚开始是第一回合
        self.pos_index = 0
        self.pos_index_lv1 = 0
        self.pos_index_lv2 = 0
        self.pos_index_lv3 = 0
        self.spec_pos_index_lv3 = 0
        self.battle_phase_final_deleted_flag = 0
        self.shuaxin_wujiang = ['a', 'b', 'c', 'd']
        self.ref_update_flag = 0
        self.drag_zhuangbei_flag = 0
        self.drag_zhuangbei_flag2 = 0
        self.drag_zhuangbei_flag3 = 0
        self.number_hun_max = 0
        self.expect_flag = 0       #期望能否战斗胜利
        self.yijianronghe_cnt = 1 # 统计融合次数
        self.touxiang_cnt = 0
        self.jinbichongneng_state = 0
        for i in range(len(self.wujiang_all_list)):
            self.dict_lv[self.wujiang_all_list[i]] = 1

        self.dict_wuqi = {}

        for i in range(len(self.wujiang_all_list)):
            self.dict_wuqi[self.wujiang_all_list[i]] = 0
        self.buy_cnt = {}

        for i in range(len(self.wujiang_all_list)):
            self.buy_cnt[self.wujiang_all_list[i]] = 0
        log.info("当前战斗轮数 :%d",self.battle_cnt)

        self.four_huang_list = []
        self.four_huang_list_done = 0
        self.final_list_done = 0


        self.battle_phase_lv1_list = []
        self.battle_phase_lv1_list.extend(self.lv3_list)
        self.battle_phase_lv1_list.extend(self.lv2_list)
        self.battle_phase_lv1_list.extend(self.lv1_list)
        self.battle_phase_lv2_list = self.battle_phase_lv1_list  #4
        self.battle_phase_lv3_list = self.battle_phase_lv1_list  #5
        self.battle_phase_lv4_list = self.battle_phase_lv1_list
        self.battle_phase_lv5_list = self.battle_phase_lv1_list
        self.battle_phase_lv6_list = self.battle_phase_lv1_list
        self.battle_phase_lv7_list = self.battle_phase_lv1_list
        self.battle_phase_lv8_list = self.battle_phase_lv1_list
        self.battle_phase_lv9_list = self.battle_phase_lv1_list
        self.battle_phase_lv10_list = self.battle_phase_lv1_list
        self.battle_phase_lv11_list = self.battle_phase_lv1_list

        self.dict_pos_use = self.dict_pos_default
        self.lv1_already_have = []

        self.firstlook_huangjiang_black_cnt = 0
        self.firstlook_zijiang_black_cnt = 0
        self.firstlook_lanjiang_black_cnt = 0
        self.firstlook_huangjiang_white_cnt = 0
        self.firstlook_zijiang_white_cnt = 0
        self.firstlook_lanjiang_white_cnt = 0

        self.firstlook_huangjiang_cnt = 0

        self.battle_success_flag = 0
        self.exit_game_flag = 0


        with open('config.yml', 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        for i in range(len(self.battle_phase_lv1_list)):
            try :
                tmp = self.battle_phase_lv1_list[i] + "_wuqi" # lishimin_wuqi
                self.wujiang_wuqi[self.battle_phase_lv1_list[i]] = config['database'][tmp]
            except:
                1
    def sub_data_init(self):
        self.end_time = time.time()
        self.run_time = self.end_time - self.start_time
        if int(self.run_time - self.run_time_last) > 20:
            log.info("当前成功刷了%d/%d次,投降%d次,被T次数统计%d,当前验证码识别次数:%d,当前运行时间 :%ds,预计结束时间,:%ds,当前人口 :%d/%d, 当前战斗阶段:%d",
                     self.battle_success_cnt,self.battle_cnt,self.touxiang_cnt,self.beiT_cnt,self.verify_cnt, self.run_time,(2160-int(self.run_time)),self.renkou_cur,self.number_renkou_max,self.battle_phase)
            self.run_time_last = self.run_time
        
        if self.run_time > 31*60 and self.battle_success_flag == 0:
            self.battle_success_cnt = self.battle_success_cnt + 1
            self.battle_success_flag = 1
        self.get_screen()
        if self.battle_phase == 10:
            self.recognize_renkou()

        if self.run_time == -1:
            self.recognize_money()
            self.recognize_hun()
            self.recognize_round()
            self.recognize_renkou()
    def update_run_time(self):
        self.run_time = self.end_time - self.start_time

    def recognize_hun(self):
        self.get_screen()

        screen = self.screen[
            30:75,
            270:330,
        ]
        text = easyocr.Reader(['ch_sim', 'en'],gpu=False)
        data = text.readtext(screen, detail=0)
        try:
            self.number_hun = int(data[0])
            log.info("当前魂 :%d", self.number_hun)
        except:
            print("当前魂识别失败")

    def recognize_hun_needed(self):
        self.get_screen()
        screen = self.screen[
            637:688,
            1746:1868,
        ]
        text = easyocr.Reader(['ch_sim', 'en'], gpu=False)

        data = text.readtext(screen, detail=0)
        data = ' '.join(data)
        data = data.split('/')

        try:
            self.hun_needed = int(data[1]) - int(data[0])
            self.number_hun_max = int(data[1])

            log.info("当前升级所需魂 :%d, 当前统计:%d/%d", self.hun_needed,int(data[0]),int(data[1]))
        except:
            print("当前魂识别失败")
    def recognize_money(self):
        self.get_screen()

        screen = self.screen[
            30:75,
            90:180,
        ]
        text = easyocr.Reader(['ch_sim', 'en'], gpu=False)
        data = text.readtext(screen, detail=0)
        try:
            self.number_money = int(data[0])
            log.info("当前金钱 :%d", self.number_money)
        except:
            print("当前魂识别失败")


    def recognize_renkou(self):
        self.get_screen()

        screen = self.screen[
            30:75,
            505:600,
        ]

        text = easyocr.Reader(['ch_sim', 'en'], gpu=False)
        data = text.readtext(screen, detail=0)
        data = ' '.join(data)
        data = data.split('/')

        try:
            self.number_renkou_max = int(data[1])
            self.renkou_cur = int(data[0])  # 更新下当前人口

            log.info("当前最大人口 :%d,当前人口情况 :%d/%d", self.number_renkou_max,int(data[0]),int(data[1]))


        except:

            print("当前最大人口别失败")
        return self.number_renkou_max

    def recognize_round(self):
        self.get_screen()

        screen = self.screen[
                 90:123,
                 700:723,
                 ]

        text = easyocr.Reader(['ch_sim', 'en'], gpu=False)
        data = text.readtext(screen, detail=0)
        try:
            self.number_renkou_max = int(data[0])
            log.info("当前波数 :%d", self.number_renkou_max)

        except:
            print("波数识别失败")




    def update_renkou(self,ii=1):#升级人口后 就得D牌了
        self.location_x = 1800
        self.location_y = 760
        for i in range(ii):
            self.click()

    def click_update_renkou(self, ii=1):  # 升级人口后 就得D牌了
        self.location_x = 1800
        self.location_y = 760
        for i in range(ii):
            self.click()
        # self.start_D_pai = 1
    def update_hun(self,ii=1):#升级人口后 就得D牌了
        if self.jinbichongneng_state == 1:
            self.location_x = 1600
            self.location_y = 750
            for i in range(ii):
                self.click()
                log.debug("点了升级魂%d次",i)


    def check_money(self ):


        y0 = 300
        y1 = 500
        self.location_y = self.shuaxin_wujiang_pos[self.shuaxin_wujiang_pos_idx][1]
        if  self.shuaxin_wujiang_pos[self.shuaxin_wujiang_pos_idx][0] <500 :
            x0 = 500
            x1 = 500+300

        if  self.shuaxin_wujiang_pos[self.shuaxin_wujiang_pos_idx][0] >500 \
                and self.shuaxin_wujiang_pos[self.shuaxin_wujiang_pos_idx][0] >500 < 800:
            x0 = 800
            x1 = 800+300
        if  self.shuaxin_wujiang_pos[self.shuaxin_wujiang_pos_idx][0] >800 \
                and self.shuaxin_wujiang_pos[self.shuaxin_wujiang_pos_idx][0] >500 < 1300:
            x0 = 1100
            x1 = 1300

        if  self.shuaxin_wujiang_pos[self.shuaxin_wujiang_pos_idx][0] >1300 \
                and self.shuaxin_wujiang_pos[self.shuaxin_wujiang_pos_idx][0] >500 < 1600:
            x0 = 1300
            x1 = 1600
        # 根据 x,y位置 来判断是否有钱购买


        tmp_cnt = 180
        confirm_cnt = 0
        while tmp_cnt > 1:
            meiqian_flag = 0
            youqian_flag = 0
            self.get_screen()


            name_youqian = 'youqian' + str(self.wujiang_renkou_delta)
            name_meiqian = 'meiqian' + str(self.wujiang_renkou_delta)
            if self.check(name_meiqian,x0,x1,y0,y1,threshold=0.97) :
                log.info("确实没钱")
                meiqian_flag = 1
                self.all_tiaozhan()

            if self.check(name_youqian,x0,x1,y0,y1,threshold=0.97) :
                log.debug("有钱")
                youqian_flag = 1

            if meiqian_flag == 0 and youqian_flag == 1:
                confirm_cnt = confirm_cnt + 1
            else:
                confirm_cnt = 0
            log.debug("有钱确认次数 confirm_cnt :%d",confirm_cnt)
            if confirm_cnt == 3 :
                break
            time.sleep(0.3)
            tmp_cnt = tmp_cnt - 1
        return tmp_cnt

    def check_more(self,name,loop_cnt=1):
        exist_shengji = 0
        for i in range(loop_cnt):
            if self.check(name,400, 1500, 600, 1080):
                exist_shengji = 1
                break
            # time.sleep(0.2)
            self.get_screen()
            self.yincang_D_pai()

        return exist_shengji

    def checkAndClick(self,name,x0=0,x1=1920,y0=0,y1=1080,t=0):
        if self.check(name,x0,x1,y0,y1):
            if name == "yincang":
                run_time = time.time()-self.start_time
                log.info("run_time:%d",run_time)
            self.click(t)
            return 1
        return 0

    def SystemInit(self):
        self.changeWindow() # 切换到游戏界面
        time.sleep(2)
        self.get_screen()

        if self.check("zuidahua", 1820, 1920, 0, 60):
            self.location_y = self.location_y + 20
            self.location_x = self.location_x + 30
            self.click()
        self.verifyCode()

    def Recovery(self):
        self.killM4DEAD() #先KILL掉 在运行

        self.location_x = 1919 # 最小化
        self.location_y = 1065
        self.click(2)
        self.checkAndClick("shoutabunengting")
        self.press('enter')     # 启动游戏
        time.sleep(120)
        self.location_x = 1609  # 按X
        self.location_y = 161
        self.click(1)
        self.location_x = 958   # 开始游戏
        self.location_y = 930
        self.click(20)
        if self.check("zuidahua", 1820, 1920, 0, 60):
            self.location_y = self.location_y + 20
            self.location_x = self.location_x + 30
            self.click()
        log.info("启动recovery 模式")
        self.verifyCode()

    def cur_phase_deinit(self):
        self.start_D_pai = 0
        self.refresh_cnt = 0
        self.yincang_D_pai()

    def all_tiaozhan(self):
        self.checkAndClick('jinbitiaozhan', 0, 200, 0, 270)
        self.checkAndClick('huntiaozhan', 0, 200, 0, 540)
        self.checkAndClick('shenzhuangtiaozhan', 0, 200, 270, 540)

        self.checkAndClick('xunbao',1920-300,1920,0,540)
        self.checkAndClick('huoquhun',1920-300,1920,0,540)
        self.checkAndClick('yincang', 400, 960, 540, self.screen_max_y)
        if self.check('wozhidaole', 0, 700, 700, 1080):
            self.location_y = self.location_y + 30
            self.click()


    def drag_zhuangbei(self,abs_pos):
        self.checkAndClick('yincang', 0, 960, 540, self.screen_max_y)

        self.location_x = 1250
        # self.location_x = 1375
        self.location_y = 550
        win32api.SetCursorPos((self.location_x, self.location_y))
        pyautogui.mouseDown() # 选中装备

        des_x = abs_pos[0]
        des_y = abs_pos[1]
        pyautogui.dragTo(des_x, des_y, 1.5, button='left')  # 按住鼠标左键，用0.5s将鼠标拖拽至1230，458
        pyautogui.mouseUp()

    def drag_wuqi(self,abs_pos):
        self.get_screen()
        self.checkAndClick('yincang', 0, 960, 540, self.screen_max_y)
        if self.check('wozhidaole', 0, 700, 700, 1080):
            self.location_y = self.location_y + 30
            self.click()
        win32api.SetCursorPos((self.location_x, self.location_y))
        pyautogui.mouseDown() # 选中装备
        time.sleep(0.3)
        des_x = abs_pos[0]
        des_y = abs_pos[1]
        pyautogui.dragTo(des_x, des_y, 2, button='left')  # 按住鼠标左键，用0.5s将鼠标拖拽至1230，458
        # pyautogui.mouseUp()
        time.sleep(0.5)
        self.get_screen()
        if self.check("chushouyingxiong", 100, 400, 800, 1000):
            self.yincang_D_pai()

    def wait_for_next_phase(self): # 当前阶段任务完成，等待魂够了升级下一次阶段，并打开D_PAI 标志
        timeout = 60

        while self.exit_game_flag == 0 and timeout > 0:
            self.recognize_hun_needed()
            self.recognize_hun()

            self.all_tiaozhan()
            if self.number_renkou_max >= 9:
                self.update_hun()
            tmp_renkou_max = self.recognize_renkou()
            if self.number_hun_max == 8 and self.number_renkou_max == (3+self.ziyuan) :
                self.battle_phase = 1
                log.debug("人口是合法的")
                break
            if self.number_hun_max == 12 and self.number_renkou_max == (4+self.ziyuan):
                self.battle_phase = 2
                log.debug("人口是合法的")
                break
            if self.number_hun_max == 16 and self.number_renkou_max == (5+self.ziyuan):
                self.battle_phase = 3
                log.debug("人口是合法的")
                break
            if self.number_hun_max == 22 and self.number_renkou_max == (7+self.ziyuan):
                self.battle_phase = 4
                log.debug("人口是合法的")
                break
            if self.number_hun_max == 30 and self.number_renkou_max == (9+self.ziyuan):
                self.battle_phase = 5
                log.debug("人口是合法的")
                break
            if self.number_hun_max == 50 and self.number_renkou_max == (11+self.ziyuan):
                self.battle_phase = 6
                log.debug("人口是合法的")
                break
            if self.number_hun_max == 60 and self.number_renkou_max == (13+self.ziyuan):
                self.battle_phase = 7
                log.debug("人口是合法的")
                break
            if self.number_hun_max == 66 and self.number_renkou_max == (15+self.ziyuan):
                self.battle_phase = 8
                log.debug("人口是合法的")
                break
            if self.number_hun_max == 72 and self.number_renkou_max == (17+self.ziyuan):
                self.battle_phase = 9
                log.debug("人口是合法的")
                break
            if self.number_hun_max == 80 and self.number_renkou_max == (19+self.ziyuan):
                self.battle_phase = 10
                log.debug("人口是合法的")
                break
            if self.number_renkou_max == 21:
                self.battle_phase = 11
                log.debug("人口是合法的")
                break
            if self.number_renkou_max == (21+self.ziyuan):
                self.battle_phase = 11
                log.debug("人口是合法的")
                break

            if self.number_hun_max == 16 and self.number_renkou_max == 4:
                self.battle_phase = 2
                log.debug("人口是合法的")
                break
            if self.number_hun_max == 20 and self.number_renkou_max == 5:
                self.battle_phase = 3
                log.debug("人口是合法的")
                break
            if self.number_hun_max == 28 and self.number_renkou_max == 7:
                self.battle_phase = 4
                log.debug("人口是合法的")
                break
            if self.number_hun_max == 34 and self.number_renkou_max == 9:
                self.battle_phase = 5
                log.debug("人口是合法的")
                break
            if self.number_hun_max == 40 and self.number_renkou_max == 11:
                self.battle_phase = 6
                log.debug("人口是合法的")
                break
            if self.number_hun_max == 50 and self.number_renkou_max == 13:
                self.battle_phase = 7
                log.debug("人口是合法的")
                break
            if self.number_hun_max == 56 and self.number_renkou_max == 15:
                self.battle_phase = 8
                log.debug("人口是合法的")
                break
            if self.number_hun_max == 60 and self.number_renkou_max == 17:
                self.battle_phase = 9
                log.debug("人口是合法的")
                break

            log.error("人口非法")
            timeout = timeout - 1
            self.judge_exit_game()

        if self.battle_phase <11:
            if self.number_hun > self.hun_needed * 5 + 10:
                log.info("升级所需魂够了,当前有魂:%d,所需:%d", self.number_hun, self.hun_needed * 5 + 10)
                tmp = self.hun_needed / 4 + 1
                self.update_renkou(int(tmp))

                time_out = 25   # 升级后一定要判断最大人口变没变
                while time_out > 1 and self.exit_game_flag == 0 :
                    self.recognize_renkou() # #变了才可以走下去
                    if tmp_renkou_max < self.number_renkou_max :
                        break
                    else:   #不变就给我乖乖等着 ，最大等待时间 25*2 秒
                        self.update_renkou(4)
                    time_out = time_out - 1
                self.battle_phase = self.battle_phase + 1  ##9阶段 17人口
                self.start_D_pai = 1
                self.checkAndClick('fanhui', 1700, 1920, 800, 1080, 1)

        if self.battle_phase == 11 :
            time_out = 25
            while time_out > 1 and self.exit_game_flag == 0 :     # 老是19人口升级21人口 卡
                self.recognize_renkou()
                if self.number_renkou_max == (21+self.ziyuan):
                    break
                time_out = time_out - 1
                self.update_hun(2)
                self.update_renkou(2)
                self.judge_exit_game()

        if self.number_renkou_max == (21+self.ziyuan):
            self.battle_phase = 11


    def killM4DEAD(self):
        try:
            pids = psutil.pids()
            for pid in pids:
                p = psutil.Process(pid)
                # get process name according to pid
                process_name = p.name()
                # kill process "sleep_test1"
                if 'M4DEAD.exe' == process_name:
                    print("kill specific process: name(%s)-pid(%s)" % (process_name, pid))
                    process = psutil.Process(pid)
                    process.terminate()
        except:
            log.error("kill M4 DEAD fail")

    def verifyCode(self):

        self.get_screen()
        if self.check("zaixianyanzheng") and self.verify_cnt < 100:
            log.info("在线验证")
            x0 = self.location_x - 250
            y0 = self.location_y + 100

            try:
                screen_raw = pyautogui.screenshot(region=[x0, y0, 320, 100])
                screen_raw.save("screenshot.png")
                log.info("保存验证码")
                # client = AipOcr("42731625", "v6FF9Gx1DAGlR5tRliDT78CH", "bTvGkdfehbgzyU1aP6b4mRChX2D10v6r") # gzz
                client = AipOcr(self.AppID, self.APIKey, self.SecretKey) # fei

                # 灰度
                gray = cv2.imread('screenshot.png', cv2.IMREAD_GRAYSCALE)
                cv2.imwrite('out.jpg', gray)
                with open('out.jpg', 'rb') as f:
                    content = f.read()
                    # 识别图片
                    #     result = client.accurate(content)
                    #     print(result)
                    result2 = client.basicAccurate(content)
                    log.info(result2)

                    tmp = result2['words_result']   ### # 刷洗数据
                    tmp = str(tmp).replace("{", '')
                    tmp = str(tmp).replace("}", '')
                    tmp = str(tmp).replace("'", '')
                    tmp = str(tmp).replace("words", '')
                    tmp = str(tmp).replace(":", '')
                    tmp = str(tmp).replace(" ", '')
                    tmp = str(tmp).replace("[", '')
                    tmp = str(tmp).replace("]", '')
                    tmp = str(tmp).replace(",", '') ### # 刷洗数据
                    # 1. 6* 8 , "6乘8"

                    # 找到乘以后 找出数据并计算
                    if '乘' in str(tmp):
                        tmp = tmp.split("乘")
                        data0 = self.transNumber(str(tmp[0]))
                        data1 = self.transNumber(str(tmp[1]))
                        result = int(data0) * int(data1)
                        log.info("验证码 :%d * %d = %d",data0,data1,result)

                    if '减' in str(tmp):
                        tmp = tmp.split("减")
                        data0 = self.transNumber(str(tmp[0]))
                        data1 = self.transNumber(str(tmp[1]))
                        result = int(data0) - int(data1)
                        log.info("验证码 :%d - %d = %d",data0,data1,result)

                    if '滅' in str(tmp):
                        tmp = tmp.split("滅")
                        data0 = self.transNumber(str(tmp[0]))
                        data1 = self.transNumber(str(tmp[1]))
                        result = int(data0) - int(data1)
                        log.info("验证码 :%d - %d = %d",data0,data1,result)

                    if '加' in str(tmp):
                        tmp = tmp.split("加")
                        data0 = self.transNumber(str(tmp[0]))
                        data1 = self.transNumber(str(tmp[1]))
                        log.info("data0,data1, %d,%d",data0,data1)
                        result = int(data0) + int(data1)

                        log.info("验证码 :%d + %d = %d",data0,data1,result)

                    if '除' in str(tmp):
                        tmp = tmp.split("除")
                        data0 = self.transNumber(str(tmp[0]))
                        data1 = self.transNumber(str(tmp[1]))
                        result = int(data0) / int(data1)
                        log.info("验证码 :%d / %d = %d",data0,data1,result)

                    ### 根据计算结果输入
                    baiwei = math.floor(result / 100)
                    shiwei = math.floor(result / 10)
                    gewei = result % 10


                    self.checkAndClick("shuru")
                    if baiwei != 0:
                        self.press(str(baiwei))
                        log.info("按下百位:%d",baiwei)
                    if baiwei == 0 and shiwei == 0:
                        log.info("只有个位，不按十位")
                    else:
                        self.press(str(shiwei))
                        log.info("按下十位:%d",shiwei)

                    self.press(str(gewei))
                    log.info("按下个位:%d", gewei)
                    self.verify_cnt = self.verify_cnt + 1

                    self.checkAndClick('queding')
                    self.checkAndClick('queding2')
            except:
                print("截图失败!")
                time.sleep(0.1)
        self.get_screen()

    def transNumber(self,str2):
        return_val = 0
        str_tmp = str(str2)
        if str_tmp == '零' or str_tmp == '0':
            return_val = 0
        if str_tmp == '壹' or str_tmp == '一' or str_tmp == '1':
            return_val = 1
        if str_tmp == '贰' or str_tmp == '二' or str_tmp == '2':
            return_val = 2
        if str_tmp == '叁' or str_tmp == '三' or str_tmp == '3':
            return_val = 3
        if str_tmp == '肆' or str_tmp == '四' or str_tmp == '4':
            return_val = 4
        if str_tmp == '伍' or str_tmp == '五' or str_tmp == '5':
            return_val = 5
        if str_tmp == '陆' or str_tmp == '六' or str_tmp == '6':
            return_val = 6
        if str_tmp == '柒' or str_tmp == '七' or str_tmp == '7':
            return_val = 7
        if str_tmp == '捌' or str_tmp == '八' or str_tmp == '8':
            return_val = 8
        if str_tmp == '玖' or str_tmp == '九' or str_tmp == '9':
            return_val = 9

        log.info("识别返回值 : %d",return_val)
        return return_val

    def judge_exit_game(self):


        self.get_screen()
        if self.check("yingxiongshengji", 0, 1920, 0, 270) \
                or self.check("jinbi") \
                or self.check("jinbi2") \
                or self.check("jingyanyaoji") \
                or self.check("guankajiangli", 0, 1920, 0, 540):
            self.location_x = 400
            self.location_y = 900
            for i in range(8):
                self.click()
            self.exit_game_flag = 1
        self.get_screen()

        if self.check("jixu") or self.check('jixu2'):
            self.click(2)
            self.exit_game_flag = 1

        if self.check("fanhuifangjian2"):
            self.click(2)
            time.sleep(10)
            self.get_screen()
            self.verifyCode()
            self.exit_game_flag = 1

    def init_xinyuan(self):

        self.checkAndClick("xinyuan",0,130,600,700)
        for i in range(len(self.xinyuan_list)):
            name = self.xinyuan_list[i]
            if name in self.lv1_list_raw:
                self.location_x = 1540  # 选择
                self.location_y = 322
                self.click()
                self.location_x = 1540  # 史诗
                self.location_y = 568
                self.click()
            if name in self.lv2_list_raw:
                self.location_x = 1540  # 选择
                self.location_y = 322
                self.click()
                self.location_x = 1540  # 史诗
                self.location_y = 515
                self.click()
            if name in self.lv3_list_raw:
                self.location_x = 1540  # 选择
                self.location_y = 322
                self.click()
                self.location_x = 1540  # 传说
                self.location_y = 468
                self.click()

            self.check_wujiang_xinyuan(name)


        self.yincang_D_pai()

    def share_zhuangbei(self):
        self.checkAndClick('yincang', 0, 960, 540, self.screen_max_y)
        self.checkAndClick('beibao', 1550, 1650, 900, 950)
        # self.checkAndClick('hechengronglian', 1500, 1700, 760, 900)
        # time.sleep(0.2)
        # for k in range(2):
        #     self.checkAndClick('yijianquanxuan')
        #     time.sleep(0.2)
        #     self.checkAndClick('hecheng')
        #     time.sleep(0.2)
        #     self.location_x = 1032  # 合完guanbi
        #     self.location_y = 686
        #     self.click(0.1)
        #
        #
        # self.location_x = 1529 #合完guanbi
        # self.location_y = 64
        # self.click(0.1)
        self.location_x = 68  # 点击分享
        self.location_y = 850
        self.click(0.1)
        for k in range(2):   #分享4次
            self.location_x = 1262
            self.location_y = 549
            self.click()
        self.yincang_D_pai() # 返回

    def parseConfig(self):

        with open('config.yml', 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        # 访问数据库配置信息
        lv1_list = config['database']['lv1_list']
        lv2_list = config['database']['lv2_list']
        lv3_list = config['database']['lv3_list']

        self.lv1_list = lv1_list
        self.lv2_list = lv2_list
        self.lv3_list = lv3_list
        self.battle_phase_lv1_list = []
        self.battle_phase_lv1_list.extend(self.lv3_list)
        self.battle_phase_lv1_list.extend(self.lv2_list)
        self.battle_phase_lv1_list.extend(self.lv1_list)

        self.dict_pos_default = config['database']['postion']

        self.xinyuan_list = config['database']['xinyuan_list']
        self.tequan = config['database']['tequan']
        self.ziyuan = config['database']['ziyuan']
        self.touxiang_en = config['database']['touxiang']


        self.refresh_cnt_max = config['database']['refresh_max']

        self.AppID = config['database']['AppID']
        self.APIKey = config['database']['APIKey']
        self.SecretKey = config['database']['SecretKey']

        self.qianghua_list = config['database']['qianghua_list']

        self.wujiang_wuqi = {}
        for i in range(len(self.wujiang_all_list)):
            self.wujiang_wuqi[self.wujiang_all_list[i]] = []


        for i in range(len(self.battle_phase_lv1_list)):
            try :
                tmp = self.battle_phase_lv1_list[i] + "_wuqi" # lishimin_wuqi
                self.wujiang_wuqi[self.battle_phase_lv1_list[i]] = config['database'][tmp]
                log.info("找到武将 %s 的武器:%s", self.battle_phase_lv1_list[i],self.wujiang_wuqi[self.battle_phase_lv1_list[i]])
            except:
                log.info("没有找到武将 %s 的武器",self.battle_phase_lv1_list[i])

    #     self.AppID
    # self.battle_phase_lv1_list


    def wuqi_process(self):
        self.yincang_D_pai()
        self.checkAndClick('beibao', 1550, 1650, 900, 950)
        time.sleep(0.2)
        drag_wuqi_flag = 0

        for wuqi_idx in range(1, 9, 1):

            self.get_screen()
            for i in range(len(self.wuqi)):
                wuqi_name = self.wuqi[i]
                # log.info("wuqi_idx:%d",wuqi_idx)
                if self.check_wuqi(wuqi_name, wuqi_idx, 0.98):  # 识别是什么装备
                    log.debug("识别到位置 %d, 装备 :%s", wuqi_idx, wuqi_name)
                    # wujiang_name = 'lishimin'
                    wuqi_name_list = self.battle_phase_lv1_list
                    for wujiang_name in wuqi_name_list:
                        if wujiang_name in self.lv1_list_raw:
                            extra_gezi = 0
                            gezi_limit = 3
                        if wujiang_name in self.lv2_list_raw:
                            extra_gezi = 1
                            gezi_limit = 4
                        if wujiang_name in self.lv3_list_raw:
                            extra_gezi = 2
                            gezi_limit = 6
                        wujiang_wuqi_list =  self.wujiang_wuqi[wujiang_name]

                        if (wuqi_name in wujiang_wuqi_list) and self.buy_cnt[wujiang_name] > 0:
                            gezishu = int(self.dict_lv[wujiang_name]) + extra_gezi
                            if gezishu > gezi_limit:
                                gezishu = gezi_limit
                            log.info("这是%s的装备,格子%d/%d", wujiang_name, self.dict_wuqi[wujiang_name], gezishu)

                            if self.dict_wuqi[wujiang_name] < gezishu:
                                tmp_pos_idx = int(self.dict_pos_use[wujiang_name])
                                log.info("tmp_pos_idx:%d", tmp_pos_idx)
                                log.info("self.abs_pos[tmp_pos_idx]:%s", self.abs_pos[tmp_pos_idx])
                                self.check_wuqi(wuqi_name, wuqi_idx, 0.98)
                                self.drag_wuqi(self.abs_pos[tmp_pos_idx])
                                self.dict_wuqi[wujiang_name] = self.dict_wuqi[wujiang_name] + 1
                                idx = wujiang_wuqi_list.index(wuqi_name)
                                wujiang_wuqi_list.pop(idx)
                                drag_wuqi_flag = 1
                                break
            if drag_wuqi_flag:
                break
        self.yincang_D_pai()
        return drag_wuqi_flag

    def yijianronghe_judge(self):
        self.yincang_D_pai()
        self.checkAndClick('beibao', 1550, 1650, 900, 950)
        time.sleep(0.5)

        for wuqi_idx in range(1, 9, 1):
            self.get_screen()
            for i in range(len(self.wuqi)):
                wuqi_name = self.wuqi[i]
                # log.info("wuqi_idx:%d",wuqi_idx)
                if self.check_wuqi(wuqi_name, wuqi_idx, 0.98):  # 识别是什么装备
                    log.debug("识别到位置 %d, 装备 :%s", wuqi_idx, wuqi_name)
                    # wujiang_name = 'lishimin'
                    wuqi_name_list = self.battle_phase_lv1_list
                    for wujiang_name in wuqi_name_list:

                        wujiang_wuqi_list =  self.wujiang_wuqi[wujiang_name]

                        if wuqi_name in wujiang_wuqi_list:
                            log.info("有大佬装备，不建议一键融合")
                            self.yincang_D_pai()

                            return 0

        self.yincang_D_pai()
        log.info("可以一键融合")
        return 1

    def yijianronghe(self):
        self.checkAndClick('yincang', 0, 960, 540, self.screen_max_y)
        self.yincang_D_pai()  # 返回
        self.checkAndClick('beibao', 1550, 1650, 900, 950)
        self.checkAndClick('hechengronglian', 1500, 1700, 760, 900)
        time.sleep(0.2)
        self.checkAndClick('yijianquanxuan')
        time.sleep(0.2)
        if self.checkAndClick('hecheng'):
            time.sleep(0.2)
            self.location_x = 1032  # 合完guanbi
            self.location_y = 686
            self.click(0.1)
        self.yincang_D_pai()  # 返回
        log.info("yijianronghe")

    def share_wujiang(self):
        if self.check('duiyouxuyao', 450, 1250, 0, 540, 0.98):
            if self.location_x > 450 and self.location_x < 750:
                self.location_x = 525
                self.location_y = 450
            if self.location_x > 750 and self.location_x < 1000:
                self.location_x = 802
                self.location_y = 450
            if self.location_x > 1000 and self.location_x < 1250:
                self.location_x = 1084
                self.location_y = 450
            self.click(5)

    def touxiang(self):
        self.yincang_D_pai()
        self.location_x = 1768
        self.location_y = 63
        self.click()
        self.location_x = 1078
        self.location_y = 913
        self.click()
        self.location_x = 885
        self.location_y = 648
        self.click()

    def expect_result(self):
        touxiang_cnt = 0

        while touxiang_cnt != 10:
            tequan_cnt = 0
            ziyuan_cnt = 0
            tequan_cnt = tequan_cnt + self.check("tequan_battle", 1370, 1480, 170, 240)
            tequan_cnt = tequan_cnt + self.check("tequan_battle", 1480, 1630, 170, 240)
            tequan_cnt = tequan_cnt + self.check("tequan_battle", 1630, 1750, 170, 240)
            tequan_cnt = tequan_cnt + self.check("tequan_battle", 1750, 1920, 170, 240)

            ziyuan_cnt = ziyuan_cnt + self.check("ziyuan_battle", 1370, 1480, 170, 240)
            ziyuan_cnt = ziyuan_cnt + self.check("ziyuan_battle", 1480, 1630, 170, 240)
            ziyuan_cnt = ziyuan_cnt + self.check("ziyuan_battle", 1630, 1750, 170, 240)
            ziyuan_cnt = ziyuan_cnt + self.check("ziyuan_battle", 1750, 1920, 170, 240)

            if tequan_cnt > 1 or ziyuan_cnt > 1:
                log.info("这场战斗可能可以到60波, tequan_cnt:%d,ziyuan_cnt:%d", tequan_cnt, ziyuan_cnt)
                return
            else:

                touxiang_cnt = touxiang_cnt + 1
                time.sleep(0.9)
                self.get_screen()

        if True:
            self.touxiang()
            self.touxiang_cnt = self.touxiang_cnt + 1
            log.info("这场战斗可能不可以到60波, tequan_cnt:%d,ziyuan_cnt:%d", tequan_cnt, ziyuan_cnt)

    def yincang_D_pai(self, loop=2):

        for i in range(loop):
            self.location_x = 1538
            self.location_y = 38
            self.click()  # 这里点一下隐藏购买武将界面

    def jinbichongneng(self):
        if self.check('jinbichongneng', 1700, 1800, 590, 650) or self.check('jinbichongneng2', 1700, 1800, 590, 650):
            self.jinbichongneng_state = 1
        else:
            self.location_x = 1800
            self.location_y = 550
            self.click()
            self.location_x = 1180
            self.location_y = 80
            self.click()
            self.location_x = 1300
            self.location_y = 650
            self.click()
            self.location_x = 1400
            self.location_y = 800
            self.click()
            self.jinbichongneng_state = 0
            self.yincang_D_pai()

    def xinyuan_process(self):
        xinyuan_list = self.battle_phase_lv1_list
        for i in range(len(xinyuan_list)):
            name = xinyuan_list[i]
            while self.check_wujiang_share(name):
                if self.buy_cnt[name] == 0 or \
                        (self.buy_cnt[name] > 0 and self.dict_lv[
                            name] < 5 and self.battle_phase >= 6):  # and self.battle_phase < 10 : # 只会购买一次
                    self.click()
                    self.yincang_D_pai()  # 万一一分享就取消 导致我点到武将上
                    if self.check_wujiang_bottom(name):  # 判断是否购买成功
                        self.buy_cnt[name] = self.buy_cnt[name] + 1
                        log.info("分享的 %s 购买成功", name)

                        self.wujiang_renkou_delta = 0
                        if name in self.lv1_list_raw:
                            self.wujiang_renkou_delta = 1
                        if name in self.lv2_list_raw:
                            self.wujiang_renkou_delta = 2
                        if name in self.lv3_list_raw:
                            self.wujiang_renkou_delta = 3
                        self.all_tiaozhan()

                        if self.check_more('shengji', 2):
                            self.dict_lv[name] = int(self.dict_lv[name]) + 1
                            log.info("武将 %s 升级了,当前等级:%s!", name, self.dict_lv[name])
                            self.click(1)
                            self.get_screen()
                            if self.check('shengji', 400, 1500, 600, 1080):
                                self.dict_lv[name] = int(self.dict_lv[name]) + 1
                                log.info("武将 %s 升级了,当前等级:%s!", name, self.dict_lv[name])
                                self.click()
                            continue
                        try:
                            tmp_pos_idx = self.dict_pos_use[name]
                            log.info("武将放置到 %s 位置", tmp_pos_idx)
                            log.info("ref_abs_pos_x:%d ,ref_abs_pos_y:%d", self.ref_abs_pos_x,
                                     self.ref_abs_pos_y)

                            self.drag_quick(self.abs_pos[int(tmp_pos_idx)])

                            timeout = 3
                            time.sleep(2)

                            while timeout:
                                self.get_screen()
                                self.all_tiaozhan()
                                self.get_screen()
                                if self.check_wujiang_bottom(name):
                                    self.drag_safe(self.abs_pos[int(tmp_pos_idx)])
                                    log.info("为什么会进来呢")

                                else:
                                    log.info('拖武将失败次数:%d', 3 - timeout)
                                    break
                                timeout = timeout - 1
                            self.renkou_cur = self.renkou_cur + self.wujiang_renkou_delta
                        except:
                            log.info("字典里没这个武将 按顺序从0摆放")
                        break
                else:
                    self.yincang_D_pai()
                    break