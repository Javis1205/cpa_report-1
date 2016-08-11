from abs_DataSource import Datasource
import mysql.connector as connector
import requests

class DataBase(Datasource):
	def __init__(self, config_info_database):
		self.config = config_info_database

	def connect_database(self):
		try:
			cnx = connector.connect(buffered=True, use_unicode=True, **self.config)
		except Exception as ex:
			print(ex)
			exit()
		else: 
			self.conn = cnx
			self.cur = self.conn.cursor()

	def Query(self, sql):
		self.connect_database()
		self.cur.execute(sql)
		
	def Fetch_All(self, sql):
		self.Query(sql)
		rows = self.cur.fetchall()
		self.close_connect()
		return rows

	def close_connect(self):
		self.conn.close()
		self.cur.close()

	def Limited_Records(self, size = 100):
		while True:
			rows = self.cur.fetchmany(size)
			if not rows:
				break
			yield row
#
class DatabaseErp(Datasource):
	def __init__(self, config_info_database):
		self.config = config_info_database

	def connect_database(self):
		data = requests.get(self.config)
		return data
	def Query(self, sql):
		pass
		
	def Fetch_All(self, sql):
		pass

	def close_connect(self):
		pass

	def Limited_Records(self, size = 100):
		pass

