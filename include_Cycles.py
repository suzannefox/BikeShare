# -*- coding: utf-8 -*-
"""
Created on Mon Dec  1 11:49:32 2014

@author: acjx602
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import os
import socket
#import statsmodels.api as sm
import pylab
from scipy import stats

printPlots = 'True'

def df_analysis(inDataFrame):
    icol=0
    meandatatypes=['float64','int64','float']
    df_dtypes = inDataFrame.dtypes

    df = pd.DataFrame(columns=['offset','colname','coltype',"IsNumeric",'Nan_Count','Valid_Count','Nan %','Total', \
                               'Min','Max','Mean','Std dev','Var'])

    for col in inDataFrame:
        df.loc[icol]=[icol, \
                      col, \
                      df_dtypes[col], \
                      False,
                      inDataFrame[col].isnull().sum(), \
                      inDataFrame[col].count(), \
                      0, \
                      0, \
                      0, \
                      0, \
                      0, \
                      0, \
                      0]
                      
        if df_dtypes[col] in meandatatypes: 
            df.ix[icol,"IsNumeric"]=True
            df.ix[icol,'Min']=inDataFrame[col].min()
            df.ix[icol,'Max']=inDataFrame[col].max()
            df.ix[icol,'Mean']=inDataFrame[col].mean()
            df.ix[icol,'Std dev']=inDataFrame[col].std()
            df.ix[icol,'Var']=inDataFrame[col].var()
            
        # Need to think about this bit some more
        #elif df_dtypes[col] in ['object']:
            #df.ix[icol,'Min']=inDataFrame[col].min()[0:3]
            #df.ix[icol,'Max']=inDataFrame[col].max()[0:3]

        icol+=1
        
    df['Total']=df['Nan_Count']+df['Valid_Count']
    df['Nan %']=(df['Nan_Count']/df['Total']) * 100
    return df


def analyse_Topline(data_path, cycle_file):
    cycles = pd.read_excel(data_path + cycle_file, 'Sheet1', index_col=None, na_values=['NA'])

#    print(pd.crosstab(cycles['Cycle#'], cycles['RainType'] , margins=True, aggfunc=[np.mean]))

    print("")
    print("Mean cycle Hires by Raintype (None,  Higher, Lower) among WorkDays and Holidays")
    print(pd.pivot_table(cycles, values=['Cycle#'], index=['DayType'], columns=['RainType'],aggfunc=np.mean, margins=True) )

    # Initial analysis
    print(cycles.head())
    print(cycles.shape)
    print("Pearson correlations for Cycle Hire/Weather data. Jan 2012-Sep 2014")
    print('')
    print(cycles.corr(method='pearson', min_periods=1))
    print(df_analysis(cycles))

    # DayType
    cyclesWork = cycles[cycles['DayType'] == 'Work']
    cyclesWorkDry = cyclesWork[cyclesWork['Rainfall'] > 0]
    print(cyclesWorkDry.corr(method='pearson', min_periods=1))

    return
    # Dry Days
    cyclesDry = cycles[cycles['Rainfall'] == 0]
    print("Pearson correlations for Cycle Hire/Weather data. Jan 2012-Sep 2014 - Dry Days")
    print('')
    print(cyclesDry.corr(method='pearson', min_periods=1))
    print(df_analysis(cycles))
    print("")
    print("ANALYSIS OF DRY DAYS")
    print(df_analysis(cyclesDry))

    # Wet Days
    cyclesWet = cycles[cycles['Rainfall'] > 0]
    print("Pearson correlations for Cycle Hire/Weather data. Jan 2012-Sep 2014 - Wet Days")
    print('')
    print(cyclesWet.corr(method='pearson', min_periods=1))
    print("")
    print("ANALYSIS OF WET DAYS")
    print(df_analysis(cyclesWet))

    cyclesWetLow = cyclesWet[cyclesWet['Rainfall'] <= 4.3]
    print("")
    print("LESS WET ",cyclesWetLow.shape)
    print(df_analysis(cyclesWetLow))
    
    cyclesWetHigh = cyclesWet[cyclesWet['Rainfall'] > 4.3]
    print("")
    print("MORE WET ",cyclesWetHigh.shape)
    print(df_analysis(cyclesWetHigh))


def analyse_WindSpeed(data_path, cycle_file):
    cycles = pd.read_excel(data_path + cycle_file, 'CycleData', index_col=None, na_values=['NA'])

    # DayType
    cyclesWork = cycles[cycles['DayType'] == 'Work']
    print(cyclesWork.shape)
    cyclesHols = cycles[cycles['DayType'] == 'Hols']
    print(cyclesHols.shape)
    
    # Temperature
    axes = ['WindSpeed','Cycle#']
    x = cyclesWork[axes[0]]
    y = cyclesWork[axes[1]]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    evaluatedLine = np.polyval([slope, intercept], y)

    plt.title('All Workdays - {0} vs {1}'.format(axes[0],axes[1]))
    plt.xlabel = axes[0]
    plt.ylabel = axes[1]
    plt.xlim([0,20])
    plt.ylim([0,50000])
    plt.scatter(x,y)
    if printPlots == 'True':  
        plt.show()
    print('All Workdays - {0} vs {1}'.format(axes[0],axes[1]))
    print("STATS : Slope {0}, R val {1}, P val {2}".format(slope, r_value, p_value))

    x = cyclesHols[axes[0]]
    y = cyclesHols[axes[1]]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    evaluatedLine = np.polyval([slope, intercept], y)

    plt.title('All Holidays - {0} vs {1}'.format(axes[0],axes[1]))
    plt.xlabel = axes[0]
    plt.ylabel = axes[1]
    plt.xlim([0,20])
    plt.ylim([0,50000])
    plt.scatter(x,y)
    if printPlots == 'True': 
        plt.show()
    print('All Holidays - {0} vs {1}'.format(axes[0],axes[1]))
    print("STATS : Slope {0}, R val {1}, P val {2}".format(slope, r_value, p_value))

def analyse_quartiles(data_path, cycle_file):
    cycles = pd.read_excel(data_path + cycle_file, 'CycleData', index_col=None, na_values=['NA'])

    # DayType
    cyclesWork = cycles[cycles['DayType'] == 'Work']
    print(cyclesWork.describe())
    quintile_bins = [1, 2, 3, 4]
    cyclesWork['Temp5'] = pd.qcut(cyclesWork['Temperature'],4, labels = quintile_bins)
    
    print("")
    print("Temp quartiles by humidy")
    print(pd.pivot_table(cyclesWork, values=['Cycle#'], index=['RainType'], columns=['Temp5'],aggfunc=np.mean, margins=True) )


def analyse_Temperature(data_path, cycle_file):
    cycles = pd.read_excel(data_path + cycle_file, 'CycleData', index_col=None, na_values=['NA'])

    # DayType
    cyclesWork = cycles[cycles['DayType'] == 'Work']
    print(cyclesWork.shape)
    cyclesHols = cycles[cycles['DayType'] == 'Hols']
    print(cyclesHols.shape)
    
    # Dry Days
    cyclesWorkDry = cyclesWork[cyclesWork['Rainfall'] == 0]
    print(cyclesWorkDry.shape)
    print(cyclesWorkDry.describe())
    cyclesHolsDry = cyclesHols[cyclesHols['Rainfall'] == 0]
    print(cyclesHolsDry.shape)

    # Wet Days
    cyclesWorkWet = cyclesWork[cyclesWork['Rainfall'] > 0]
    print(cyclesWorkWet.shape)
    cyclesHolsWet = cyclesHols[cyclesHols['Rainfall'] > 0]
    print(cyclesHolsWet.shape)

    # ===============================================================
    # Analyse cycle Hires by Dry Workdays
    # ===============================================================
    plt.plot(cyclesWorkDry['Cycle#'])
    plt.show()

    from sklearn import preprocessing
    tester = cyclesWorkDry['Cycle#']
    norm_tester = preprocessing.scale(tester)

    plt.hist(norm_tester, bins=10)
    plt.show()

    sm.qqplot(norm_tester, line='45')
    pylab.title("QQ Plot for Cycle")
    pylab.show()

    # Temperature & Dry days
    axes = ['Temperature','Cycle#']
    x = cyclesWorkDry[axes[0]]
    y = cyclesWorkDry[axes[1]]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    evaluatedLine = np.polyval([slope, intercept], y)

    plt.title('All Dry Workdays - {0} vs {1}'.format(axes[0],axes[1]))
    plt.xlabel = axes[0]
    plt.ylabel = axes[1]
    plt.xlim([-10,30])
    plt.ylim([5000,55000])
    plt.scatter(x,y)
    if printPlots == 'True': 
        plt.show()
    print('All Dry Workdays - {0} vs {1}'.format(axes[0],axes[1]))
    print("STATS : Slope {0}, R val {1}, P val {2}".format(slope, r_value, p_value))

    return
    # ===============================================================
    # Analyse temperature by Dry Workdays
    # ===============================================================
    plt.plot(cyclesWorkDry['Temperature'])
    plt.show()

    from sklearn import preprocessing
    tester = cyclesWorkDry['Temperature']
    norm_tester = preprocessing.scale(tester)

    plt.hist(norm_tester, bins=10)
    plt.show()

    sm.qqplot(norm_tester, line='45')
    pylab.title("QQ Plot for Temp")
    pylab.show()

    axes = ['Temperature','Cycle#']
    x = cyclesWorkDry[axes[0]]
    y = cyclesWorkDry[axes[1]]

    text1 = "Temperature"
    text2 = "Cycle Hire #"
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    evaluatedLine = np.polyval([slope, intercept], x)

    plt.figure(1)
    plt.title('Linear Regression - Using linregress\n {0} vs {1}\n'.format(text1, text2))
    plt.xlabel(text1)
    plt.ylabel(text2)
    plt.scatter(x , y, linewidth='1')    
    plt.xlim([-10,30])
    plt.ylim([5000,52000])
    plt.plot(y, evaluatedLine, 'k-')
    plt.show()
    print("STATS : Slope {0}, R val {1}".format(slope, r_value))
    print("")

    # ===============================================================
    # Analyse Windspeed by Dry Workdays
    # ===============================================================
    from sklearn import preprocessing
    tester = cyclesWorkDry['WindSpeed']
    norm_tester = preprocessing.scale(tester)

    plt.hist(norm_tester, bins=10)
    plt.show()

    sm.qqplot(norm_tester, line='45')
    pylab.title("QQ Plot for Wind")
    pylab.show()

    axes = ['WindSpeed','Cycle#']
    x = cyclesWorkDry[axes[0]]
    y = cyclesWorkDry[axes[1]]

    text1 = "WindSpeed"
    text2 = "Cycle Hire #"
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    evaluatedLine = np.polyval([slope, intercept], x)

    plt.figure(1)
    plt.title('Linear Regression - Using linregress\n {0} vs {1}\n'.format(text1, text2))
    plt.xlabel(text1)
    plt.ylabel(text2)
    plt.scatter(x , y, linewidth='1')    
    plt.xlim([0,15])
    plt.ylim([5000,52000])
    plt.plot(y, evaluatedLine, 'k-')
    plt.show()
    print("STATS : Slope {0}, R val {1}".format(slope, r_value))
    print("")


    # ===============================================================
    # Analyse Humidity by Dry Workdays
    # ===============================================================
    print ("")
    print ("HUMIDITY")
    print ("")
    from sklearn import preprocessing
    tester = cyclesWorkDry['Humidity']
    norm_tester = preprocessing.scale(tester)

    plt.hist(norm_tester, bins=10)
    plt.show()

    sm.qqplot(norm_tester, line='45')
    pylab.title("QQ Plot for Humid")
    pylab.show()

    axes = ['Humidity','Cycle#']
    x = cyclesWorkDry[axes[0]]
    y = cyclesWorkDry[axes[1]]

    text1 = "Humidity"
    text2 = "Cycle Hire #"
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    evaluatedLine = np.polyval([slope, intercept], x)

    plt.figure(1)
    plt.title('Linear Regression - Using linregress\n {0} vs {1}\n'.format(text1, text2))
    plt.xlabel(text1)
    plt.ylabel(text2)
    plt.scatter(x , y, linewidth='1')    
    plt.xlim([25,100])
    plt.ylim([5000,52000])
    plt.plot(y, evaluatedLine, 'k-')
    plt.show()
    print("STATS : Slope {0}, R val {1}".format(slope, r_value))
    print("")


    # ===============================================================
    # Analyse Humidity by Temperature for Dry Workdays
    # ===============================================================
    axes = ['Humidity','Temperature']
    x = cyclesWorkDry[axes[0]]
    y = cyclesWorkDry[axes[1]]

    text1 = "Humidity"
    text2 = "Temperature"
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    evaluatedLine = np.polyval([slope, intercept], x)

    plt.figure(1)
    plt.title('Linear Regression - Using linregress\n {0} vs {1}\n'.format(text1, text2))
    plt.xlabel(text1)
    plt.ylabel(text2)
    plt.scatter(x , y, linewidth='1')    
    plt.xlim([25,100])
    plt.ylim([-10,40])
    plt.plot(y, evaluatedLine, 'k-')
    plt.show()
    print("STATS : Slope {0}, R val {1}".format(slope, r_value))
    print("")

#    # Analyse temperature by Dry Workdays
#    axes = ['Temperature','Cycle#']
#    x = cyclesWorkDry[axes[0]]
#    y = cyclesWorkDry[axes[1]]
#    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
#    evaluatedLine = np.polyval([slope, intercept], y)
#
#    plt.figure(1)
#    plt.title('All Dry Workdays - {0} vs {1}'.format(axes[0],axes[1]))
#    plt.xlabel("Temperature")
##    plt.ylabel() = 'Cycle Hire #'
#    plt.xlim([-10,30])
#    plt.ylim([0,50000])
#    plt.scatter(x,y)
#    if printPlots == 'True': 
#        plt.show()
#    print("STATS : Slope {0}, R val {1}".format(slope, r_value))
#    print("")
    
    # outliers
#    cyclesWorkDryOut = cyclesWorkDry[cyclesWorkDry['Cycle#'] < 35000]
#    cyclesWorkDryOut = cyclesWorkDryOut[cyclesWorkDryOut['Temperature'] > 20]
#    print(cyclesWorkDryOut.shape)
#    print(cyclesWorkDryOut)

    return
    # Temperature
    axes = ['Temperature','Cycle#']
    x = cyclesWork[axes[0]]
    y = cyclesWork[axes[1]]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    evaluatedLine = np.polyval([slope, intercept], y)

    plt.title('All Workdays - {0} vs {1}'.format(axes[0],axes[1]))
    plt.xlabel = axes[0]
    plt.ylabel = axes[1]
    plt.xlim([-10,30])
    plt.ylim([0,50000])
    plt.scatter(x,y)
    if printPlots == 'True': 
        plt.show()
    print('All Workdays - {0} vs {1}'.format(axes[0],axes[1]))
    print("STATS : Slope {0}, R val {1}, P val {2}".format(slope, r_value, p_value))

    x = cyclesHols[axes[0]]
    y = cyclesHols[axes[1]]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    evaluatedLine = np.polyval([slope, intercept], y)

    plt.title('All Holidays - {0} vs {1}'.format(axes[0],axes[1]))
    plt.xlabel = axes[0]
    plt.ylabel = axes[1]
    plt.xlim([-10,30])
    plt.ylim([0,50000])
    plt.scatter(x,y)
    if printPlots == 'True': 
        plt.show()
    print('All Holidays - {0} vs {1}'.format(axes[0],axes[1]))
    print("STATS : Slope {0}, R val {1}, P val {2}".format(slope, r_value, p_value))

    # Temperature & Dry days
    axes = ['Temperature','Cycle#']
    x = cyclesWorkDry[axes[0]]
    y = cyclesWorkDry[axes[1]]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    evaluatedLine = np.polyval([slope, intercept], y)

    plt.title('All Dry Workdays - {0} vs {1}'.format(axes[0],axes[1]))
    plt.xlabel = axes[0]
    plt.ylabel = axes[1]
    plt.xlim([-10,30])
    plt.ylim([0,50000])
    plt.scatter(x,y)
    if printPlots == 'True': 
        plt.show()
    print('All Dry Workdays - {0} vs {1}'.format(axes[0],axes[1]))
    print("STATS : Slope {0}, R val {1}, P val {2}".format(slope, r_value, p_value))

    x = cyclesHolsDry[axes[0]]
    y = cyclesHolsDry[axes[1]]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    evaluatedLine = np.polyval([slope, intercept], y)

    plt.title('All Dry Holidays - {0} vs {1}'.format(axes[0],axes[1]))
    plt.xlabel = axes[0]
    plt.ylabel = axes[1]
    plt.xlim([-10,30])
    plt.ylim([0,50000])
    plt.scatter(x,y)
    if printPlots == 'True': 
        plt.show()
    print('All Dry Holidays - {0} vs {1}'.format(axes[0],axes[1]))
    print("STATS : Slope {0}, R val {1}, P val {2}".format(slope, r_value, p_value))

    # Temperature & Wet days
    axes = ['Temperature','Cycle#']
    x = cyclesWorkWet[axes[0]]
    y = cyclesWorkWet[axes[1]]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    evaluatedLine = np.polyval([slope, intercept], y)

    plt.title('All Wet Workdays - {0} vs {1}'.format(axes[0],axes[1]))
    plt.xlabel = axes[0]
    plt.ylabel = axes[1]
    plt.xlim([-10,30])
    plt.ylim([0,50000])
    plt.scatter(x,y)
    if printPlots == 'True': 
        plt.show()
    print('All Wet Workdays - {0} vs {1}'.format(axes[0],axes[1]))
    print("STATS : Slope {0}, R val {1}, P val {2}".format(slope, r_value, p_value))

    x = cyclesHolsWet[axes[0]]
    y = cyclesHolsWet[axes[1]]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    evaluatedLine = np.polyval([slope, intercept], y)

    plt.title('All Wet Holidays - {0} vs {1}'.format(axes[0],axes[1]))
    plt.xlabel = axes[0]
    plt.ylabel = axes[1]
    plt.xlim([-10,30])
    plt.ylim([0,50000])
    plt.scatter(x,y)
    if printPlots == 'True': 
        plt.show()
    print('All Wet Holidays - {0} vs {1}'.format(axes[0],axes[1]))
    print("STATS : Slope {0}, R val {1}, P val {2}".format(slope, r_value, p_value))

def analyse_Humidity(data_path, cycle_file):
    cycles = pd.read_excel(data_path + cycle_file, 'CycleData', index_col=None, na_values=['NA'])

    # DayType
    cyclesWork = cycles[cycles['DayType'] == 'Work']
    print(cyclesWork.shape)
    cyclesHols = cycles[cycles['DayType'] == 'Hols']
    print(cyclesHols.shape)

    cyclesWorkDry = cyclesWork[cyclesWork['Rainfall'] > 0]

    from sklearn import preprocessing
    tester = cyclesWorkDry['Cycle#']
    norm_tester = preprocessing.scale(tester)

    plt.hist(norm_tester, bins=10)
    plt.show()

    sm.qqplot(norm_tester, line='45')
    pylab.title("QQ Plot for Cycle")
    pylab.show()

    tester = cyclesWorkDry['Humidity']
    norm_tester = preprocessing.scale(tester)

    plt.hist(norm_tester, bins=10)
    plt.show()

    sm.qqplot(norm_tester, line='45')
    pylab.title("QQ Plot for Humid")
    pylab.show()
    
    # Humidity
    axes = ['Humidity','Cycle#']
    x = cyclesWorkDry[axes[0]]
    y = cyclesWorkDry[axes[1]]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    evaluatedLine = np.polyval([slope, intercept], y)

    plt.title('All Dry Workdays - {0} vs {1}'.format(axes[0],axes[1]))
#    plt.xtitle('Humidity')
#    plt.ytitle('Cycle#')
    plt.xlim([40,100])
    plt.ylim([5000,55000])
    plt.scatter(x,y)
    plt.plot(y, evaluatedLine, 'k-')
    if printPlots == 'True': 
        plt.show()
    print('All Dry Workdays - {0} vs {1}'.format(axes[0],axes[1]))
    print("STATS : Slope {0}, R val {1}, P val {2}".format(slope, r_value, p_value))

    x = cyclesHols[axes[0]]
    y = cyclesHols[axes[1]]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    evaluatedLine = np.polyval([slope, intercept], y)

    return
    plt.title('All Holidays - {0} vs {1}'.format(axes[0],axes[1]))
#    plt.xlabel('Humidity')
#    plt.ylabel('Cycle#')
    plt.xlim([20,100])
    plt.ylim([0,50000])
    plt.scatter(x,y)
    plt.plot(y, evaluatedLine, 'k-')
    if printPlots == 'True': 
        plt.show()
    print('All Holidays - {0} vs {1}'.format(axes[0],axes[1]))
    print("STATS : Slope {0}, R val {1}, P val {2}".format(slope, r_value, p_value))



def analyse_Rainfall(data_path, cycle_file):
    cycles = pd.read_excel(data_path + cycle_file, 'CycleData', index_col=None, na_values=['NA'])

    # DayType
    cyclesWork = cycles[cycles['DayType'] == 'Work']
    print(cyclesWork.shape)
    cyclesHols = cycles[cycles['DayType'] == 'Hols']
    print(cyclesHols.shape)
 
    # Dry Days
    cyclesWorkDry = cyclesWork[cyclesWork['Rainfall'] == 0]
    print(cyclesWorkDry.shape)
    cyclesHolsDry = cyclesHols[cyclesHols['Rainfall'] == 0]
    print(cyclesHolsDry.shape)

    # Wet Days
    cyclesWorkWet = cyclesWork[cyclesWork['Rainfall'] > 0]
    print(cyclesWorkWet.shape)
    cyclesHolsWet = cyclesHols[cyclesHols['Rainfall'] > 0]
    print(cyclesHolsWet.shape)
    
    # Rainfall
    axes = ['Rainfall','Cycle#']
    x = cyclesWorkWet[axes[0]]
    y = cyclesWorkWet[axes[1]]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    evaluatedLine = np.polyval([slope, intercept], y)

    plt.title('All Wet Workdays - {0} vs {1}'.format(axes[0],axes[1]))
#    plt.xtitle('Humidity')
#    plt.ytitle('Cycle#')
    plt.xlim([0,45])
    plt.ylim([0,50000])
    plt.scatter(x,y)
    plt.plot(y, evaluatedLine, 'k-')
    if printPlots == 'True': 
        plt.show()
    print('All Wet Workdays - {0} vs {1}'.format(axes[0],axes[1]))
    print("STATS : Slope {0}, R val {1}, P val {2}".format(slope, r_value, p_value))

    x = cyclesHolsWet[axes[0]]
    y = cyclesHolsWet[axes[1]]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    evaluatedLine = np.polyval([slope, intercept], y)

    plt.title('All Wet Holidays - {0} vs {1}'.format(axes[0],axes[1]))
#    plt.xlabel('Humidity')
#    plt.ylabel('Cycle#')
    plt.xlim([0,45])
    plt.ylim([0,50000])
    plt.scatter(x,y)
    plt.plot(y, evaluatedLine, 'k-')
    if printPlots == 'True': 
        plt.show()
    print('All Wet Holidays - {0} vs {1}'.format(axes[0],axes[1]))
    print("STATS : Slope {0}, R val {1}, P val {2}".format(slope, r_value, p_value))

    # Wet Days
    cyclesWet = cycles[cycles['Rainfall'] > 0]
    print("")
    print("ANALYSIS OF WET DAYS")
    print(df_analysis(cyclesWet))

    cyclesWetLow = cyclesWet[cyclesWet['Rainfall'] <= 4.3]
    print("LESS WET ",cyclesWetLow.shape)
    print(cyclesWetLow.describe)
    
    cyclesWetHigh = cyclesWet[cyclesWet['Rainfall'] > 4.3]
    print("MORE WET ",cyclesWetHigh.shape)
    print(cyclesWetHigh.describe)
    

    plt.title('All Wet days')
    plt.hist(cyclesWet['Rainfall'], bins=20)
    if printPlots == 'True':  
        plt.show()

    # Temperature
    axes = ['Temperature','Cycle#']
    x = cyclesWet[axes[0]]
    y = cyclesWet[axes[1]]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    evaluatedLine = np.polyval([slope, intercept], y)

    plt.title('All Wet - {0} vs {1}'.format(axes[0],axes[1]))
    plt.xlabel = axes[0]
    plt.ylabel = axes[1]
    plt.xlim([0,20])
    plt.ylim([0,50000])
    plt.scatter(x,y)
    if printPlots == 'True':  
        plt.show()
    print('All Wet - {0} vs {1}'.format(axes[0],axes[1]))
    print("STATS : Slope {0}, R val {1}, P val {2}".format(slope, r_value, p_value))

    # Temperature
    axes = ['Temperature','Cycle#']
    x = cyclesWetLow[axes[0]]
    y = cyclesWetLow[axes[1]]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    evaluatedLine = np.polyval([slope, intercept], y)

    plt.title('Less Wet - {0} vs {1}'.format(axes[0],axes[1]))
    plt.xlabel = axes[0]
    plt.ylabel = axes[1]
    plt.xlim([0,20])
    plt.ylim([0,50000])
    plt.scatter(x,y)
    if printPlots == 'True':  
        plt.show()
    print('Less Wet - {0} vs {1}'.format(axes[0],axes[1]))
    print("STATS : Slope {0}, R val {1}, P val {2}".format(slope, r_value, p_value))


    axes = ['Temperature','Cycle#']
    x = cyclesWetHigh[axes[0]]
    y = cyclesWetHigh[axes[1]]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    evaluatedLine = np.polyval([slope, intercept], y)

    plt.title('More Wet - {0} vs {1}'.format(axes[0],axes[1]))
    plt.xlabel = axes[0]
    plt.ylabel = axes[1]
    plt.xlim([0,20])
    plt.ylim([0,50000])
    plt.scatter(x,y)
    if printPlots == 'True':  
        plt.show()
    print('More Wet - {0} vs {1}'.format(axes[0],axes[1]))
    print("STATS : Slope {0}, R val {1}, P val {2}".format(slope, r_value, p_value))

#    plt.title('All Less Wet days')
#    plt.hist(cyclesWetLow['Rainfall'])
#    if printPlots == 'True':  
#        plt.show()
#
#    plt.title('All More Wet days')
#    plt.hist(cyclesWetHigh['Rainfall'])
#    if printPlots == 'True':  
#        plt.show()


