import sys
sys.path.append('Class/')
sys.path.append('Functions/')
sys.path.append('Config/')
import config
import convert_datetime, datetime, functions
import cls_DataFactory_DS, cls_AssemblyWorker, cls_GSS
def return_dict_data(sta_date, end_date):
	sql_update_data_fixed 	= """ SELECT MIN(ord_id), MAX(ord_id) FROM orders_new 
								WHERE ord_date BETWEEN {} 
								AND {} """.format(sta_date, end_date)
	max_min_ord_id_fixed	= Data.Fetch_All(sql_update_data_fixed) 	
	dic_return_fixed 		= {}
	list_ord_id 			= []
	for i in functions.my_range(max_min_ord_id_fixed[0][0], max_min_ord_id_fixed[0][1],1000):
		# get estore_id
		lm			= i + 1000 # limit
		if (lm > max_min_ord_id_fixed[0][1]):
			lm = max_min_ord_id_fixed[0][1]
		if(lm <= max_min_ord_id_fixed[0][1]):
			sql_get = """SELECT ord_id, ord_estore_id, ord_code, ord_date FROM orders_new
						WHERE ord_id BETWEEN {0} 
						AND {1} 
						AND ord_estore_id IN({2})""".format(i, lm,','.join(GSpS.Get_Value_Gs_By_Range('')))
			dic 	= Data.Fetch_All(sql_get)
			for j in range(len(dic)): 
				est_id 		= dic[j][1]
				list_ord_id.append(dic[j][0]);
				dic_return_fixed.update({'orders_product_{0}'.format(est_id % 20) : list_ord_id}) 
	list_fixed 				= []		
	for k in dic_return_fixed:
		# chuyển list sang string
		str_ord_id 		= ', '.join(str(e) for e in dic_return_fixed[k])
		# sql lấy ra thông tin của đơn hàng
		sql_info_order_fixed 	= """ SELECT ord_code, ord_phone, ord_estore_id, ord_status, pro_id, pro_category, op_price, op_quantity, onc_status, orr_source_referer FROM {0} 
									LEFT JOIN orders_new ON op_order_id = ord_id
									LEFT JOIN orders_new_checked ON ord_id = onc_order_id
									LEFT JOIN orders_referer ON ord_id = orr_order_id
									LEFT JOIN products_multi ON op_product_id = pro_id 
									WHERE op_order_id IN ({1}) """.format(k, str_ord_id)
		list_fixed.append(Data.Fetch_All(sql_info_order_fixed))		
	return list_fixed
#
def update_gs_data(data , sh_name, current_row):
	row		= len(data) 
	col		= 0
	if (row >= 1):
		col 	= len(data[0]) 

	max_cell_label = sh.get_addr_int(row + int(current_row) ,col)
	rg			= 'A{}:{}'.format(current_row, max_cell_label)
	GSpS.Set_Value(data, sh_name, rg)
#
def update_row_in_tab_config(row):
	range_update 	= 'B{}'.format(config.gss_config['position_row_update'] + 1)
	GSpS.Set_Value([[row]], config.gss_config['tab_config'], range_update)
#
# action
DF_DS 	= cls_DataFactory_DS.DataFactoryDS()
AW 		= cls_AssemblyWorker.AssemblyWorker(DF_DS)
AW.Perform()
Data 	= AW.DS 
gs 		= AW.Keeper
GSpS 	= gs.gss()
Parser 	= AW.Parser
# get position row insert
data_range 	= GSpS.Get_Value(config.gss_config['col_data'], config.gss_config['tab_config'])
sh_name 	= data_range[config.gss_config['tab_raw_data']].value
row_update 	= data_range[config.gss_config['position_row_update']].value
sh 			= GSpS.Get_Sheet(sh_name)
start_date 	= data_range[config.gss_config['min_date']].value #"01/05/2016"
int_start_date, int_first_day_of_month_ago, int_today, int_first_day_of_month_before  = functions.get_first_of_month(start_date, 15)
# 01/05/2016 , 01/8/2016, 16/8/2016, 16
if (int(row_update) == 2):
	list_data_fixed	= return_dict_data(int_start_date,(int_first_day_of_month_ago - (24 * 60 * 60)))

	# list_data_fixed = [
	# 	['dailyphukien_1503852_thang5_6','1262268262','1034043','5','406271','4036','85000','1','10','None'],
	# 	['dailyphukien_1503981_20160505','1627368583','1034043','5','4611197','5781','120000','1','10','None'],
	# 	['Senkai_1506240_20160507','913537661','1271175','100','5671877','15389','68000','3','15','None'],
	# 	['Senkai_1506283_20160507','913537661','1271175','5','5761211','15389','350000','1','10','None'],
	# 	['dailyphukien_1506415_20160507','903936012','1034043','5','1619215','464','450000','1','10','None'],
	# 	['dailyphukien_1507806_20160508','989942586','1034043','5','453464','5699','50000','1','10','None']
	# ]
	data_gs_fixed	= Parser.ProcessData(list_data_fixed,int(row_update))
	update_gs_data(data_gs_fixed,sh_name,int(row_update))
	row_update  		= int(row_update) + len(data_gs_fixed)
	update_row_in_tab_config(row_update)
# nếu ngày bằng 16
if (int(int_first_day_of_month_before) != 0):
	# cập nhật lại row update trên tab config = số hiện tại + số bản ghi trong tháng trc
	list_data_of_month_before	= return_dict_data(int_first_day_of_month_before, int_first_day_of_month_ago - (24 * 60 * 60))
	# list_data_of_month_before = [
	# 	['giadunggiarevn_1646262_thang7','1262268262','1034043','5','406271','4036','85000','1','10','None'],
	# 	['giadunggiarevn_1646262_20160724','1627368583','1034043','5','4611197','5781','120000','1','10','None'],
	# 	['myphamtrangnhung1_1646319_20160724','913537661','1271175','100','5671877','15389','68000','3','15','cm=noibo_cpa_nguyenhuong_giadungiare_5841719_dm_313x120'],
	# 	['Senkai_1506283_20160507','913537661','1271175','5','5761211','15389','350000','1','10','None'],
	# 	['dailyphukien_1646719_20160724','903936012','1034043','5','1619215','464','450000','1','10','None'],
	# 	['myphamtrangnhung1_1646319_20160724','989942586','1034043','5','453464','5699','50000','1','10','cm=noibo_cpa_nguyenhuong_giadungiare_5841719_dm_313x120']
	# ]
	data_gs_of_month_before		= Parser.ProcessData(list_data_of_month_before,int(row_update))
	update_gs_data(data_gs_of_month_before,sh_name,int(row_update))
	row_update  				= int(row_update) + len(data_gs_of_month_before)
	update_row_in_tab_config(row_update)
#
list_data	= return_dict_data(int_first_day_of_month_ago, int_today)
# list_data = [
# 	['verygoodvn_1679495_thang_8','1262268262','1034043','5','406271','4036','85000','1','10','None'],
# 	['giadunggiarevn_1646262_20160724','1627368583','1034043','5','4611197','5781','120000','1','10','None'],
# 	['myphamtrangnhung1_1646319_20160724','913537661','1271175','100','5671877','15389','68000','3','15','cm=noibo_cpa_nguyenhuong_giadungiare_5841719_dm_313x120'],
# 	['Senkai_1506283_20160507','913537661','1271175','5','5761211','15389','350000','1','10','None'],
# 	['dailyphukien_1646719_20160724','903936012','1034043','5','1619215','464','450000','1','10','None'],
# 	['dailyphukien_1646719_thang_9','903936012','1034043','5','1619215','464','450000','1','10','None'],
# 	['myphamtrangnhung1_1646319_20160724','989942586','1034043','5','453464','5699','50000','1','10','cm=noibo_cpa_nguyenhuong_giadungiare_5841719_dm_313x120']
# ]
data_gs		= Parser.ProcessData(list_data,int(row_update))
update_gs_data(list_data,sh_name,int(row_update))