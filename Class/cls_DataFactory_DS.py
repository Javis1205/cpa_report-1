import sys
sys.path.append('Config/')
import config
import cls_DataBase
from cls_ParserDataSource import ParserDataSource
import cls_Keeper
#
class DataFactoryDS():

	def __init__(self):
		self.conf = config
		
	def Create_DataSource(self):
		return cls_DataBase.DataBase(self.conf.config['database']['vg'])

	def Create_Parser(self):
		return ParserDataSource(self.conf.config_ct_range_ds)

	def Create_Keeper(self):
		return cls_Keeper.GSKeeper(self.conf)
