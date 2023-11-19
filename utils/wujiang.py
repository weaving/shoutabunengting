from utils.utils import UniverseUtils

class WuJiang(UniverseUtils):
    def __init__(self):

        self.dict_lv = {}
        for i in range(len(self.wujiang_all_list)):
            self.dict_lv[self.wujiang_all_list[i]] = 1

        super().__init__()