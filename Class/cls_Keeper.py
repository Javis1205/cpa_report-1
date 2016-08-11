import sys
sys.path.append('Config/')
import config
from abc import ABCMeta, abstractmethod
import threading, time, logging, datetime, json
import gspread, cls_GSS
from oauth2client.service_account import ServiceAccountCredentials


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Keeper:
	def __init__(self,input):
		pass
		
	@abstractmethod	
	def insert_gs(self):
		pass
		
class GSKeeper(Keeper):
	def __init__(self, inp):
		self.config = inp
		
	def gss(self):
		return cls_GSS.GoogleSpeadSheet(self.config.config_info_gs)
		
class MEKeeper(Keeper):
	pass
	

# if __name__ == '__main__':
# 	input = {
# 		'fileId':'',
# 		'app_key_path':'',
		
# 	}