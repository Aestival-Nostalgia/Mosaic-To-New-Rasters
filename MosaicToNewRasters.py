import sys

sys.path.append(r'D:\Acedemic softs and apps\ArcGIS\Desktop10.2\arcpy')
sys.path.append(r'D:\Acedemic softs and apps\ArcGIS\Desktop10.2\bin')
sys.path.append(r'C:\Python27\ArcGIS10.2\Lib\site-packages')
sys.path
#以上是包的路径信息，替代了环境变量配置的功能

import arcpy
import os
import time
from tqdm import tqdm
from tqdm._tqdm import trange

reload(sys)
sys.setdefaultencoding('utf8')
#此处见：https://blog.csdn.net/Airy_/article/details/107118930 总之，Py2的诸多问题
 
#指定工作目录，即存放影像的目录
arcpy.env.workspace = r"G:\Bachelor_Degree_Thesis\DATA\LUCC_30m\2020"  #此处要修改！！！
 
#指定该工作空间下的一副影像为基础影像，为后面的参数提取做准备
base = "GLC_FCS30_2020_E85N35.tif"   #此处要修改！！！
 
#以下一段代码是为执行拼接做参数准备
out_coor_system = arcpy.Describe(base).spatialReference #获取坐标系统
dataType = arcpy.Describe(base).DataType 
piexl_type = arcpy.Describe(base).pixelType 
cellwidth = arcpy.Describe(base).meanCellWidth #获取栅格单元的的宽度
bandcount = arcpy.Describe(base).bandCount #获取bandCount
 
#打印一些信息
print("栅格影像的坐标系统是 %s" %out_coor_system.name)  
print("栅格影像的数据类型是 %s" %dataType)  
print("栅格影像的像素类型是 %s" %piexl_type)  
print("栅格影像的栅格单元宽度是 %s" %cellwidth)  
print("栅格影像的波段数是 %s" %bandcount)  
 
arcpy.CheckOutExtension("Spatial")
 
#提取待拼接影像的文件名，且中间以;隔开，例如：a.tif;b.tif;c.tif
rasters = []
for ras in arcpy.ListRasters("*.tif"):    #for循环，对wrokspace下的所有以dem.tif结尾的影像进行过滤
    rasters.append(ras)
 
ras_list = ";".join(rasters)              #字符串拼接
 
#打印出来，看看什么结果吧
print("预备进行镶嵌的栅格影像如下 %s" %ras_list)  

#指定输出文件夹
outFolder = r"G:\Bachelor_Degree_Thesis\DATA\LUCC_30m\Mosaic_Result"  
 
#执行拼接操作
arcpy.MosaicToNewRaster_management(ras_list, outFolder, "2020.tif", out_coor_system, "16_BIT_SIGNED", cellwidth, bandcount, "LAST", "FIRST")   #此处要修改！！！

#for i in tqdm(range(100)):
    #time.sleep(0.01)          #进度条捏（不好用）

#这个代码是基于ArcGIS 10.2 桌面版自带的ArcPy包的栅格批量镶嵌工具，可以将同一个文件夹下的栅格批量镶嵌，当然，栅格必须携带对应的坐标信息
#这个代码需要基于Py2 32bit的ArcPy环境，配置起来还是有点麻烦的，并且Py2已经基本上被淘汰，所以如非必要，不需要使用此代码
#在VS中，如果要使用调试功能，记得选定旧版的调试工具，否则无法调试！
#在按照时间序列进行合并时（逐年合并），基本上只需要修改三处，就可在短时间内大量按照年份合并出栅格影像，建议影像按照年份分配到不同的文件夹，而后再合并进入同一文件夹！

