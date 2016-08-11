import sys
sys.path.append('Config/')
import config
import cls_DataBase
from cls_ParserDataSource import ParserDataSource
import cls_Keeper
#
class DataFactoryErp():

	def __init__(self):
		self.conf = config
		
	def Create_DataSource(self):
		return cls_DataBase.DatabaseErp('https://www.facebook.com/')#self.conf.config['database']['erp']['url'])

	def Create_Parser(self):
		pass
		# return ParserDataSource(self.conf.config_ct_range_ds)

	def Create_Keeper(self):
		pass
		# return cls_Keeper.GSKeeper(self.conf)
