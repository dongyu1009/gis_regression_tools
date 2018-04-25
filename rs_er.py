
# -*- encoding:utf-8 -*-
from __future__ import division
from scipy.stats import norm
from sklearn import linear_model


import osgeo.gdal as gdal
import numpy as np
import os
import copy

if __name__ == '__main__':
	mask_filename = "C:\\Users\\dongy\\Desktop\\gimms\\mask.tif"
	filenames = ["C:\\Users\\dongy\\Desktop\\gimms\\f1981.tif", 
				 "C:\\Users\\dongy\\Desktop\\gimms\\f1982.tif", 
				 "C:\\Users\\dongy\\Desktop\\gimms\\f1983.tif"]
	years = [[1990, 1991, 1992]]
	years = np.transpose(years)
	
	nodatavalue = -100
	
	model = linear_model.LinearRegression()
			
	ds_mask = gdal.Open(mask_filename) 
	im_width1 = ds_mask.RasterXSize
	im_height1 = ds_mask.RasterYSize
	# im_bands1 = ds_mask.RasterCount
	im_geotrans1 = ds_mask.GetGeoTransform()
	im_proj1 = ds_mask.GetProjection()
	im_mask = ds_mask.ReadAsArray(0,0,im_width1,im_height1)
	res = copy.deepcopy(im_mask).astype(np.float32)
	r_sqrt = copy.deepcopy(im_mask).astype(np.float32)
	del ds_mask 
	
	data = []
	for i in range(len(filenames)):
		filename = filenames[i]
		ds_data = gdal.Open(filename)
		im_data = ds_data.ReadAsArray(0,0,im_width1,im_height1)
		data.append(im_data)
		del ds_data 

	for i in range(im_height1):
		print i, " ", im_height1
		for j in range(im_width1):
			if im_mask[i][j] == 0:
				res[i][j] = nodatavalue
				r_sqrt[i][j] = nodatavalue
				continue
			sequence = []
			for k in range(len(data)):
				b1 = data[k][i][j]
				sequence.append(b1)
			model.fit(years, sequence)
			r_sqrt[i][j] = model.score(years, sequence)
			res[i][j] = model.coef_[0]

	ds_out = gdal.GetDriverByName("GTiff").Create("res.tif",im_width1,im_height1,1,gdal.GDT_Float32)
	ds_out.SetGeoTransform(im_geotrans1)
	ds_out.SetProjection(im_proj1)
	ds_out.GetRasterBand(1).WriteArray(res.astype(np.float32))
	ds_out.GetRasterBand(1).SetNoDataValue(nodatavalue)
	del ds_out
	
	ds_out = gdal.GetDriverByName("GTiff").Create("r_sqrt.tif",im_width1,im_height1,1,gdal.GDT_Float32)
	ds_out.SetGeoTransform(im_geotrans1)
	ds_out.SetProjection(im_proj1)
	ds_out.GetRasterBand(1).WriteArray(r_sqrt.astype(np.float32))
	ds_out.GetRasterBand(1).SetNoDataValue(nodatavalue)
	del ds_out
	
	print 'all done!'
