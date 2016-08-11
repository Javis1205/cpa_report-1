import sys
sys.path.append('Class/')
sys.path.append('Functions/')
sys.path.append('Config/')
import config
import gspread
from oauth2client.service_account import ServiceAccountCredentials
#
class GoogleSpeadSheet():
	def __init__(self, config_gs=config.config_info_gs):
		self.json_key = config_gs['gs_app_key_file_name']
		self.file_id = config_gs['file_id']
		self.Get_File()

	def Connect_GS(self, scope=['https://spreadsheets.google.com/feeds']):
		json_key = self.json_key
		credentials = ServiceAccountCredentials.from_json_keyfile_name(json_key, scope)
		google_credentials = gspread.authorize(credentials)
		return google_credentials

	def Get_File(self):
		gc = self.Connect_GS()
		file_id = self.file_id
		self.wsh = gc.open_by_key(file_id)

	def Get_Sheet(self, sheet_name):
		sh = self.wsh.worksheet(sheet_name)	
		return sh

	def Get_Value_Gs_By_Range(self, rg):
		if (not(rg)):
				return config.estore_id_list		

	def Get_Value(self, rg, sheet_name):
		sh = self.Get_Sheet(sheet_name)
		dt_range = sh.range(rg)
		return dt_range

	def Set_Value(self, raw_data, sheet_name, rg):
		row_ = len(raw_data) 
		col_ = 0
		if (row_ >= 1):
			col_ = len(raw_data[0])
		if (row_ >= 1 and col_ >= 1):
			sh = self.Get_Sheet(sheet_name)
			dt = sh.range(rg)
			i_start = 0
			i_end = col_	
			for x in range(row_):
				i_val = 0
				for y in range(i_start, i_end):
					dt[y].value = raw_data[x][i_val]
					i_val += 1
				i_start = i_end
				i_end = i_start + col_
			sh.update_cells(dt)
		else :
			return	
		
if __name__ == '__main__':
	list_ = [['a1','b1','c1'],['a2','b2','c2'],['d1','d2','d3']]
	gsp = GoogleSpeadSheet()
	print(gsp.Set_Value(list_))