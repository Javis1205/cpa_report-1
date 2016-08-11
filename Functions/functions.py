import convert_datetime, datetime
def my_range(start, end, step):
	while start <= end:
		yield start
		start += step
def get_first_of_month(day_start_from, num_day_ago):
	# string start date
	str_st_date 				= day_start_from # "01/05/2016"
	# convert string start date to start date type date 
	cv_str_st_date_to_type_date = convert_datetime.string_to_date(str_st_date, '%d/%m/%Y')
	# convert start date type date to type int
	int_start_date 				= int(convert_datetime.date_to_timestamp(cv_str_st_date_to_type_date))
	# today type date
	today 			= datetime.datetime.now()
	# get day
	day 			= today.strftime('%d')
	# convert today type date to type int
	int_today 		= int(convert_datetime.date_to_timestamp(today))
	# test
	# int_today 		= int_today + (7*24*60*60)
	# td 				= convert_datetime.timestamp_to_date(int_today)
	# day 				= td.strftime('%d')
	# 15 day ago
	day_ago 	= int_today - (int(num_day_ago) * 24 * 60 * 60)
	# if 15 day ago < start date then that day = start date
	if (day_ago < int_start_date):
		day_ago = int_start_date
	# convert day ago type int to type datetime
	type_date_day_ago 	= convert_datetime.timestamp_to_datetime(day_ago)
	# get month , year of day ago
	get_month  			= type_date_day_ago.strftime('%m')
	get_year  			= type_date_day_ago.strftime('%Y')
	# get start day of month day ago
	first_day_of_month	= '01/{}/{}'.format(get_month,get_year)
	# convert this first day to date
	date_first_day 		= convert_datetime.string_to_date(first_day_of_month, '%d/%m/%Y')
	# convert this first type date to type int
	int_first_day		= int(convert_datetime.date_to_timestamp(date_first_day))
	# nếu ngày = 16 
	# trả ra ngày 1 của tháng trước
	int_first_day_of_month_ago 					= 0
	if (int(day) == 16):
	# ngày cuối cùng của tháng trước
		last_day_of_month_ago 						= int_first_day - (24 * 60 * 60)
		# convert day ago type int to type datetime
		type_last_day_of_month_ago 					= convert_datetime.timestamp_to_datetime(last_day_of_month_ago)
		# get month , year of day ago
		get_month_last_day_of_month_ago  			= type_last_day_of_month_ago.strftime('%m')
		get_year_last_day_of_month_ago  			= type_last_day_of_month_ago.strftime('%Y')
		# get start day of month day ago
		first_day_of_month_ago						= '01/{}/{}'.format(get_month_last_day_of_month_ago,get_year_last_day_of_month_ago)
		# convert this first day to date
		date_first_day_of_month_ago					= convert_datetime.string_to_date(first_day_of_month_ago, '%d/%m/%Y')
		# convert this first type date to type int
		int_first_day_of_month_ago					= int(convert_datetime.date_to_timestamp(date_first_day_of_month_ago))
	#
	return int_start_date, int_first_day, int_today, int_first_day_of_month_ago
