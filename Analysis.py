# -*- coding: utf-8 -*-
"""
Created on Thu Nov 27 10:13:27 2014

@author: Suzanne
"""

import matplotlib.pyplot as plt 
from scipy import stats
import pandas as pd
import numpy as np

from pylab import plot,show
from numpy import vstack,array
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq


data_path = 'Data/'


# Bus Boarding data
orig_bus_file = 'tfl_bus_hourly_boardings_2012.csv'
daily_bus_file = 'bus_daily_data.csv'
waterloo_bus_file = 'bus_waterloo_data.csv'
total_waterloo_file = 'bus_wattot_data.csv'

# Tube usage data
orig_tube_file = 'tfl_underground_quarter_hourly_entry_exit_counts_2012.csv'
entry_tube_file = 'tube_entry_data.csv'
station_tube_file = 'tube_station_data.csv'
total_tube_file = 'tube_total_data.csv'
waterloo_tube_file = 'tube_waterloo_data.csv'
total_waterloo_tube_file = 'tube_wattot_data.csv'
station_file = 'London stations.csv'

# Cycle Data
cycle_file = 'CW02-CycleHire.xlsx'

# Total data
data_file = 'CW02-Data.xlsx'

import include_Buses as BUSES
import include_Tubes as TUBES
import include_Cycles as CYCLES
import include_Clusters as CLUSTERS

   
if __name__ == "__main__":

# ==========================================================================
# Buses, take orig_bus_file, use BUSES.buses_reformat to collapse
#        data into route per day format, with times as columns
#        this creates daily_bus_file
#    BUSES.buses_reformat(data_path, orig_bus_file, daily_bus_file, '')
    
#   Just get the buses which go over Waterloo bridge
#    BUSES.buses_reformat(data_path, orig_bus_file, waterloo_bus_file, 'Waterloo Bridge')
#    BUSES.buses_accumulate(data_path, waterloo_bus_file, total_waterloo_file)    
#    BUSES.analyse_buses_csv(data_path, total_waterloo_file)   
    
# ==========================================================================
# Get some data about the tubes file
#    TUBES.analyse_tubes_csv('stations', data_path, orig_tube_file, '', '')
#
# Tubes, take orig_tube_file, use TUBES.tubes_entrydata to split off Entry
#        records for valid line
#        put output fom this into TUBES.tubes_reformat to create Station
#        level data for each day by Periods (Morning rush, Morning ... Night)
#        take output from this and use TUBES.tubes_daily to accumulate
#        for all stations
#   Step 1. Split out valid Tube entry records into a new file
#   TUBES.tubes_entrydata(data_path, station_file, orig_tube_file, entry_tube_file)
#   Step 2. From the data that has been split off, reformat by station
#    TUBES.tubes_reformat(data_path, entry_tube_file, station_tube_file)
#   Step 3. Accumulate across stations giving daily data
#    TUBES.tubes_accumulate(data_path, station_tube_file, total_tube_file)
#
# Create data just for Waterloo
#    TUBES.analyse_tubes_csv('Waterloo', data_path, orig_tube_file, waterloo_tube_file, '')
#    print("WATERLOO")
#    TUBES.analyse_tubes_csv('columns', data_path, waterloo_tube_file, '', '')
#    print("TOTAL DATA")
#    TUBES.analyse_tubes_csv('columns', data_path, orig_tube_file, '', '')
#     TUBES.tubes_reformat(data_path, waterloo_tube_file, total_waterloo_tube_file)

# Analyze Cycle usage
#    print("Topline figures")
#    CYCLES.analyse_Topline(data_path, cycle_file)
#    print("TEMPERATURE")
#    CYCLES.analyse_Temperature(data_path, cycle_file)
#    print("RAINFALL")
#    CYCLES.analyse_Rainfall(data_path, cycle_file)
#    print("HUMIDITY")
#    CYCLES.analyse_Humidity(data_path, cycle_file)    
#    print("WIND SPEED")
#    CYCLES.analyse_WindSpeed(data_path, cycle_file)

#    CYCLES.analyse_quartiles(data_path, cycle_file)

#    CLUSTERS.create_clusters(data_path, cycle_file)
#    data = pd.read_excel(data_path + data_file, 'Sheet1', index_col=None, na_values=['NA'])
#
#    print(data.describe())
#    
    plt.plot(data['Cycle Hires'])
    plt.show()
#    
#    plt.plot(data['Tube Morning Rush'])
#    plt.show()
#    
#    plt.plot(data['Bus Morning Rush'])
#    plt.show()
