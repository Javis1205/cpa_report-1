import sys
sys.path.append('Class/')
sys.path.append('Functions/')
sys.path.append('Config/')
import convert_datetime, datetime, functions
import cls_DataFactory_Erp, cls_AssemblyWorker
#
DF = cls_DataFactory_Erp.DataFactoryErp()
AW = cls_AssemblyWorker.AssemblyWorker(DF)
AW.Perform()
data = AW.DS.connect_database()
if __name__ == '__main__':
	print(data)