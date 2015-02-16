
class SymTabEntry():
	def __init__(self,name):
		self.lines = []
		self.attr = {}
		self.name = name
	def appendLineNumber(self,nr):
		self.lines.append(nr)
	def setattr(self,name,value):
		self.attr[name] = value;
	def getattr(self,name):
		return self.attr[name];