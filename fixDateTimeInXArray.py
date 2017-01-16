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
    prData = xy.open_dataset(oneFile,decode_cf=False) 
    lon = prData['lon_110']
    lat = prData['lat_110']
    prData = prData[field]
    prOneDay = xy.DataArray(prData, coords=[time,lat,lon],dims=['time','lat','lon'])
    return prOneDay

pr = xy.concat([getOneDay(oneFile) for oneFile in fileList], dim='time')
