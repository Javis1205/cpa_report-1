import mysql.connector as connector
from mysql.connector import Error
import re, time, argparse, datetime
import csv,json
import logging
import db_connect_config as config
import report_hard_code_data

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

# return a list of cursor and connector
def connect(config):
	try:
		cnx = connector.connect(buffered=True, use_unicode=True, charset="utf8", **config)
	except Exception as ex:
		print(ex)
		exit()
	cursor = cnx.cursor()	
	return [cnx,cursor] 	

	
def iter_row(cursor, size=100):
	while True:
		rows = cursor.fetchmany(size)
		if not rows:
			break
		for row in rows:
			yield row

def gotError(mesg=''):
	print('Got and error: {}'.format(mesg if mesg else 'No description for the error'))
	print('Exit')
	exit()

# the function can cause error 	
def addWhere(query, conditions):
	r = re.compile(r'WHERE', re.IGNORECASE)
	if r.search(query):
		i = query.index('WHERE')
		return (query[:(i+5)] + ' ('+ conditions +') AND' + query[(i+5):])
	else:
		return query + ' WHERE ' + conditions # NOTICE can cause error! 

# assume get heavy_start and heavy_end according to a range of numerical values	like between unix timestamps
def gotHeavyParam(target_attr, table, cond_attr, start_number, end_number):
	# connect to db 	
	cnx,cursor = connect(config.config_vg) # changable	
	query = 'SELECT MIN({0}), MAX({0}) FROM {1} WHERE {2} BETWEEN UNIX_TIMESTAMP("{3}") AND UNIX_TIMESTAMP("{4}")'.format(target_attr, table, cond_attr, start_number, end_number)

	try:
		cursor.execute(query)
		result = cursor.fetchall()
		
	except Exception as ex:
		print(ex)
		cnx.close()
		cursor.close()
		exit()
	else:
		cnx.close()
		cursor.close()	
		return result[0]

	
# set `heavy` as any positive number when querying more than 500 records at a time
# `heavy_attr` should be of type number, and be indexed. `heavy_start` and `heavy_end` is the min and max value of `heavy_attr`, being used to keep track a number of records being query at a time. statement `where heavy_attr between heavy_start and heavy_end` is used. 
# still works whell if query contain subquery and also contain `where` both in the subquery and outer query if it is the desired result		
# not allow to query `select *`
# only for select
# always save to a file with random name

def select_mh(query='', is_csv=1, is_json=0, fname='', heavy=1, heavy_attr='dummy', heavy_start=-1,heavy_end=-1, mesg='', title='', numQuery=1000):
	# test query
	
	r = re.compile(r'select \*', re.IGNORECASE)
	if r.search(query): 
		gotError('Not have permission to use "SELECT *"')
		
	# connect to db 	
	cnx,cursor = connect(config.config_vg) # changable

	# set up other variables
	count = 0
	
	# choose type of file for output


	if is_csv:
		if not fname:
			fname = report_hard_code_data.path+str(int(time.time())) + '_data.output'
		outfile = open(fname, 'a', newline='', encoding='utf-8') # changable
		writer = csv.writer(outfile, delimiter=' ')	
	elif is_json:
		gotError('Not support JSON yet. Choose csv instead')
	else:
		result_list = [] # store records into the list and return it at the end
	
	# check if query lots of records
	if heavy:
		logging.debug('In heavy mode')
		if heavy_start == -1 or heavy_end == -1 or heavy_attr == 'dummy':
			gotError('Have to assign heavy_start, heavy_end, and heavy_attr')
		
		heavy_curr_end = heavy_start + numQuery - 1# --------------------------------- changable
		if heavy_curr_end > heavy_end: heavy_curr_end = heavy_end
		stop = 0
				
		while heavy_curr_end <= heavy_end:
		
			logging.debug('heavy_curr_end: {}'.format(heavy_curr_end))
		
			try:
				conditions = '{} BETWEEN {} AND {}'.format(heavy_attr, heavy_start, heavy_curr_end)
				temp_query = addWhere(query, conditions)
				logging.debug('Query: {}'.format(temp_query))
			
				cursor.execute(temp_query)
				print('writing record ...')
				for row in iter_row(cursor):
					count += 1
					if is_csv:
						try:
							if count == 1:
								writer.writerow(title.split(','))
							writer.writerow(row)
						except Exception as ex:
							print(ex)
							gotError('Exception happen when writing to file csv')
						else:
							pass 
					elif is_json: gotError('Not support writing data to as JSON yet')
					else:
						print('Store record {} in a list ... '.format(count))
						result_list.append(row) 
					

			except Exception as ex:

				print(ex)
				gotError('Exception happen when execute query or write to file')
			else:
				if stop == 1:
					break
				heavy_start = heavy_curr_end + 1
				heavy_curr_end = heavy_start + numQuery - 1
				if heavy_start > heavy_end or stop == 1: break
				elif heavy_curr_end > heavy_end: 
					heavy_curr_end = heavy_end
					stop = 1

							
		logging.debug('Finish querying. Query {} rows'.format(count))
		
		
	else:
		logging.debug('In normal mode')
		
		cursor.execute(query)
		for row in iter_row(cursor):
			count += 1
			if is_csv: 
				print('writing record {} to file csv ...'.format(count))
				writer.writerow(row)
			elif is_json: gotError('Not support writing data to as JSON yet')
			else:
				print('Store record {} in a list ... '.format(count))
				result_list.append(row) 

	cursor.close()
	cnx.close()	
	if mesg:
		print(mesg)
	if is_json or is_csv: outfile.close()
	else:
		return result_list

def select_direct(query='', is_csv=0, fname= ''):
	return select_mh(query=query, is_csv=is_csv, fname=fname, heavy=0)	


if __name__ == '__main__':
 	query = 'select ord_id from orders_new where ord_date between unix_timestamp("2016-01-01") and unix_timestamp("2016-01-02")'
 	select_direct(query=query)	
		