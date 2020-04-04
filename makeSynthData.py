#!/home/jmframe/programs/anaconda3/bin/python3
"""
Created on Thu January 21 2020
@author: Jonathan Frame
"""
import numpy as np
import pandas as pd
import time
import datetime as dt
import sys
import os
import matplotlib.pyplot as plt

ymi = 'yearmonth' # Year month index
########################  Synthetic data generating parameters  #####################
PRECIP_PARAMETER1 = 0.75
PRECIP_PARAMETER2 = 0.25
########################  Synthetic data generating parameters  #####################

# Need to set print options to max for generating the results files.
np.set_printoptions(threshold=sys.maxsize)
#import matplotlib.pyplot as plt

# time the program
startProgramTime = time.time()

#Store all attributes. Really just need basin area, but the rest might come in handy.
att_path = "/home/NearingLab/data/camels_attributes_v2.0/camels_all.txt"
attributes = pd.read_csv(att_path, sep=";")
attributes.set_index('gauge_id', inplace=True)

#data directory path
df_path = "/home/NearingLab/projects/jmframe/CAMELS_synthData/nldas_forcing/"

# Setting nGauges to be one above the known number of gauges in CAMELS
nGauges = 673
count_id = 0

# Loop through all the files in the forcing data directory.
for filename in os.listdir(df_path):
    print(filename)
    startCatchmentTime = time.time()
    
    # the known location of the gauge ids in the files
    gauge_id = filename[0:8]
    
    # Confirm that there is a corresponding precipitation gauge to the discharge.
    if int(gauge_id) in attributes.index:
        catch_area = attributes.loc[int(gauge_id),'area_geospa_fabric'] # km^2
    else:
        print("gauge_id: " + gauge_id)
        print("WARNING::this catchment is not in the CAMELS attributes: ")
        print("Moving on to the next one...")
        continue

    dataF = pd.read_csv(df_path+filename,sep='\t| ',header=3, engine='python')

    # This loop has two purposes right now.
    # 1) to get some monthly ids for generating month statistics down the road
    # 2) for checking the data for missing values.
    badData=0   # a boolean to switch on if a value is bad.
    ym=[]       # ym=yearmonth, to be used for indexing values for monthly statistics
    ym_new=[]   # a set of uniqu ym values.
    for t in range(dataF.shape[0]):
        yearmonthasinteger=int(str(dataF.iloc[t,0])+str(dataF.iloc[t,1]).zfill(2))
        if yearmonthasinteger not in ym:
            ym_new.append(yearmonthasinteger)
        ym.append(yearmonthasinteger)

        for v in range(5,11):
            if dataF.iloc[t,v] < -990:
                print("gauge_id: " + gauge_id)
                print('bad data at time/variable',[t,v])
                badData += 1
    if badData == 0:
        print('All the data in this catchment looks good to go')
    else:
        print('bad values in the data =', badData)
    
    dataF.insert(4, ymi, ym)

    origColNames=list(dataF.columns)
    dataF.columns = dataF.columns.str.strip().str.lower().str.replace('/', '').str.replace('(', '').str.replace(')', '')
    forcingCol=list(dataF.columns)
    # Get the statistics for each month in the data record.
    dataFave = dataF.groupby(ymi, as_index=True).mean() # Forcing data averaged by yearmonth
    dataFmin = dataF.groupby(ymi, as_index=True).min()
    dataFmax = dataF.groupby(ymi, as_index=True).max()
    dataFstd = dataF.groupby(ymi, as_index=True).std()
    # Get the statistics for days in the month that it is raining.
    dataPave = dataF[dataF.prcpmmday > 1].groupby(ymi, as_index=True).mean()
    dataPmin = dataF[dataF.prcpmmday > 1].groupby(ymi, as_index=True).min()
    dataPmax = dataF[dataF.prcpmmday > 1].groupby(ymi, as_index=True).max()
    dataPstd = dataF[dataF.prcpmmday > 1].groupby(ymi, as_index=True).std()
    dataPsum = dataF[dataF.prcpmmday > 1].groupby(ymi, as_index=True).sum()
    # Get the statistics for days in the month that it is NOT raining.
    dataP0ave = dataF[dataF.prcpmmday == 0].groupby(ymi, as_index=True).mean()
    dataP0min = dataF[dataF.prcpmmday == 0].groupby(ymi, as_index=True).min()
    dataP0max = dataF[dataF.prcpmmday == 0].groupby(ymi, as_index=True).max()
    dataP0std = dataF[dataF.prcpmmday == 0].groupby(ymi, as_index=True).std()

    dataFcnt = dataF.groupby(ymi, as_index=True).count() # Number days in month
    dataPcnt = dataF[dataF.prcpmmday > 1].groupby(ymi, as_index=True).count() # Number of rain days

    # to get the percent of rainy days
    dataFcnt = pd.DataFrame(dataFcnt[forcingCol[0]]).rename(columns = {'year':'Ndays'})
    dataPcnt = pd.DataFrame(dataPcnt[forcingCol[0]]).rename(columns = {'year':'Rdays'})
    dataPsum = pd.DataFrame(dataPsum[forcingCol[6]]).rename(columns = {'prcpmmday':'prcpmmmonth'})

    # Neet to set the yearmonth as the index here, so it can be referenced by the larger data sets.
    # Some months have zero raining days, and got cut out. Put them back in with zero.
    for ym in dataFcnt.index.values:
        if ym not in dataPcnt.index.values:
            df_temp = pd.DataFrame({'Rdays':0}, index=[ym], columns=['Rdays'])
            dataPcnt = dataPcnt.append(df_temp, ignore_index=False, sort=True)
            df_temp = pd.DataFrame({'prcpmmmonth':0}, index=[ym], columns=['prcpmmmonth'])
            dataPsum = dataPsum.append(df_temp, ignore_index=False, sort=True)
            dataPave = dataPave.append(dataP0ave.loc[ym])
            dataPmin = dataPmin.append(dataP0min.loc[ym])
            dataPmax = dataPmax.append(dataP0max.loc[ym])
            dataPstd = dataPstd.append(dataP0std.loc[ym])

    dataPcnt['percentRainday'] = dataPcnt['Rdays']/np.maximum(1,dataFcnt['Ndays'])

    # Generate a synthetic record based on these statistics. 
    synthData = dataF.copy()
    for t in range(synthData.shape[0]):
        ym = int(synthData.iloc[t][ymi])
        # make the first values equal to the average. Since the calcs depend on the previous values.
        if t == 0:
            for v in range(5,11):
                synthData.iloc[t, v] = dataFave.loc[ym, forcingCol[v]]
        if t > 0:
            # Then go through and fill in all the values with the probabilistic values.
            p = dataPcnt.loc[ym, 'percentRainday']
            pwd = PRECIP_PARAMETER1 * p
            pww = PRECIP_PARAMETER2 + pwd
            a = dataPave.loc[ym, forcingCol[6]]
            s = dataPstd.loc[ym, forcingCol[6]]

            # Set the precipitation value. The chance of precip is higher if it rained the day before
            PmWm = dataPsum.loc[ym, 'prcpmmmonth']/np.maximum(1,dataPcnt.loc[ym,'Rdays'])
            x1 = np.maximum(0.1,-2.16+1.83*PmWm)
            x2 = np.maximum(1,PmWm/x1)

            # Check if it rained the day before, because the probability of rain today depends on yesterday.
            if synthData.iloc[t-1,6] == 0:
                if PRECIP_PARAMETER1 <= np.random.random_sample([1]):
                    synthData.iloc[t, 6] = np.random.gamma(x1,x2)
                else:
                    synthData.iloc[t, 6] = 0
            else:
                if PRECIP_PARAMETER2 <= np.random.random_sample([1]):
                    synthData.iloc[t, 6] = np.random.gamma(x1,x2)
                else:
                    synthData.iloc[t, 6] = 0

    plt.plot(synthData.iloc[:,6])
    plt.plot(dataF.iloc[:,6])
    plt.show()

    print("total time for this catchment:: ", time.time() - startCatchmentTime)
    exit()
print("total time for this program: ", time.time() - startProgramTime)



















