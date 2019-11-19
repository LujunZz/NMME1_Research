# This script is written for the purpose of retrieving data    #
# from NMME data portal.                                       #   
# ##############################################################
# Scirpt_Name: 0.DataRetriving.py                              #
# Sections: 1. Clipping NC dataset using shapefiles            #
#           2. Saving clipped & maksed .nc file at local disk  #
################################################################
# Section 1 modified from Wuxb's script from: github.io/blog   #
# /work/2015/09/10/%E9%80%9A%E8%BF%87shaplefile%E8%A3%81%E5%89 #
# %AANetCDF                                                    #
# Section 2  written by Lujun Zhang @ U of Oklahoma 10/02/2019 #
# REVISION HISTORY                                             #
# 20150910 -- Initial section one version online (Wuxb)        #
# 20191015 -- Modifed Section one by Lujun Zhang               #
# 20191105 -- Initial section two completed                    #
################################################################
# Requie packages:   Numpy, Pandas, necCDF4, osgeo, gdal       #
################################################################
import numpy as np
import numpy.ma as ma
import pandas as pd
import sys
import os  
import datetime
from netCDF4 import Dataset  
from osgeo import gdal, ogr
import matplotlib.pyplot as plt

NCInputBase = ['http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME/.CanCM4i/.FORECAST/.MONTHLY/.prec/dods',
               'http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME/.Cansips/.FORECAST/.MONTHLY/.prec/dods',
               'http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME/.CanSIPSv2/.FORECAST/.MONTHLY/.prec/dods',
               'http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME/.CMC1-CanCM3/.FORECAST/.MONTHLY/.prec/dods',
               'http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME/.CMC2-CanCM4/.FORECAST/.MONTHLY/.prec/dods',
               'http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME/.COLA-RSMAS-CCSM3/.MONTHLY/.prec/dods',
               'http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME/.COLA-RSMAS-CCSM4/.MONTHLY/.prec/dods',
               'http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME/.CPC-CMAP/.prate/dods',
               'http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME/.CPC-CMAP-URD/.prate/dods',
               'http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME/.CPC-PRECIP/.prate/dods',
               'http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME/.GEM-NEMO/.FORECAST/.MONTHLY/.prec/dods',
               'http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME/.GFDL-CM2p1/.MONTHLY/.prec/dods',
               'http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME/.GFDL-CM2p1-aer04/.MONTHLY/prec/dods',
               'http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME/.GFDL-CM2p5-FLOR-A06/.MONTHLY/.prec/dods',
               'http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME/.GFDL-CM2p5-FLOR-B01/.MONTHLY/.prec/dods',
               'http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME/.IRI-ECHAM4p5-AnomalyCoupled/.MONTHLY/.prec/dods',
               'http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME/.IRI-ECHAM4p5-DirectCoupled/.MONTHLY/.prec/dods',
               'http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME/.NASA-GEOSS2S/.FORECAST/.MONTHLY/.prec/dods',
               'http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME/.NASA-GMAO/.MONTHLY/.prec/dods',
               'http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME/.NASA-GMAO-062012/.MONTHLY/.prec/dods',
               'http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME/.NCAR-CESM1/.FORECAST/.MONTHLY/.prec/dods',
               'http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME/.NCEP-CFSv1/.MONTHLY/.prec/dods',
               'http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME/.NCEP-CFSv2/.FORECAST/.EARLY_MONTH_SAMPLES/.MONTHLY/.prec/dods']
ShpInputBase = ['C:/Users/Lujun/Desktop/ShapeFIle/CITY_SHP/CHICAGO_IL.shp',
                'C:/Users/Lujun/Desktop/ShapeFIle/CITY_SHP/DALLAS_TX.shp',
                'C:/Users/Lujun/Desktop/ShapeFIle/CITY_SHP/DENVER_CO.shp',
                'C:/Users/Lujun/Desktop/ShapeFIle/CITY_SHP/SIOUXFALL_SD.shp',
                'C:/Users/Lujun/Desktop/ShapeFIle/CITY_SHP/OKC_OK.shp',
                'C:/Users/Lujun/Desktop/ShapeFIle/CITY_SHP/LA_CA.shp',
                'C:/Users/Lujun/Desktop/ShapeFIle/CITY_SHP/ORLA_FL.shp',
                'C:/Users/Lujun/Desktop/ShapeFIle/CITY_SHP/PHIL_PA.shp',
                'C:/Users/Lujun/Desktop/ShapeFIle/CITY_SHP/SEA_WA.shp']
NMME_Member_Name = ['CanCM4i','Cansips','CanSIPSv2','CMC1-CanCM3',
                    'CMC1-CanCM4','COLA-RMSAS-CCSM3','COLA-RMSAS-CCSM4',
                    'CPC-CMAP','CPC-CMAP-URD','CPC-PRECIP','GEM-NEMO',
                    'GFDL-CM2p1','GDFL-CM2p1-aer04','GFDL-CM2P5-FLOR-A06',
                    'GFDL-CM2P5-FLOR-B01','IRI-ECHAM4p5-AnomalyCoupled',
                    'IIRI-ECHAM4p5-DirectCoupled','NASA-GEOSS2S','NASA-GMAO',
                    'NASA-GMAO-062012','NCAR-CESM1','NCEP-CFSv1','NCEP-CFSv2']
City_Name = ['Chicago','Dallas','Denver','Sioux_Fall','Oklahoma_City','Los_Angeles','Orlando','Philadaphia','Seattle']

