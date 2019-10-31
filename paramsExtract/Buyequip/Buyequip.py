import cv2,time
import pypinyin as py
import dm.MainCommucation as dm
class BaseEquip:
	def __init__(self,id:int,name:str,needmoney:int,need_Equip:list):
		self.id = id
		self.name = name
		self.pinyin = py.slug(name, separator='')
		self.NeedMoney = needmoney
		if needmoney > 0 and needmoney <= 500:
			self.Priorty = 5
		elif needmoney > 500 and needmoney <= 1000:
			self.Priorty = 4
		elif needmoney > 1000 and needmoney <= 2000:
			self.Priorty = 3
		elif needmoney > 2000 and needmoney <= 3000:
			self.Priorty = 2
		elif needmoney > 3000:
			self.Priorty = 1
		self.need_Equip = need_Equip
class Equips:
	def __init__(self):
		#保存所有装备的列表
		self.EquipList = []
		EquipList = [
			[1, "多兰之刃", 450,[]],
			[2, "速度之靴", 300, []],
			[3, "仙女护符", 125, []],
			[4, "治疗宝珠", 150, []],
			[5, "布甲", 300, []],
			[6, "短剑", 300, []],
			[7, "蓝水晶", 350, []],
			[8, "长剑", 350, []],
			[9, "红水晶", 400, []],
			[10, "格斗手套", 400, []],
			[11, "增幅典籍", 435, []],
			[12, "抗魔斗篷", 450, []],
			[13, "多兰之盾", 400, []],
			[14, "基舍艾斯碎片", 600, [6]],
			[15, "秒表",600, []],
			[16, "晶体护腕", 650, [9,4]],
			[17, "负极斗篷", 720, [12]],
			[18, "灵巧披风", 800, []],
			[19, "锁子甲", 800, [5]],
			[20, "和谐圣杯", 800, [12,3,3]],
			[21, "燃烧宝石", 800, [9]],
			[22, "禁忌雕像", 800, [3,3]],
			[23, "死刑宣告", 800, [8]],
			[24, "爆裂魔杖", 850, []],
			[25, "女神之泪", 850, [7,3]],
			[26, "以太精魄", 850, [11]],
			[27, "十字镐", 875, []],
			[28, "吸血鬼节杖", 900, [8]],
			[29, "猛禽斗篷", 900, [4,5]],
			[30, "轻灵之靴", 900, [2]],
			[31, "冰川护甲", 900, [7,5]],
			[32, "恶魔法典", 900, [11]],
			[33, "疾行之靴", 900, [2]],
			[34, "明朗之靴", 900, [2]],
			[35, "班比的熔渣", 900, [9]],
			[36, "巨人腰带", 1000, [9]],
			[37, "反曲之弓", 1000, [6,6]],
			[38, "荆棘背心", 1000, [5, 5]],
			[39, "守望者铠甲", 1000, [5, 5]],
			[40, "耀光", 1050, [7]],
			[41, "海克斯科技左轮枪", 1050, [11,11]],
			[42, "狂战士胫甲", 1100, [2, 6]],
			[43, "万世催化石", 1100, [7, 9]],
			[44, "法师之靴", 1100, [2]],
			[45, "蜂刺", 1100, [6, 6]],
			[46, "军团圣盾", 1100, [6, 6]],

		]
		for i in EquipList:
			self.EquipList.append(BaseEquip(*i))
	def ReturnEquipName(self,id=None,Name=None):
		"""通过id或者名字返回名字"""
		for i in self.EquipList:
			if i.id == id or i.name == Name:
				return i.pinyin
class Main:
	"""
	FristBuyPriorty是关于大件小件的购买优先级，数值越低越优先攒钱购买大件
	0-500的装备优先级是5
	500-1000的装备优先级是4
	1000-2000的装备优先级是3
	2000-3000的装备优先级是2
	3000以上的装备优先级是1
	默认购买套装是[""]
	"""
	def __init__(self,dm,FristBuyPriorty=3):
		"""这里只是声明变量，初始化在INIT内"""
		self.INIT_Finished = False
		self.FBP = FristBuyPriorty
		self.EquipList = Equips()
		self.dm = dm
	def INIT(self):
		"""找到初始购买的位置，锚定购买坐标"""
		self.dm.start()
		time.sleep(5)
		self.open_shop()
		self.EnterEquipName("多兰之刃")
		time.sleep(1)
		self.find_pos()
		print("定位完成{}".format(str(self.pos)))
		self.Action_Buy()
		self.Action_QuitShop()
	def EnterEquipName(self,Name):
		pinyin = self.EquipList.ReturnEquipName(id,Name)
		if pinyin:
			for i in pinyin:
				self.dm.KeyPressChar(i)
				time.sleep(0.1)
	def Action_QuitShop(self):
		time.sleep(0.5)
		self.dm.KeyPressChar("esc")
	def Action_Buy(self):
		time.sleep(0.5)
		self.dm.MoveTo(*self.pos)
		self.dm.RightClick()
	def find_pos(self):
		self.dm.Capture(0, 0, 2000, 2000, r"C:\\Users\\Administrator\\Desktop\\123.jpg")
		pic = cv2.imread(r"C:\\Users\\Administrator\\Desktop\\123.jpg")
		img_gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
		template = cv2.imread(r"C:\\Users\\Administrator\\Desktop\\duolan.png", 0)
		res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		self.pos = tuple(map(lambda x: x + 50, max_loc))
		self.INIT_Finished = True
	def open_shop(self):
		"""打开商店"""
		self.dm.KeyPressChar("p")
		time.sleep(0.5)
		self.dm.KeyDownChar("ctrl")
		time.sleep(0.5)
		self.dm.KeyPressChar("l")
		time.sleep(0.5)
		self.dm.KeyUpChar("ctrl")
if __name__ == '__main__':
	import time
	dm = dm.MainCommucation()
	ww =Main(dm)
	ww.INIT()


