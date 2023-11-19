from utils.log import log
from utils.position import MapPosition
class BattleList(MapPosition):
    def __init__(self):

        ############# 所有武将的原始数据 不经常修改
        # LV1的 所有武将
        self.lv1_list_raw = ['huangyueying', 'shaseng', 'muludawang', 'zhubajie', 'machao', 'chenping', 'dayu',
                             'tieshangongzhu', 'liuchan', 'xuanwu', 'zhuque', 'liubei', 'sunshangxiang',
                             'niumowang', 'luban', 'liyuanfang', 'donghuangtaiyi', 'yuanshao', 'zhuangzhou',
                                                                     'diaochan', 'sunjian', 'gongsunzan', 'huangzhong', 'jinjiaodawang', 'yinjiaodawang',]

        self.lv2_list_raw = ['liubang', 'baihu', 'baiqi', 'dianmu', 'zhurongfuren', 'xiaohe', 'tangseng', 'qinglong', \
                             'baigujing', 'sunce', 'lvbuwei', 'sunquan', 'fanzeng', 'direnjie', 'lixin', 'zhangfei',
                             'honghaier', 'dongzhuo', 'leigong', 'simazhao']
        self.lv3_list_raw = ['nvwa', 'mozi', 'lishimin', 'zhouyu', 'zhugeliang', 'pangu', 'sunwukong', 'xiangyu',
                             'caocao', \
                             'zhaoyun', 'lvbu', 'hanxin', 'wuzetian', 'guanyu', 'simayi', 'daozu', 'change',
                             ]

        self.wujiang_all_list=[]
        self.wujiang_all_list.extend(self.lv1_list_raw)
        self.wujiang_all_list.extend(self.lv2_list_raw)
        self.wujiang_all_list.extend(self.lv3_list_raw)
        ############# 所有武将的原始数据 不经常修改

        ############# 战斗配置武将数据
        self.lv1_list = ['muludawang',  'niumowang', 'huangzhong', 'machao', 'chenping', ]
        self.lv1_list_final = ['muludawang',  'chenping', ]
        self.lv2_list = [ 'xiaohe', 'sunce', 'baiqi', 'liubang', 'zhurongfuren', ]
        self.lv2_list_final = ['xiaohe', 'liubang', ]
        self.lv3_list = ['nvwa', 'mozi', 'lishimin', 'zhouyu', 'zhugeliang', 'pangu', 'sunwukong', 'xiangyu',
                                      'zhaoyun', 'lvbu', 'hanxin', 'wuzetian', 'guanyu', ]
        self.lv3_list_final = [ 'lishimin', 'wuzetian','hanxin', ]

        self.lv1_dev_can_lvup = ['muludawang']
        self.list_final = [
            #LV3
            'nvwa', 'pangu', 'lishimin', 'wuzetian',
            #LV2
            # 'zhangfei', 'dongzhuo',
            #LV1
            'huangzhong', 'liubei', 'machao', 'donghuangtaiyi', 'dayu'
        ]
        self.list_qiangli_tibu = ['lishimin', 'wuzetian', 'nvwa', 'pangu', 'hanxin', 'daozu']

        self.four_huang_list = []

        self.battle_phase_lv1_list = []
        self.battle_phase_lv1_list.extend(self.lv3_list)
        self.battle_phase_lv1_list.extend(self.lv2_list)
        self.battle_phase_lv1_list.extend(self.lv1_list)

        self.battle_phase_lv2_list = self.battle_phase_lv1_list  # 4
        self.battle_phase_lv3_list = self.battle_phase_lv1_list  # 5

        self.battle_phase_lv4_list = self.battle_phase_lv1_list
        self.battle_phase_lv5_list = self.battle_phase_lv1_list
        self.battle_phase_lv6_list = self.battle_phase_lv1_list
        self.battle_phase_lv7_list = self.battle_phase_lv1_list
        self.battle_phase_lv8_list = self.battle_phase_lv1_list
        # self.battle_phase_lv9_list = self.list_final
        # self.battle_phase_lv10_list = self.list_final

        self.battle_phase_lv9_list = []
        self.battle_phase_lv9_list.extend(self.lv3_list)
        self.battle_phase_lv9_list.extend(self.lv2_list_final)
        self.battle_phase_lv9_list.extend(self.lv1_list_final)
        self.battle_phase_lv10_list = self.battle_phase_lv9_list
        self.battle_phase_lv11_list = self.battle_phase_lv9_list


        super().__init__()

