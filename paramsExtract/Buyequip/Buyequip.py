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
			[47, "水银之靴", 1100, [2,12]],
			[48, "考尔菲得的战锤", 1100, [8,8]],
			[49, "锯齿短匕", 1100, [8, 8]],
			[200, "探索者的护臂", 1100, [5, 5, 11]],
			[50, "紫雨林之拳", 1200, [8, 9]],
			[51, "狂热", 1200, [6, 10]],
			[52, "幽魂斗篷", 1200, [9, 12]],
			[53, "无用大棒", 1250, []],
			[54, "净蚀", 1250, [9, 8]],
			[55, "暴风之剑", 1300, []],
			[56, "水银饰带", 1300, [12]],
			[57, "海克斯饮魔刀", 1300, [12,8]],
			[58, "遗失的章节", 1300, [11, 11,7]],
			[59, "提亚马特", 1325, [8, 8, 4]],
			[60, "黑暗封印", 350, []],
			[61, "梅贾的窃魂书", 1400, [60]],
			[62, "最后的轻语", 1450, [8, 8]],
			[63, "幽魂面具", 1500, [9, 11]],
			[64, "比尔吉沃特弯刀", 1600, [28, 8]],
			[65, "湮灭宝珠", 1600, [9, 11]],
			[66, "救赎", 2100, [16, 22]],
			[67, "雅典娜的邪恶圣杯", 2100, [20, 32]],
			[68, "米凯尔的坩埚", 2100, [20, 22]],
			[69, "骑士之誓", 2200, [19, 21]],
			[70, "钢铁烈阳之匣", 2200, [46, 12]],
			[71, "舒瑞亚的狂想曲", 2250, [21, 26, 3]],
			[72, "基克的聚合", 2250, [46,31]],
			[73, "炙热香炉", 2300, [26, 22]],
			[74, "魔宗", 2400, [25, 27]],
			[75, "双生暗影", 2400, [32, 26]],
			[76, "海克斯科技原型腰带-01", 2500, [41, 21]],
			[77, "石像鬼板甲", 2500, [19, 17, 15]],
			[78, "时光之杖", 2600, [43, 24]],
			[79, "幻影之舞", 2600, [51, 10,6]],
			[80, "卢安娜的飓风", 2600, [51, 6, 6]],
			[81, "斯塔缇克电刃", 2600, [51, 14]],
			[82, "急射火炮", 2600, [51, 14]],
			[83, "瑞莱的冰晶节杖", 2600, [24, 9 ,12]],
			[84, "干扰水晶", 2650, [29, 21]],
			[85, "虚空之杖", 2650, [24, 12]],
			[86, "正义荣耀", 2650, [31, 16]],
			[87, "冰脉护手", 2700, [40, 31]],
			[88, "兹苔特的传送门", 2700, [29, 17]],
			[89, "日炎斗篷", 2750, [19, 35, 9]],
			[90, "守护天使", 2800, [55, 19, 15]],
			[91, "海克斯科技GLP-800", 2800, [58, 41]],
			[92, "凡性的提醒", 2800, [23, 62]],
			[93, "多米尼克领主的至意", 2800, [27, 62]],
			[94, "振奋盔甲", 2800, [52, 21]],
			[95, "适应性头盔", 2800, [52, 12, 4]],
			[96, "狂徒铠甲", 2850, [21, 36, 16]],
			[97, "荆棘之甲", 2900, [12, 38, 39]],
			[98, "智慧末刃", 2900, [37, 17, 6]],
			[99, "幽梦之魂", 2900, [48, 49]],
			[100, "兰顿之兆", 2900, [36, 39]],
			[101, "德拉克萨的幕刃", 2900, [48, 49]],
			[102, "中娅沙漏", 2900, [200, 15, 32 ]],
			[103, "亡者的板甲", 2900, [19,36]],
			[104, "缚法宝珠", 2900, [53, 26]],
			[105, "深渊面具", 3000, [43, 17]],
			[106, "黑色切割者", 3000, [54, 21]],
			[107, "女妖面纱", 3000, [32, 12, 24]],
			[108, "纳什之牙", 3000, [45,32]],
			[109, "莫雷洛秘典", 3000, [65, 24]],
			[110, "夜之锋刃", 3000, [27, 49, 12]],
			[111, "冰霜之锤", 3100, [50, 36]],
			[112, "岚切", 3100, [55, 14, 8]],
			[113, "鬼索的狂暴之刃", 3100, [11, 37, 27]],
			[114, "兰德里的折磨", 3100, [63, 24]],
			[115, "大天使之杖", 3200, [25, 58]],
			[116, "斯特拉克的挑战护手", 3200, [50, 27, 9]],
			[117, "巫妖之祸", 3200, [40, 26, 24]],
			[118, "卢登的回声", 3200, [58, 24]],
			[119, "马默提乌斯之噬", 3250, [57, 48]],
			[120, "饮血剑", 3300, [55, 8, 28]],
			[121, "破败王者之刃", 3300, [64, 31]],
			[122, "夺萃之镰", 3300, [55, 48, 18]],
			[123, "无尽之刃", 3400, [55, 27, 18]],
			[124, "水银弯刀", 3400, [56, 27, 28]],
			[125, "海克斯的科技枪刃", 3400, [64, 41]],
			[126, "朔极之矛", 3400, [55, 21,8]],
			[127, "贪欲九头蛇", 3500, [59, 28, 27]],
			[128, "巨型九头蛇", 3500, [59, 9, 50]],
			[129, "死亡之舞", 3500, [28, 27, 48]],
			[130, "灭世者的死亡之帽", 3600, [53, 53]],
			[131, "三相之力", 3500, [40, 45, 54]],
		]
		for i in EquipList:
			self.EquipList.append(BaseEquip(*i))
	def ReturnEquipName(self,Name=None,id=None,attr="pinyin"):
		"""通过id或者名字返回属性"""
		for i in self.EquipList:
			if i.id == id or i.name == Name:
				return getattr(i,attr)
	def ReturnInside(self,Name=None,id=None):
		"""通过id或者名字返回是否存在列表内"""
		for i in self.EquipList:
			if i.id == id or i.name == Name:
				return True
		return False
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
	def __init__(self,dm,FristBuyPriorty=3,DefaultEquips=None):
		"""这里只是声明变量，初始化在INIT内"""
		self.Number = 0
		self.INIT_Finished = False
		self.FBP = FristBuyPriorty
		self.EquipList = Equips()
		self.dm = dm
		if DefaultEquips:
			self.DefaultList = DefaultEquips
			if len(self.DefaultList) > 6:
				self.DefaultList = self.DefaultList[:6]
		else:
			self.DefaultList = ["123","饮血剑","夺萃之镰","三项之力","三相之力","三相之力"]
		self.DefaultList = list(map(self.EquipCheck,self.DefaultList))
		# 真实购买列表
		self.NowEquipList = []
	def EquipCheck(self,name):
		"""检查输入的装备是否都在列表内，不在列表用默认装备代替"""
		if not self.EquipList.ReturnInside(name):
			return "三相之力"
		return name
	def INIT(self):
		"""找到初始购买的位置，锚定购买坐标"""
		self.dm.start()
		time.sleep(0.1)
		self.open_shop()
		self.EnterEquipName("多兰之刃")
		time.sleep(1)
		self.find_pos()
		print("定位完成{}".format(str(self.pos)))
		self.Action_QuitShop()
	def CanBuyEquips(self,Money:int):
		"""通过传入的钱数来回传可购买的装备"""
		CanBuyList = []
		EM = self.EquipList.ReturnEquipName(self.DefaultList[self.Number])
		if Money >= EM:
			CanBuyList.append(self.DefaultList[self.Number])

	def EnterEquipName(self,Name:str):
		pinyin = self.EquipList.ReturnEquipName(Name)
		if pinyin:
			for i in pinyin:
				self.dm.KeyPressChar(i)
				time.sleep(0.1)

	def Action_QuitShop(self):
		time.sleep(0.5)
		self.dm.KeyPressChar("esc")

	def Action_Buy(self):
		# self.dm.MoveTo(*self.pos)
		# time.sleep(0.5)
		# self.dm.LeftClick()
		time.sleep(0.5)
		self.dm.MoveTo(*self.pos)
		time.sleep(0.5)
		self.dm.RightClick()

	def find_pos(self):
		self.dm.Capture(0, 0, 2000, 2000, r"C:\\Users\\Administrator\\Desktop\\123.jpg")
		pic = cv2.imread(r"C:\\Users\\Administrator\\Desktop\\123.jpg")
		img_gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
		template = cv2.imread(r"C:\\Users\\Administrator\\Desktop\\duolan.png", 0)
		res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		self.pos = tuple(map(lambda x: x + 25, max_loc))
		self.INIT_Finished = True

	def open_shop(self):
		"""打开商店"""
		self.dm.MoveTo(100,100)
		self.dm.LeftClick()
		time.sleep(0.5)
		self.dm.KeyPressChar("p")
		time.sleep(0.5)
		self.dm.KeyDownChar("ctrl")
		time.sleep(0.5)
		self.dm.KeyPressChar("l")
		time.sleep(0.5)
		self.dm.KeyUpChar("ctrl")

	def Buy(self,name):
		self.open_shop()
		self.EnterEquipName(name)
		self.Action_Buy()
		self.Action_QuitShop()

if __name__ == '__main__':
	import time
	dm = dm.MainCommucation()
	ww =Main(dm)
	print(ww.DefaultList)

