# -*- coding: utf-8 -*-
"""
Created on Thu Nov 27 18:59:37 2014

@author: Suzanne
"""

import pandas as pd
import numpy as np

def analyse_buses_csv(data_path, orig_bus_file, new_bus_file):
    buses = pd.read_csv(data_path + orig_bus_file)
    print(buses.describe)
    trips = np.sum(buses['Boardings'])
    print (trips)
    
def buses_reformat(data_path, orig_bus_file, daily_bus_file, bus_area):    
    diagnostics = False

    # Map the end times to periods of the day
    mapping = {'06:00': 'night',
               '07:00': 'night',
               '08:00': 'morning rush',
               '09:00': 'morning rush',
               '10:00': 'morning',
               '11:00': 'morning',
               '12:00': 'morning',
               '13:00': 'morning',
               '14:00': 'afternoon',
               '15:00': 'afternoon',
               '16:00': 'afternoon',
               '17:00': 'afternoon',
               '18:00': 'evening rush',
               '19:00': 'evening rush',
               '20:00': 'evening',
               '21:00': 'evening',
               '22:00': 'evening',
               '23:00': 'evening',
               '24:00': 'evening',
               '01:00': 'night', 
               '02:00': 'night',
               '03:00': 'night',
               '04:00': 'night',
               '05:00': 'night'}
    
    
    in_file = open(data_path + orig_bus_file,'r')
    out_file = open(data_path + daily_bus_file,'w')
    line_no = 0 ; output_no = 0
    
    CurrentRoute = "NEW"
    CurrentDate = "NEW"
    CurrentPeriod = "NEW"
    Current_T = 0
    Current_MR = 0
    Current_M = 0
    Current_A = 0
    Current_ER = 0
    Current_E = 0
    Current_N = 0
    Current_S = 0
    Boardings = 0
    TotalBoardings = 0
    
    routes = []
    if bus_area == 'Waterloo Bridge':
        routes = ['1','4','26','59','68','76','139','168','171','172','176','188','RV1']
    
    for line in in_file:
        line_no +=1
        csvl = line.split(',')
    
        if line_no == 1:
            out_file.write("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}\n".format('Route_id', 'Date', 'Total', \
                                                        'Morning Rush','Morning','Afternoon', \
                                                        'Evening Rush','Evening','Night','Strange'))
            continue
        
        myRoute = csvl[0]

        got_Route = True        
        if bus_area == 'Waterloo Bridge':
            got_Route = False
            for goodroute in routes:
                if myRoute == goodroute:
                    got_Route = True
                    continue
        
        if got_Route == False:
            continue
        
        myDate = csvl[1]
        myEnd = csvl[3]
        myBoardings = int(csvl[4])
        TotalBoardings += myBoardings
            
        myPeriod = 'strange'
        for thetime in mapping:
           if thetime==myEnd:
               myPeriod = mapping.get(thetime)
               break
        
        NewData = True
        
        if line_no == 2:
            CurrentRoute = myRoute
            CurrentDate = myDate
            CurrentPeriod = myPeriod
                    
        if myRoute == CurrentRoute:
            if myDate == CurrentDate:
                NewData = False
                Current_T += myBoardings

                if myPeriod == 'morning rush':
                    Current_MR += myBoardings
                elif myPeriod == 'morning':
                    Current_M += myBoardings
                elif myPeriod == 'afternoon':
                    Current_A += myBoardings
                elif myPeriod == 'evening rush':
                    Current_ER += myBoardings
                elif myPeriod == 'evening':
                    Current_E += myBoardings
                elif myPeriod == 'night':
                    Current_N += myBoardings
                elif myPeriod == 'strange':
                    Current_S += myBoardings
                    
        if NewData == True:        
            # forget night buses
            if myRoute.startswith('N'):
                continue

            output_no +=1
            if output_no == 1:
                continue
    
            if myPeriod == 'strange' :
                continue

            if diagnostics == True:                
                print ("VALS {0}, {1}, {2}, {3}".format(CurrentRoute, CurrentDate, CurrentPeriod, Boardings))
            out_file.write('"{0}", {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}\n'.format(CurrentRoute, CurrentDate, \
                                       Current_T, \
                                       Current_MR, \
                                       Current_M, \
                                       Current_A, \
                                       Current_ER, \
                                       Current_E, \
                                       Current_N, \
                                       Current_S))
    
            CurrentRoute = myRoute
            CurrentDate = myDate
            CurrentPeriod = myPeriod
            Boardings = myBoardings
            Current_T = 0
            Current_MR = 0
            Current_M = 0
            Current_A = 0
            Current_ER = 0
            Current_E = 0
            Current_N = 0
            Current_S = 0
            Current_X = 0
            Current_T = myBoardings
            if myPeriod == 'morning rush':
                Current_MR = myBoardings
            elif myPeriod == 'morning':
                Current_M = myBoardings
            elif myPeriod == 'afternoon':
                Current_A = myBoardings
            elif myPeriod == 'evening rush':
                Current_ER = myBoardings
            elif myPeriod == 'evening':
                Current_E = myBoardings
            elif myPeriod == 'night':
                Current_N = myBoardings
            elif myPeriod == 'strange':
                Current_S = myBoardings
    
    # Final line
    out_file.write('"{0}", {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}\n'.format(CurrentRoute, CurrentDate, \
                               Current_T, \
                               Current_MR, \
                               Current_M, \
                               Current_A, \
                               Current_ER, \
                               Current_E, \
                               Current_N, \
                               Current_S))
    
    print("FINISHED")
    in_file.close()
    out_file.close()
    print("lines in {0}, lines out {1}, Boardings {2}".format(line_no, output_no, TotalBoardings))

def buses_accumulate(data_path, area_bus_file, total_bus_file):
        diagnostics = False
        in_file = open(data_path + area_bus_file,'r')
        out_file = open(data_path + total_bus_file,'w')

        line_no = 0
        out_no = 0
        
        # Columns to use
        TotalTrips = 2
        Morning_rush = 3
        Morning = 4
        Afternoon = 5
        Evening_rush = 6
        Evening = 7
        Night = 8
        Strange = 9

        CurrentDate = ''    
        Current_Tot = 0
        Current_MR = 0
        Current_M = 0
        Current_A =0
        Current_ER = 0
        Current_E = 0
        Current_N = 0
        Current_S = 0
        
        for line in in_file:
            line_no +=1

            # First line is the header
            if line_no == 1:
                out_file.write("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}\n".format('Date', 'Total',\
                                                            'Morning Rush','Morning','Afternoon', \
                                                            'Evening Rush','Evening','Night', 'Strange'))
                continue

            # split the line into elements
            tokens = line.strip().split(',')
            if line_no == 2:
                CurrentDate = tokens[1]
            
            myDate = tokens[1]
            if myDate != CurrentDate:
                out_no +=1
                out_file.write("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}\n".format(CurrentDate, Current_Tot,\
                                                            Current_MR,Current_M,Current_A, \
                                                            Current_ER,Current_E,Current_N, Current_S))
                Current_Tot = 0
                Current_MR = 0
                Current_M = 0
                Current_A =0
                Current_ER = 0
                Current_E = 0
                Current_N = 0
                Current_S = 0
                CurrentDate = myDate
                
            Current_Tot += int(tokens[TotalTrips])
            Current_MR += int(tokens[Morning_rush])
            Current_M += int(tokens[Morning])
            Current_A += int(tokens[Afternoon])
            Current_ER += int(tokens[Evening_rush])
            Current_E += int(tokens[Evening])
            Current_N += int(tokens[Night])
            Current_N += int(tokens[Strange])

        # Finished file read
        out_no +=1
        out_file.write("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}\n".format(CurrentDate, Current_Tot,\
                                                Current_MR,Current_M,Current_A, \
                                                Current_ER,Current_E,Current_N,Current_S))

        in_file.close()
        out_file.close()
        print("FINISHED {0} Lines processed, {1} output".format(line_no, out_no))
