import logging
import math

import time
from utils.log import log
import cv2 as cv
from utils.utils import UniverseUtils
from utils.battleList import  BattleList
import win32api
import pyautogui
from aip import AipOcr
from PIL import Image
import cv2 as cv2
class SimulatedUniverse(BattleList):
    def __init__(self,  gui=0):

        self.threshold = 0.99
        self.number_hun = 0
        self.number_money = 0
        self.number_renkou = 0
        super().__init__()
    def hezuo_init_single(self):
        while True:
            self.get_screen()
            if self.check("timeout"):
                self.location_x = 957
                self.location_y = 674
                self.click(1)

            if self.check("hezuomoshi"):
                self.click(0.5)
            if self.check("chuangjianfangjian"):
                self.click(0.5)
            if self.check("mima"):
                self.click(0.5)
                self.press("3")
                self.press("1")
            if self.check("chuangjian"):
                self.click(0.5)
            if self.check("kaishizhandou"):
                self.click(2)
                while True:
                    if self.check("shangdian",1700, 1920,400,600):
                        break
                    time.sleep(1)
                    self.get_screen()

                break
            time.sleep(1)


        print("hezuomoshi init finished")

    def hezuo_init_multi(self):
        log.info("开始初始化多人快速战斗")
        self.watchdog_s = time.time()
        while True:
            watchdog_time = time.time() - self.watchdog_s
            self.get_screen()
            if self.check("timeout"):
                self.location_x = 957
                self.location_y = 674
                self.click(1)
            self.checkAndClick('queren')
            self.verifyCode()
            if self.check("hezuomoshi"):

                log.info("self.battle_cnt:%d,self.qiwang_battle_cnt：%d",self.battle_cnt,self.qiwang_battle_cnt)
                if  self.battle_cnt != self.qiwang_battle_cnt:
                    self.checkAndClick("entrance_guaji",1500,1900,0,300)
                    # self.location_x = 1670
                    # self.location_y = 180
                    # self.click(0.3)
                    if  self.check("lingquguajijiangli"):
                        self.click(0.5)
                        self.click(0.5)
                        if self.check("shijianweidao"):
                            self.location_x = 964-747+self.location_x
                            self.location_y = 672-486+self.location_y
                            self.click()

                        self.location_x = 1520
                        self.location_y = 130
                        self.click(0.3)
                        self.qiwang_battle_cnt = self.battle_cnt
                        log.info("期望战斗次数 %d",self.qiwang_battle_cnt)

                self.check("hezuomoshi")
                self.click(0.3)
            if self.check("kuaisuzhandou"): # 快速战斗
                self.click(0.5)

            if self.check("quxiaozhunbei",1000,1920,540,1080):
                self.check("houtui", 0, 500, 0, 500)
                self.location_x = self.location_x + 20
                self.location_y = self.location_y + 20
                self.click(0.5)
            if self.check("queding"):
                self.click(0.2)
            if self.check("queding2"):
                self.click(0.2)
            if self.check("queren"):
                self.click()
            if self.check("kaishizhandou") or self.check("kaishizhandou2"):
                if self.check("queren"):
                    self.click()
                while self.check("houtui",0,500,0,500):
                    self.location_x = self.location_x + 25
                    self.location_y = self.location_y + 25
                    self.click(0.2)

                while self.check("houtui2",0,500,0,500):
                    self.location_x = self.location_x + 25
                    self.location_y = self.location_y + 25
                    self.click(0.2)
            if self.check("zhunbei"):
                self.click(0.5)
                self.time_cnt = 18  # 准备以后灯最多18秒，不开就换一个房间
                while self.time_cnt > 1:
                    if self.check("shangdian",1700, 1920,400,600):
                        break
                    if self.check("queren"):
                        self.click()
                    if self.check("kuaisuzhandou") or self.check("kaishizhandou2") or self.check("kaishizhandou"):
                        break
                    self.time_cnt = self.time_cnt - 1
                    time.sleep(1)
                    self.get_screen()
                if self.time_cnt == 1:
                    timeout = 15
                    while self.check("houtui", 0, 500, 0, 500):
                        self.location_x = self.location_x + 20
                        self.location_y = self.location_y + 20
                        self.click(0.5)
                        self.get_screen()
                        timeout = timeout - 1
                        if timeout == 1:
                            break
                    timeout = 15

                    while self.check("houtui2", 0, 500, 0, 500):
                        self.location_x = self.location_x + 25
                        self.location_y = self.location_y + 25
                        self.click(0.5)
                        timeout = timeout - 1
                        if timeout == 1:
                            break
            if self.check("shangdian", 1700, 1920, 400, 600):
                break
            if watchdog_time > 25*60:
                self.Recovery()
                self.SystemInit()
                self.watchdog_s = time.time()
                log.info("启动recovery 模式，看门狗没有喂狗")
            time.sleep(0.3)
        self.battle_cnt = self.battle_cnt + 1

        log.info("成功进入战斗,战斗次数 :%d",self.battle_cnt)

    def start(self):    # gzz
        self._stop = False

        self.parseConfig()

        while True: # 这才是大循环吧
            ## 这里是初始化代码 每盘游戏只需运行一次
           # self.hezuo_init_single()

            self.SystemInit()
            self.hezuo_init_multi() # 战斗初始化 能识别到商店 算成功进入

            self.ref_update()  # 进入游戏后 需要找个坐标基准，因为每次进入游戏 放置武将的位置会有一点不一样，所以需要找个基准，类似校准
            self.dragForMainDataInit() # 我觉得需要校准2次了 ，第一次根据基准来拖动
            self.ref_update()           #拖动后在进行一次校准


            self.main_data_init()
            self.init_xinyuan()  # 带验证

            while True:  # 每个周期 计算游戏该干嘛
                self.sub_data_init()
                if self.start_D_pai == 0 and self.exit_game_flag == 0: #1分55 升级D卡 4人口
                    self.wait_for_next_phase()

                if self.exit_game_flag == 1 :
                    break

                self.checkAndClick('queding2')# 这是啥
                self.all_tiaozhan()

                self.judge_exit_game()
                log.debug("是否可以D牌 %d",self.start_D_pai)
                if self.start_D_pai == 1 :
                    if (self.battle_phase == 1 and self.renkou_cur >= 2) \
                            or (self.battle_phase == 1 and self.refresh_cnt_max[self.battle_phase-1] == self.refresh_cnt) :
                            self.cur_phase_deinit() # 清零刷新次数, 停止D牌, 隐藏购买界面
                    if (self.battle_phase == 2 and self.renkou_cur >= 3 )\
                            or (self.battle_phase == 2 and self.refresh_cnt_max[self.battle_phase-1] == self.refresh_cnt):#2
                        self.cur_phase_deinit()  # 清零刷新次数, 停止D牌, 隐藏购买界面

                    if (self.battle_phase == 3 and self.renkou_cur >=4 ) \
                            or (self.battle_phase == 3 and self.refresh_cnt_max[self.battle_phase-1] == self.refresh_cnt):#3
                        self.cur_phase_deinit()  # 清零刷新次数, 停止D牌, 隐藏购买界面

                    if (self.battle_phase == 4 and self.renkou_cur >= 6) \
                            or (self.battle_phase == 4 and self.refresh_cnt_max[self.battle_phase-1] == self.refresh_cnt):#4
                        self.cur_phase_deinit()  # 清零刷新次数, 停止D牌, 隐藏购买界面
                        self.update_hun()

                    if self.battle_phase == 5 and self.renkou_cur >= 8\
                            or (self.battle_phase == 5 and self.refresh_cnt_max[self.battle_phase-1] == self.refresh_cnt):# 5阶段一起 9人口
                        self.cur_phase_deinit()  # 清零刷新次数, 停止D牌, 隐藏购买界面
                        self.update_hun(5)

                    if self.battle_phase == 6 and self.renkou_cur >= 10\
                            or (self.battle_phase == 6 and self.refresh_cnt_max[self.battle_phase-1] == self.refresh_cnt):# 6阶段一起 11人口
                        self.cur_phase_deinit()  # 清零刷新次数, 停止D牌, 隐藏购买界面
                        self.update_hun(5)

                    if self.battle_phase == 7 and self.renkou_cur >= 12\
                            or (self.battle_phase == 7 and self.refresh_cnt_max[self.battle_phase-1] == self.refresh_cnt): #7阶段 13人口
                        self.cur_phase_deinit()  # 清零刷新次数, 停止D牌, 隐藏购买界面
                        self.update_hun(3)

                    if self.battle_phase == 8 and self.renkou_cur >= 14\
                            or (self.battle_phase == 8 and self.refresh_cnt_max[self.battle_phase-1] == self.refresh_cnt): # 8阶段 15
                        self.cur_phase_deinit()  # 清零刷新次数, 停止D牌, 隐藏购买界面
                        self.update_hun(2)

                    if self.battle_phase == 9 and self.renkou_cur >= 15 and self.firstlook_huangjiang_cnt>=3:
                        self.cur_phase_deinit()  # 清零刷新次数, 停止D牌, 隐藏购买界面

                    if self.battle_phase == 10 and self.renkou_cur >= 18:
                        self.cur_phase_deinit()  # 清零刷新次数, 停止D牌, 隐藏购买界面

                    if self.battle_phase == 11:
                        if self.refresh_cnt % 7 == 0 : #and self.run_time < 30*60:
                            self.update_hun()
                        self.start_D_pai = 1
                        self.checkAndClick('fanhui', 1700, 1920, 800, 1080, 1)

                ## 心愿逻辑 gzz2
                xinyuan_list = self.battle_phase_lv1_list
                self.all_tiaozhan()
                for i in range(len(xinyuan_list)):
                    name = xinyuan_list[i]
                    while self.check_wujiang_share(name):
                        if self.buy_cnt[name] == 0 or \
                                (self.buy_cnt[name]>0 and self.dict_lv[name]<5): # and self.battle_phase>=10):# and self.battle_phase < 10 : # 只会购买一次
                            self.click()
                            self.yincang_D_pai()    # 万一一分享就取消 导致我点到武将上
                            if self.check_wujiang_bottom(name): # 判断是否购买成功
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



                                if self.check_more('shengji', 3):
                                    self.dict_lv[name] = int(self.dict_lv[name]) + 1
                                    log.info("武将 %s 升级了,当前等级:%s!", name, self.dict_lv[name])
                                    self.click()
                                    self.checkAndClick('yincang', 0, 960, 540, self.screen_max_y)
                                    continue
                                try:
                                    tmp_pos_idx = self.dict_pos_use[name]
                                    log.info("武将放置到 %s 位置", tmp_pos_idx)
                                    log.info("ref_abs_pos_x:%d ,ref_abs_pos_y:%d", self.ref_abs_pos_x,
                                             self.ref_abs_pos_y)

                                    self.drag(self.abs_pos[int(tmp_pos_idx)])

                                    timeout = 3
                                    time.sleep(2)

                                    while timeout:
                                        self.get_screen()
                                        self.all_tiaozhan()
                                        self.get_screen()
                                        if self.check_wujiang_bottom(name):
                                            self.drag(self.abs_pos[int(tmp_pos_idx)])
                                            log.info("为什么会进来呢")

                                        else:
                                            log.info('拖武将失败次数:%d', 3 - timeout)
                                            break
                                        timeout = timeout - 1

                                except:
                                    log.info("字典里没这个武将 按顺序从0摆放")
                                break
                        else:
                            break

                ## 刷新牌逻辑
                if self.start_D_pai == 1: ## 刷新牌逻辑
                    self.checkAndClick('fanhui', 1700, 1920, 800, 1080, 1)

                if self.check("shuaxin", 1700, 1920, 800, 1080) and self.start_D_pai == 1: ## 刷新牌逻辑 gzz3
                    self.click()

                    self.wujiang_recognize_cnt = 0
                    self.recognize_cnt_max = 20 # 7代表 识别最多7次三个武将，因为武将有时候会闪闪的，导致识别不正确
                    err_cnt = 0
                    while self.recognize_cnt_max >1: # 识别武将中
                        self.get_screen()
                        self.wujiang_recognize_cnt = 0
                        for i in range(len(self.wujiang_all_list)):
                            self.check_wujiang(self.wujiang_all_list[i],threshold=0.97)
                        if self.wujiang_recognize_cnt == (3+self.tequan):
                            break
                        else :
                            err_cnt = err_cnt+1
                        self.recognize_cnt_max = self.recognize_cnt_max-1
                        time.sleep(0.1)
                    # time.sleep(1)
                    log.info("匹配个数 %d",self.wujiang_recognize_cnt)
                    log.info(self.tequan)
                    if self.wujiang_recognize_cnt == (3+self.tequan) :
                        # 先备份上次识别成功的3个武将，2次刷新不可能相同，依靠这个来判断是否刷新成功
                        tmp=0
                        for i in range(3+self.tequan):
                            if self.shuaxin_wujiang_last[i] == self.shuaxin_wujiang[i]:
                                tmp = tmp + 1

                        if tmp != 3+self.tequan:
                            self.refresh_cnt = self.refresh_cnt + 1  # 每刷新一次就计数下
                        else:
                            continue
                        for i in range(3+self.tequan):
                            self.shuaxin_wujiang_last[i] = self.shuaxin_wujiang[i]
                        log.info("刷新成功次数 :%d", self.refresh_cnt)

                        #说明识别武将成功 ， 找个厉害的把他放上去干
                        try:
                            self.Find_Priority_wujiang() # 找到3个找白名单里最优先的武将
                            if self.name_readyToWork == 'NA': #这3个都不在白名单里
                                # 做点啥呢
                                continue
                            self.wujiang_recognize_cnt = 0 # 前面是能识别3个武将，能走到这里说明识别成功了
                                                           # 现在需要做的是，选中该武将
                                                           # 为了识别方便这里清一下 recognize_cnt 变量
                            name = self.name_readyToWork
                            try:
                                if  int(self.dict_lv[self.name_readyToWork]) == 5:
                                    log.info("武将 %s 已经5星了",self.name_readyToWork)
                                    continue

                            except:
                                print("dont care 没有这个武将的等级")

                            name = self.name_readyToWork
                            # 如果买的这个武将卡人口 先买 买完了 不拖动
                            self.wujiang_renkou_delta = 0
                            if name in self.lv1_list_raw:
                                self.wujiang_renkou_delta = 1
                            if name in self.lv2_list_raw:
                                self.wujiang_renkou_delta = 2
                            if name in self.lv3_list_raw:
                                self.wujiang_renkou_delta = 3


                            log.info("这个小伙子要去干活了 %s",name)
                            tmp = self.check_money()
                            if tmp < 2:
                                continue#超时购买就算了

                            log.info('有钱')
                            self.all_tiaozhan()

                            ########## 这里买武将
                            buy_max = 10
                            while buy_max > 1:
                                self.checkAndClick('yincang', 0, 960, 540, self.screen_max_y)


                                self.location_x = self.shuaxin_wujiang_pos[self.shuaxin_wujiang_pos_idx][0]
                                self.location_y = self.shuaxin_wujiang_pos[self.shuaxin_wujiang_pos_idx][1]
                                self.click(1)
                                log.info("x:%d,y:%d",self.location_x,self.location_y)
                                log.info("我买了 ")
                                if self.check_wujiang_bottom(name):
                                    log.debug("购买成功, buy_max :%d",buy_max)
                                    self.buy_cnt[name] = int(self.buy_cnt[name]) + 1
                                    break
                                else:
                                    log.debug("购买失败")
                                    buy_max = buy_max - 1
                            ########## 这里买武将


                            if self.check_more('shengji',3) :
                                self.dict_lv[name] = int(self.dict_lv[name]) + 1
                                log.info("武将 %s 升级了,当前等级:%s!", name, self.dict_lv[name])
                                self.click()
                                self.checkAndClick('yincang', 0, 960, 540, self.screen_max_y)
                                continue





                            #根据武将字典，放置对应位置，
                            try:
                                tmp_pos_idx = self.dict_pos_use[name]
                                log.info("武将放置到 %s 位置", tmp_pos_idx)
                                log.info("ref_abs_pos_x:%d ,ref_abs_pos_y:%d", self.ref_abs_pos_x,
                                         self.ref_abs_pos_y)


                                self.drag(self.abs_pos[int(tmp_pos_idx)])
                                timeout = 3
                                time.sleep(2)

                                while timeout:
                                    self.get_screen()
                                    self.all_tiaozhan()
                                    self.get_screen()
                                    if self.check_wujiang_bottom(name):
                                        self.drag(self.abs_pos[int(tmp_pos_idx)])
                                        log.info("为什么会进来呢")
                                      
                                    else:
                                        log.info('拖武将失败次数:%d',3-timeout)
                                        break
                                    timeout = timeout - 1

                            except:
                                log.info("字典里没这个武将 按顺序从0摆放")
                                tmp_pos_idx = self.four_huang_dage[self.pos_index_lv1]
                                log.info("lv1 drag")
                                self.drag(self.abs_pos[tmp_pos_idx])


                                timeout = 3
                                time.sleep(2)

                                while timeout:
                                    self.get_screen()
                                    self.all_tiaozhan()
                                    self.get_screen()
                                    if self.check_wujiang_bottom(name):
                                        self.drag(self.abs_pos[int(tmp_pos_idx)])
                                        log.info("为什么会进来呢")

                                    else:
                                        log.info('拖武将失败次数:%d', 3 - timeout)
                                        break
                                    timeout = timeout - 1
                                if self.pos_index_lv1 < 12 and name in self.lv1_list_raw:
                                    self.pos_index_lv1 = self.pos_index_lv1 +1
                                if self.pos_index_lv2 < 12 and name in self.lv2_list_raw:
                                    self.pos_index_lv2 = self.pos_index_lv2 +1
                                if self.pos_index_lv3 < 5 and name in self.lv3_list_raw:
                                    self.pos_index_lv3 = self.pos_index_lv3 +1
                                log.info("ref_abs_pos_x:%d ,ref_abs_pos_y:%d", self.ref_abs_pos_x,
                                         self.ref_abs_pos_y)
                                log.info("pos_index:%d ,abs_pos:%d,abs_pos:%d", tmp_pos_idx,
                                         self.abs_pos[tmp_pos_idx][0], self.abs_pos[tmp_pos_idx][1])
                            log.info("当前人口增加前:%d", self.renkou_cur)

                            self.renkou_cur = self.renkou_cur + self.wujiang_renkou_delta
                            #买好了的武将标记下

                            log.info("当前人口:%d",self.renkou_cur)
                                #

                        except ValueError:
                            print("item is not in this list")




                self.judge_exit_game()
                if self.check("fanhuifangjian2"):
                    self.click(2)
                    time.sleep(10)
                    self.get_screen()
                    self.verifyCode()
                    break

                watchdog_time = time.time() - self.watchdog_s
                if watchdog_time > 70 * 60:
                    self.Recovery()
                    self.SystemInit()
                    self.watchdog_s = time.time()




#1803~1808
def main():
    # su = BattleList()

    su = SimulatedUniverse(0)
    # su.getMousePos()
    su.start()





if __name__ == "__main__":
    main()
