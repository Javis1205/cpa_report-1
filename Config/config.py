config = {
	'database': 
	{
		'vg':{
			'user':'vnpbi',
			'password':'sDm5pyyGe1BogrXo',
			'host':'192.168.90.205',
			'port':'33066',
			'database':'fs_hangnhat'
		},
		'erp':{
			'url': 'http://kiennn.erp.dev.nhanh.vn/api/crm/contract?page=1'
		},
		'fb':'',
		'g':''
	},
	'parser':'',
	'keeper':''
}
estore_id_list = [
	'1271175',
	'1034043',
	'2592421',
	'1172576',
	'3730674',
	'2564269',
	'4073953',
	'4206515',
	'2620801',
	'1385779',
	'3797110',
	'4231323',
	'4196266',
	'4231034',
	'2754039'
]
config_info_gs = {
	'gs_app_key_file_name': 'D:/Python/Project_VG/CPA_Report_Sale/Config/app_key.json',
	'app_auto_report_secret': '2681bdecbc7aee70f0e6f017705d1e20',
	'file_id':'10vEdwVuVdne2FlRhITOf1EHLOd3eHo1OC1n1IpMMCyk'
}

config_ct_range_ds = [
	'=IFERROR(VLOOKUP(C{0},\'DS GH\'!B:E,4,FALSE),"")',#'CSKH' : 
	'=DATE(LEFT(RIGHT(A{0},8),4),LEFT(RIGHT(A{0},4),2),RIGHT(A{0},2))',#'d' : 
	'=WEEKNUM(K{0},1)',#'w' : 
	'=MONTH(K{0})',#'m' : 
	'=IF(COUNTIFS($A$2:A{0},A{0})=1,1,0)',#'order_count' : 
	'=IFERROR(COUNTIF(\'DS GH\'!B:B,C{0}))',#'is_reg_estore' : 
	'=IFERROR(VLOOKUP(C{0},\'DS GH\'!B:I,8,FALSE),0)*G{0}'#'CPA' : 
]

gss_config = {
	'tab_config' : 'Config_pmh',
	'col_data': 'B1:B13',
	'tab_raw_data' : 11,
	'position_row_update': 12,
	'min_date':2
}