import cv2,time
import pypinyin as py
import dm.MainCommucation as dm
class BaseEquip:
	def __init__(self,id:int,name:str,needmoney:int):
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
		print(self.name,self.pinyin)
class Equips:
	def __init__(self):
		#保存所有装备的列表
		self.EquipList = []
		EquipList = [
			[1,"多兰之刃",450]
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
	"""
	def __init__(self,dm,FristBuyPriorty=3):
		self.INIT_Finished = False
		self.FBP = FristBuyPriorty
		self.EquipList = Equips()
		self.dm = dm
		self.dm.start()
		time.sleep(10)
		self.INIT()
		self.Action_Buy()
	def INIT(self):
		"""找到初始购买的位置，锚定购买坐标"""
		self.open_shop()
		self.EnterEquipName(Name="多兰之刃")
		time.sleep(1)
		self.find_pos()
	def EnterEquipName(self,id=None,Name=None):
		pinyin = self.EquipList.ReturnEquipName(id,Name)
		print(pinyin)
		if pinyin:
			for i in pinyin:
				self.dm.KeyPressChar(i)
				time.sleep(0.1)
	def Action_Buy(self):
		time.sleep(1)
		print(self.dm.MoveTo(self.pos[0],self.pos[1]))
		time.sleep(0.5)
		print(self.dm.RightClick())
	def find_pos(self):
		ret = self.dm.Capture(0, 0, 2000, 2000, r"C:\\Users\\Administrator\\Desktop\\123.jpg")
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
	ww =Main()


