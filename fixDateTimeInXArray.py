import numpy as np
import scipy as sp
import xarray as xy
import pandas as pd
import string
import os.path
from copy import deepcopy

directoryData = ./ #put the directory path here
field = 'A_PCP_110_SFC_acc'
    
allFiles = os.listdir(directoryData)
fileList = []
for oneFile in allFiles:
    if oneFile.endswith(".nc") and ('daysum' in oneFile):
        fileList.append(''.join([directoryData,oneFile]))
fileList.sort()

#time data encoded is garbage, so replace it based on parsing the filename for year and day
def getOneDay(oneFile):
    fileStrings = str.split(oneFile,'.')
    year = int(fileStrings[1])
    dayOfYear = int(fileStrings[2])
    time = pd.datetime(year,1,1) + pd.DateOffset(days=dayOfYear-1) 
    time = [time]
    prData = xy.open_dataset(oneFile) 
    lon = deepcopy(prData['lon_110'])
    lat = deepcopy(prData['lat_110'])
    prOneDay = xy.DataArray(deepcopy(prData[field]), coords=[time,lat,lon],dims=['time','lat','lon'])
    prData.close()
    return prOneDay

pr = xy.concat([getOneDay(oneFile) for oneFile in fileList], dim='time')
