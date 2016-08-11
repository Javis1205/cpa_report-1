from abc import ABCMeta, abstractmethod
class Datasource(metaclass=ABCMeta):
	def __init__(self, config_info_database):
		pass
	@abstractmethod
	def Query(self, sql):
		pass
	@abstractmethod
	def Fetch_All(self):
		pass
	@abstractmethod
	def Limited_Records(self, size):
		pass