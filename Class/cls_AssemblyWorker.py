import abs_AssemblyWorker

class AssemblyWorker(abs_AssemblyWorker.Assembly):
	def __init__(self, factory):
		self.fact = factory

	def Perform(self):
		self.DS 		= self.fact.Create_DataSource()
		self.Parser 	= self.fact.Create_Parser() 
		self.Keeper		= self.fact.Create_Keeper()
	