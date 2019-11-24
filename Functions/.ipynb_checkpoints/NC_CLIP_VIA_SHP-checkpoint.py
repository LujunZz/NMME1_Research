################################################################
# Scirpt_Name: NC_CLIP_VIA_SHP.py                              #
# Purpose: Subset a NetCDF file with a given Shapefile         #
# Original Programmer(S): wuxb                                 #
# Downloaded from: http://smallwave.github.io/blog/work/2015/  #
# 09/10/%E9%80%9A%E8%BF%87shaplefile%E8%A3%81%E5%89%AANetCDF   #
# modeifide by: Lujun Zhang @ U of Oklahoma 10/02/2019         #
# REVISION HISTORY                                             #
# 20150910 -- Initial version online                           #
# 20191005 -- Modified for Python3.6.5                         #
# 20191124 -- Last updated                                     #
################################################################
# Requie packages: Numpy, Pandas, necCDF4, osgeo, gdal         #
################################################################
import numpy as np
import numpy.ma as ma
import pandas as pd
import os  
import datetime
from netCDF4 import Dataset  
from osgeo import gdal, ogr

def NC_CLIP_VIA_SHP(NcFilePath,ShpFilePath,OutFilePath):
    strShpFilePath = ShpFilePath
    strNetCDFPathInput = NC
    #read shapefile
    shpDS = ogr.Open(strShpFilePath)
    shpLyr = shpDS.GetLayer()
    Envelop = shpLyr.GetExtent() 
    xmin,xmax,ymin,ymax = [np.round(Envelop[0]),
                           np.round(Envelop[1]),
                           np.round(Envelop[2]),
                           np.round(Envelop[3])]    #Your extents as given above
    mask_RES = []
    ######################################################
    #                      Process                       #
    ######################################################
    leadtime = 0
    EnsembleMember = 0
    ncInput  = Dataset(strNetCDFPathInput)
    var_name = list(ncInput.variables.keys())
    lon_Ori = getDimVar(ncInput,var_name,'X')
    lat_Ori = getDimVar(ncInput,var_name,'Y')
    reftime_Ori = getDimVar(ncInput,var_name,'S')
    #time = getDimVar(ncInput,varList,'time')
    name = 'prec'
    varData_Ori  =  getDataVar(ncInput,name)
    ######################################################
    #                    Create mask                     #
    ######################################################
    if len(mask_RES) == 0 :
        #get boundary and xs ys
        lat_bnds, lon_bnds = [ymin, ymax], [xmin+180, xmax+180]
        lat_inds = np.where((lat_Ori >= (lat_bnds[0])) & (lat_Ori <= lat_bnds[1]))
        lon_inds = np.where((lon_Ori >= (lon_bnds[0])) & (lon_Ori <= lon_bnds[1]))
        ncols = len(lon_inds[0])
        nrows = len(lat_inds[0])
        nreftime = len(reftime_Ori)
        #create geotransform
        xres = (xmax - xmin) / float(ncols)
        yres = (ymax - ymin) / float(nrows)
        geotransform = (xmin-3,xres,0,ymax,0,-yres)
        #create mask
        mask_DS = gdal.GetDriverByName('MEM').Create('', ncols, nrows, 1 ,gdal.GDT_Int32)
        mask_RB = mask_DS.GetRasterBand(1)
        mask_RB.Fill(0) #initialise raster with zeros
        mask_RB.SetNoDataValue(-32767)
        mask_DS.SetGeoTransform(geotransform)
        maskvalue = 1
        err = gdal.RasterizeLayer(mask_DS, [maskvalue], shpLyr)
        mask_DS.FlushCache()
        mask_array = mask_DS.GetRasterBand(1).ReadAsArray()    
        mask_RES = ma.masked_equal(mask_array, 255)          
        ma.set_fill_value(mask_RES, -32767)  
    ######################################################
    #                      Subset                        #
    ######################################################
    var_subset = varData_Ori[:,min(lat_inds[0])-1:max(lat_inds[0]), min(lon_inds[0])-1:max(lon_inds[0])]
    var_subset.__setmask__(np.logical_not(np.flipud(mask_RES.mask))) # update mask (flipud is reverse 180)
    #var_subset = var_subset.data
    lon_subset = lon_Ori[lon_inds]-180
    lat_subset = lat_Ori[lat_inds]
    ######################################################
    # Open a new NetCDF file to for data svaing. You can #
    # choose one of the formats from 'NETCDF3_CLASSIC',  #
    # 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'  #
    ######################################################
    # Using our previous dimension info, we can create the new time dimension
    # Even though we know the size, we are going to set the size to unknown
    OutputFileDirName = OutFilePath
    ncOutput = Dataset(OutputFileDirName, 'w', format='NETCDF4')

    #ncOutput.createDimension('time', None)
    ncOutput.createDimension('lon', ncols)
    ncOutput.createDimension('lat', nrows)
    ncOutput.createDimension('reftime', nreftime)

    # Add lat Variable
    var_out_lat = ncOutput.createVariable('lat','f',("lat"))
    ncOutput.variables['lat'][:] = lat_subset[:]

    # Add lon Variable
    var_out_lon = ncOutput.createVariable('lon','f',("lon"))
    ncOutput.variables['lon'][:] = lon_subset[:]

    # Add leadtime Variable
    var_out_reftime = ncOutput.createVariable('reftime','f',("reftime"))
    ncOutput.variables['reftime'][:] = reftime_Ori[:]

    # Add data Variable
    var_out_data = ncOutput.createVariable('Precip', 'f',("reftime","lat","lon"))
    for i in range(np.size(reftime_Ori)):
        ncOutput.variables['Precip'][i,:,:] = var_subset[i,:,:]

    # attr
    ncOutput.history = "CLIP Created datatime" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " by LujunZ at OU"
    ncOutput.source  = "netCDF4 under python 3.6.5"
    ######################################################
    #                   Write close                      #
    ######################################################
    ncOutput.close()  # close the new file
    print('Done')
    
    return

