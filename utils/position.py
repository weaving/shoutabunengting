from utils.log import log
from utils.wujiang import WuJiang
import time

class MapPosition(WuJiang):
# class MapPosition():

    def __init__(self):



        self.dict_pos_default = {
            'muludawang': '0',
            'lishimin': '1',
            'liubang': '2',
            'xiaohe': '3',
            'hanxin': '4',
            'wuzetian': '5',
            'zhurongfuren':'6',

            'liubei': '7',
            'huangzhong':'8',
            'machao':'9',
            'niumowang': '10',

            'chenping': '30',
        }




        self.dict_pos_use = []

        self.dict_pos_delete_0 = [0,1,5]
        self.dict_pos_delete_use = []

        self.location_x = 0
        self.location_y = 0
        self.location_bottom_x = 0
        self.location_bottom_y = 0
        self.location_left_right = 0

        self.four_huang_dage = [0,1,2,3,4,7,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11,1,4,5,3,11]
        # self.four_huang_dage = self.dict_pos_delete_0
        self.any_lv1_pos = [6,7,8,9,10,11,11,11,11,11,11,11,11]
        self.any_lv2_pos = [2,3,4,29,28,27,26,25,4,4,4,]
        self.any_lv3_pos = [6,7,8,9,7,7,7,7,7,7,7,7,7]
        self.spec_lv3_pos = [2,3,4,4,4,4,]
        self.abs_pos = [[0 for j in range(2)] for i in range(40)]  # 位置信息
        self.shuaxin_wujiang_pos = [[0 for j in range(2)] for i in range(4)]  # 位置信息

        self.pos_occupied = [0 for i in range(40)]
        self.pos_index = 0  # 每放一个角色 移动一下这个值，方便下个武将放置
        self.ref_abs_pos_x = 0
        self.ref_abs_pos_y = 0
        self.ref_offset_x_right = 439
        self.ref_offset_y_right = 225

        self.ref_offset_x_left = 91
        self.ref_offset_y_left = 210


        self.left = 1
        self.right = 2
        self.left_right = 4


        super().__init__()
    def update_abs_pos(self, left_right):

        if left_right == self.right:



            self.abs_pos[0] = [1228,666]
            self.abs_pos[1] = [1357,666]
            self.abs_pos[2] = [1488,666]
            self.abs_pos[3] = [1509,767]
            self.abs_pos[4] = [1357,767]
            self.abs_pos[5] = [1228,767]
            self.abs_pos[6] = [1102,767]
            self.abs_pos[7] = [969,767]
            self.abs_pos[8] = [838,767]
            self.abs_pos[9] = [702,767]
            self.abs_pos[10] = [571,767]
            self.abs_pos[11] = [431,767]
            self.abs_pos[12] = [302,767]

            self.abs_pos[20] = [850,482]
            self.abs_pos[21] = [722,482]
            self.abs_pos[22] = [600,482]
            self.abs_pos[23] = [600,394]
            self.abs_pos[24] = [731,394]
            self.abs_pos[25] = [851,394]
            self.abs_pos[26] = [970,394]
            self.abs_pos[27] = [1086,394]
            self.abs_pos[28] = [1205,394]
            self.abs_pos[29] = [1319,394]
            self.abs_pos[30] = [1438,394]



        elif left_right == 1:
            self.abs_pos[0] = [636, 670]
            self.abs_pos[1] = [504, 670]
            self.abs_pos[2] = [378, 670]
            self.abs_pos[3] = [360, 767]
            self.abs_pos[4] = [492, 767]
            self.abs_pos[5] = [625, 767]
            self.abs_pos[6] = [764, 767]
            self.abs_pos[7] = [895, 767]
            self.abs_pos[8] = [1028, 767]
            self.abs_pos[9] = [1162, 767]
            self.abs_pos[10] = [1297, 767]
            self.abs_pos[11] = [1433, 767]

            self.abs_pos[20] = [1018,498]
            self.abs_pos[21] = [1144,498]
            self.abs_pos[22] = [1268,498]
            self.abs_pos[23] = [1257,407]
            self.abs_pos[24] = [1137,407]
            self.abs_pos[25] = [1017,407]
            self.abs_pos[26] = [898,407]
            self.abs_pos[27] = [780,407]
            self.abs_pos[28] = [663,407]
            self.abs_pos[29] = [550,407]
            self.abs_pos[30] = [433,407]

        elif left_right == 4:
            self.abs_pos[0] = [636, 670]
            self.abs_pos[1] = [504, 670]
            self.abs_pos[2] = [378, 670]
            self.abs_pos[3] = [360, 767]
            self.abs_pos[4] = [492, 767]
            self.abs_pos[5] = [625, 767]
            self.abs_pos[6] = [764, 767]
            self.abs_pos[7] = [895, 767]
            self.abs_pos[8] = [1028, 767]
            self.abs_pos[9] = [1162, 767]
            self.abs_pos[10] = [1297, 767]
            self.abs_pos[11] = [1433, 767]

            self.abs_pos[20] = [1018,498]
            self.abs_pos[21] = [1144,498]
            self.abs_pos[22] = [1268,498]
            self.abs_pos[23] = [1257,407]
            self.abs_pos[24] = [1137,407]
            self.abs_pos[25] = [1017,407]
            self.abs_pos[26] = [898,407]
            self.abs_pos[27] = [780,407]
            self.abs_pos[28] = [663,407]
            self.abs_pos[29] = [550,407]
            self.abs_pos[30] = [433,407]

    def ref_update(self):


        ref_updata_max = 40
        self.ref_update_flag = 0
        self.location_left_right = 0
        while self.ref_update_flag == 0:
            print("基准更新中")

            self.get_screen()
            if self.check("guanbi", 550, 750, 500, 900):
                self.location_x = self.location_x + 30
                self.location_y = self.location_y + 5
                self.click()

            if self.check("jizhun_right2", threshold=0.97) == 1 and self.ref_update_flag == 0:
                print(self.check("jizhun_right2", threshold=0.97))
                self.ref_abs_pos_x = self.location_x
                self.ref_abs_pos_y = self.location_y
                self.ref_update_flag = 1
                self.update_abs_pos(self.right)
                log.info("ref_abs_pos_x:%d ,ref_abs_pos_y:%d ", self.ref_abs_pos_x, self.ref_abs_pos_y)
                log.info("jizhun_right2")

                self.location_left_right = 2
                break
            if self.check("jizhun_left1", threshold=0.97) == 1 and self.ref_update_flag == 0:
                print(self.check("jizhun_left1", threshold=0.97))
                self.ref_abs_pos_x = self.location_x
                self.ref_abs_pos_y = self.location_y
                self.ref_update_flag = 1
                self.update_abs_pos(self.left)
                log.info("ref_abs_pos_x:%d ,ref_abs_pos_y:%d ", self.ref_abs_pos_x, self.ref_abs_pos_y)
                log.info("jizhun_left1")
                self.location_left_right = 1
                break
            if self.check("ditu_jizhun_4", threshold=0.97) == 1 and self.ref_update_flag == 0:
                print(self.check("ditu_jizhun_4", threshold=0.97))
                self.ref_abs_pos_x = self.location_x
                self.ref_abs_pos_y = self.location_y
                self.ref_update_flag = 1
                self.update_abs_pos(4)
                log.info("ref_abs_pos_x:%d ,ref_abs_pos_y:%d ", self.ref_abs_pos_x, self.ref_abs_pos_y)
                log.info("ditu_jizhun_4")
                self.location_left_right = 4
                break
            # if self.check("ditu_jizhun", threshold=0.95) == 1 and self.ref_update_flag == 0:
            #     print(self.check("ditu_jizhun", threshold=0.95))
            #     self.ref_abs_pos_x = self.location_x
            #     self.ref_abs_pos_y = self.location_y
            #     self.ref_update_flag = 1
            #     self.update_abs_pos()
            #     break
            time.sleep(0.5)
            self.yincang_D_pai(1)
            if ref_updata_max == 0:
                break
            ref_updata_max = ref_updata_max - 1

        # ref_abs_pos_x:464 ,ref_abs_pos_y:452 good



    def delete(self,pos_idx):  # 删除之前0-5的武将
        # 需要更新参数 self.renkou  self.pos_idx
        for j in range(3):
            self.get_screen()
            if self.check("yincang"):  # 我要买武将了么 你跑出来 我很烦
                self.click()
            if self.check('wozhidaole', 0, 700, 700, 1080):
                self.location_y = self.location_y + 30
                self.click()
            if self.check("guanbi", 550, 750, 500, 900):
                self.location_x = self.location_x + 30
                self.location_y = self.location_y + 5
                self.click()
                self.yincang_D_pai()
                if self.check("chushouyingxiong", 100, 400, 800, 1000):

                    self.yincang_D_pai()

            self.location_x = self.abs_pos[pos_idx][0]
            self.location_y = self.abs_pos[pos_idx][1]
            self.click(0.5)        # 点击
            log.info("self.location_x:%d",self.location_x)
            log.info("self.location_y:%d",self.location_y)
            #删除
            if self.check('wozhidaole', 0, 700, 700, 1080):
                self.location_y = self.location_y + 30
                self.click()
            if self.check("chushouyingxiong", 100, 400, 800, 1000):
                log.info("删除武将成功 位置 %d", pos_idx)
                self.click(0.5)
            else:
                log.info("武将不存在 或 删除失败")
              # 点击

            log.info("删除武将 位置 %d",pos_idx)
            break

    def delete_most(self):   #删除之前0-5的武将
                        # 需要更新参数 self.renkou  self.pos_idx
        self.yincang_D_pai()
        # for  j in range(2):
        for i in range(11):# 删10个英雄
            if i != 5  :  # 剃掉5 6
                for j in range(3): #删3次 确保稳定删除
                    tmp = self.delete(i)
                    if tmp == 0:
                        break

        self.renkou_cur = 3
        for i in range(len(self.lv2_list_raw)):
            self.dict_lv[self.lv2_list_raw[i]] = 1
        self.pos_index = 0

