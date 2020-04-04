#!/home/jmframe/programs/anaconda3/bin/python3
"""
Created on Thu February 19 2020
@author: Jonathan Frame
"""
import pandas as pd

def LOOK_UP_COORDS(basinID):
    cap = '/home/NearingLab/data/camels_attributes_v2.0/' #Camels attributes path (CAP)
    with open('/home/NearingLab/data/camels_attributes_v2.0/camels_all.txt') as f:
        attributes = pd.read_csv(f, sep=';', index_col='gauge_id')
    lat = attributes.loc[basinID,'gauge_lat']
    lon = attributes.loc[basinID,'gauge_lon']
    return [lat, lon]

def NLDAS_TXT_TO_NETCDF(basinID):
    # First thing to do is get the attributes, since at least some of this info is neccessary
    cap = '/home/NearingLab/data/camels_attributes_v2.0/' #Camels attributes path (CAP)
    with open('/home/NearingLab/data/camels_attributes_v2.0/camels_all.txt') as f:
        attributes = pd.read_csv(f, sep=';', index_col='gauge_id')
    latCatchment = attributes.loc[basinID,'gauge_lat']
    lonCatchment = attributes.loc[basinID,'gauge_lon']

    # initialize the NetCDF forcing data file.
    directory = '/home/NearingLab/projects/jmframe/CAMELS_synthData/forc/'
    forcingDataName = directory + basinID + 'forcing.nc'
    forcing = nc.Dataset(forcingDataName, 'w', format='NETCDF4_CLASSIC')
    forcing.title = basinID +' forcing'
    forcing.description = 'Forcing data for basin '+ basinID + ' in the CAMELS catchments'

    #BEGIN #######################################################################
    #BEGIN #  WRITE DATA TO THE NETCDF FORCING DATA FILE   #######################
    #BEGIN #######################################################################
    forcing.createDimension('lat', 1)
    forcing.createDimension('lon', 1)
    forcing.createDimension('time', UNLIMITED)
    ### createVareables in new data set
    forcing.createVariable('Prec', np.int32)
    forcing.variables['Prec'].units = 'mm'
    forcing.variables['Prec'].long_name = 'Precipitation'
    forcing.variables['prec']._FillValue = 1.e+20f
    forcing.variables['prec'].missing_value = 1.e+20f

    forcing.createVariable('Tmax', np.float32,('time',))
    forcing.variables['Tmax'].units = 'C'
    forcing.variables['Tmax']._FillValue = 1.e+20f
    forcing.variables['Tmax'].missing_value = 1.e+20f
    forcing.variables['Tmax'].longname = "Daily maximum temperature"
    
    forcing.createVariable('Tmin', np.float32,('time',))
    forcing.variables['Tmin'].units = 'C'
    forcing.variables['Tmin']._FillValue = 1.e+20f
    forcing.variables['Tmin'].missing_value = 1.e+20f
    forcing.variables['Tmin'].longname = "Daily minimum temperature"
    
    forcing.createVariable('latitude', np.float32, ('lat',))
    forcing.variables['latitude'].units = 'degrees_north'
    forcing.variables['latitude'].long_name = 'latitude'
    forcing.variables['latitude'].axis = 'Y'
    
    forcing.createVariable('longitude', np.float32, ('lon',))
    forcing.variables['longitude'].units = 'degrees-east'
    forcing.variables['longitude'].long_name = 'longitude'
    forcing.variables['longitude'].axis = 'X'
    
    forcing.createVariable('time', np.float64, ('time',))
    forcing.variables['time'].units = 'hours since 1900-01-01 00:00:00'
    forcing.variables['time'].long_name = 'Time axis'
    forcing.variables['time'].calendar = 'standard'






print('end script')
