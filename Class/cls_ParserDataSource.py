from abs_Parser import Parser
import sys
#
class ParserDataSource(Parser):
	#
	def __init__(self, config_ct):
		self.ct = config_ct
	
	def format_deco(func):
		def wrapper(*args, **kwargs):
			# TESTING WHEN SHOULD RUN DECO
			'''
			print(kwargs)
			print(args)
			return
			if not kwargs['deco']:
				return func(*args, **kwargs)
			'''
			
			format_input = args[-1]
			data = func(*args[0:-1], **kwargs)
			num = len(data)
			for i in range(len(data)):
				for j in range(len(data[i])):
					try:
						data[i][j] = data[i][j].format(format_input)
					except:
						pass
				format_input += 1
			return data
		return wrapper

	@format_deco
	def MegerData(self, data, deco=1):
		for x in range(len(data)):
			for y in range(len(self.ct)):
				data[x].append(self.ct[y])
		return data		
		

	def ProcessData(self, data, start_row):
		new_data = []
		for x in range(len(data)):
			for y in range(len(data[x])):
				list_dt = []
				for z in range(len(data[x][y])):
					list_dt.append(data[x][y][z])
				new_data.append(list_dt)	
		return self.MegerData(new_data, start_row)

		
	def ProcessCT(self):
		pass
	#
	

if __name__ == '__main__':
	pass
	'''
	data_ = [('1','2','4'),('2','3','5')]
	p = ParserDataSource(config.config_ct_range_ds)
	print(p.ProcessData(data_,2))
	'''
	
	