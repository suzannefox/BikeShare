# -*- coding: utf-8 -*-
"""
Created on Thu Nov 27 19:54:27 2014

@author: Suzanne
"""
import pandas as pd
import numpy as np
import re

def convert_from_xls_col(myCol):
    col_no = 0
    
    if len(myCol) == 1:
        col_no = ord(myCol)
    else:
        f1 = myCol[0]
        f2 = myCol[1]
        
        i1 = (ord(f1)-64) * 26
        i2 = ord(f2) - 64
        col_no = i1 + i2 
    
    return col_no
                
def convert_to_xls_col(counter):
    diagnostics = False
    
    # in python cols start at 0, in XLS they start at 1 or A
    counter +=1
    
#    A = 65
#    Z = 90
    myCol = ''
    loops = 0
    initcounter = counter
    
    while True:    
        F = float(counter)
        rem = int(F % 27)
        whl = int(counter / 27)
        if whl == 0:
            break
        loops +=1
        counter -= 26

    if loops == 0:
        myCol = chr(rem+64)
    else:
        myCol = chr(loops + 64)
        myCol = myCol + chr(rem+64) 
    
    if diagnostics == True:
        print(">> ", initcounter, counter, " loops ",loops, " rem ",rem,  " >> ",myCol)
    return myCol

def analyse_tubes_csv(info,data_path, orig_tube_file, new_tube_entry_file, new_tube_exit_file):

    if info == 'csv':
        for x in range(0,120):
            print ("X is ",x," col ",convert_to_xls_col(x))
        
        return
    
    if info == 'columns':
        colval = 65
        colxval = 64
        colno = 0
        
        in_file = open(data_path + orig_tube_file,'r')
        line_no = 0
        for line in in_file:
            line_no +=1
            if line_no > 1:
                break
            
            cols = line.split(',')
            for col in cols:
                if colxval > 64:
                    colasc = chr(colxval) + chr(colval)
                else:
                    colasc = chr(colval)
                    
                print (colasc, colno, col)
                colno +=1
                colval +=1
                if colval == 91:
                    colxval +=1
                    colval = 65
                
        in_file.close()

    if info == 'dups':
        tubes = pd.read_csv(data_path + orig_tube_file)
        print(tubes.describe)
        trips = np.sum(tubes['Total_day_count'])
        print (trips)
        print(tubes['Flag'].value_counts())
        badtubes = tubes[(tubes['Flag'] == 3)]

        badtubes.to_csv('badtubes.csv')                

    if info == 'colnames':
        tubes = pd.read_csv(data_path + orig_tube_file)
        collist = tubes.columns.values
        x = 0
        for col in collist:
            print("offset {0}, XLS {2}, col name {1}".format(x, col, convert_to_xls_col(x)))
            x +=1

    if info == 'stations':
        tubes = pd.read_csv(data_path + orig_tube_file)
        print("Stations in file")
        print(tubes['Station'].value_counts())

    if info == 'Waterloo':
        tubes = pd.read_csv(data_path + orig_tube_file)
        waterloo = tubes[(tubes['Station']=='Waterloo')]
        waterloo = waterloo[(waterloo['Gate_location']=='TOTAL')]
        waterloo = waterloo[(waterloo['Entry_or_exit']=='Entry')]
        waterloo.to_csv(data_path + new_tube_entry_file, index=False)
        
    if info == 'split':
        tubes = pd.read_csv(data_path + orig_tube_file)
        print(tubes.describe)
        trips = np.sum(tubes['Total_day_count'])
        print (trips)
        print(tubes['Flag'].value_counts())
        badtubes = tubes[:0:60]
        badtubes = tubes.head(50)
        badtubes.to_csv('badtubes.csv')                

    if info == 'counts':
        in_file = open(data_path + orig_tube_file,'r')
        out_exit_file = open(data_path + new_tube_exit_file,'w')
        out_entry_file = open(data_path + new_tube_entry_file,'w')
        line_no = 0
        output_no = 0
        no_gates = 0
        no_total = 0
        good_entry_lines = 0
        good_exit_lines = 0
    
        for line in in_file:
            line_no +=1
            tokens = line.split(',')
    
            myGate = tokens[1]
            if myGate == 'No gateline data yet':
                no_gates +=1
                continue
                
            if not (myGate=='' or myGate=='TOTAL'):
                continue
            
            myStation = tokens[0]
            myDate = tokens[2]
            myType = tokens[5]        
            
            if myStation=='Southgate':
                print (line)
                
            if myType == 'Entry':
                good_entry_lines +=1
                print (myStation,  myGate, myType)
    #            out_file.write("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}\n".format('Route_id', 'Date', \
    #                                                        'Morning Rush','Morning','Afternoon', \
    #                                                        'Evening Rush','Evening','Night','Strange','Check'))
            if myType == 'Exit':
                good_exit_lines +=1

        print ("FINISHED")
        print ("No gateline data for ",no_gates)
        print ("No day total data for ",no_total)
        print ("TOTAL ",line_no)
        print ("TOTAL ENTRY GOOD ",good_entry_lines)
        print ("TOTAL EXIT GOOD ",good_exit_lines)

# Get Tube Stations Entry data
def tubes_entrydata(data_path, station_file, orig_tube_file, entry_tube_file):

#        stations = pd.read_csv(data_path + station_file)
#        print("STATIONS DATA")
#        print(stations.describe)
#        print(stations['Zone'].value_counts())
#        stations123 = stations[(stations['Zone'] == '1') | (stations['Zone'] == '2') | (stations['Zone'] == '3') | (stations['Zone'] == '2,3') | (stations['Zone'] == '3,4')]

        tubedata = pd.read_csv(data_path + orig_tube_file)
        print ("TOTAL ROWS ",len(tubedata.index))
        
        tubedata = tubedata[(tubedata['Entry_or_exit'] == 'Entry')]
        print ("TOTAL ENTRY ROWS ",len(tubedata.index))
        
        tubedata = tubedata[(tubedata['Gate_location'] != 'No gateline data yet')]
        print ("TOTAL ENTRY ROWS WITH DATA",len(tubedata.index))

        tubedata = tubedata[(tubedata['Total_day_count'] > 0)]
        print ("TOTAL ENTRY ROWS WITH DATA > 0",len(tubedata.index))
        
        # Some Stations have rows with TOTAL and other gates
        # Remove other gates
        SG = ["Aldgate East","Baker Street","Bank & Monument","Canary Wharf",\
              "Charing Cross","Earl's Court","Edgware Road (Cir)","Elephant & Castle","Farringdon", \
              "Finchley Central","Hammersmith (Dis)","Kew Gardens","King's Cross St. Pancras", \
              "Knightsbridge","Leicester Square","Liverpool Street","London Bridge","Moorgate", \
              "Oxford Circus","Paddington","Seven Sisters","South Woodford","Southwark", \
              "St. James's Park","Stratford","Sudbury Town","Tower Hill","Victoria", \
              "Waterloo","Willesden Junction","Woodford"]

        for sg in SG:
            tubedata = tubedata[(tubedata['Station']!= sg ) | \
                               ((tubedata['Station']== sg ) & (tubedata['Gate_location']=='TOTAL'))]

        print ("TOTAL ENTRY ROWS WITH NON-DUPLICATED DATA",len(tubedata.index))

        tubedata.to_csv(data_path + entry_tube_file)

# Reformat to time periods. Columns are +1 from original CSV
# because this is output from dataframe
def tubes_reformat(data_path, entry_tube_file, station_tube_file):
        diagnostics = False
        in_file = open(data_path + entry_tube_file,'r')
        out_file = open(data_path + station_tube_file,'w')

        line_no = 0

#    mapping = {'06:00': 'night',
#               '07:00': 'night',
#               '08:00': 'morning rush',
#               '09:00': 'morning rush',
#               '10:00': 'morning',
#               '11:00': 'morning',
#               '12:00': 'morning',
#               '13:00': 'morning',
#               '14:00': 'afternoon',
#               '15:00': 'afternoon',
#               '16:00': 'afternoon',
#               '17:00': 'afternoon',
#               '18:00': 'evening rush',
#               '19:00': 'evening rush',
#               '20:00': 'evening',
#               '21:00': 'evening',
#               '22:00': 'evening',
#               '23:00': 'evening',
#               '24:00': 'evening',
#               '01:00': 'night', 
#               '02:00': 'night',
#               '03:00': 'night',
#               '04:00': 'night',
#               '05:00': 'night'}

        # Columns to use
        Morning_rush = (108, 109)
        Morning = (110, 113)
        Afternoon = (114, 117)
        Evening_rush = (118, 119)
        Evening = (120, 124)
        Night1 = (103, 107)
        Night2 = (125, 126)
    
        for line in in_file:
            line_no +=1

            # First line is the header
            if line_no == 1:
                out_file.write("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}\n".format('Station', 'Date', 'Total',\
                                                            'Morning Rush','Morning','Afternoon', \
                                                            'Evening Rush','Evening','Night','Strange','Check'))
                continue

            # split the line into elements
            tokens = line.strip().split(',')

            # Only interestid in 01/01/2012 for now
            myDate = tokens[2]
            
            myStation = tokens[0]
            myTotal = tokens[6]

            # Morning rush
            Count_MR = 0
            for x in range(Morning_rush[0], Morning_rush[1]+1):
                if diagnostics == True :
                    print("MR x is ",x, " col ",convert_to_xls_col(x)," ",int(tokens[x]))
                Count_MR += int(tokens[x])

            # Morning 
            Count_M = 0
            for x in range(Morning[0], Morning[1]+1):
                if diagnostics == True :
                    print("M x is ",x,convert_to_xls_col(x)," ",int(tokens[x]))
                Count_M += int(tokens[x])

            # Afternoon
            Count_A = 0
            for x in range(Afternoon[0], Afternoon[1]+1):
                if diagnostics == True :
                    print("A x is ",x,convert_to_xls_col(x))
                Count_A += int(tokens[x])

            # Evening Rush
            Count_ER = 0
            for x in range(Evening_rush[0], Evening_rush[1]+1):
                if diagnostics == True :
                    print("ER x is ",x,convert_to_xls_col(x))
                Count_ER += int(tokens[x])
            
            # Evening
            Count_E = 0
            for x in range(Evening[0], Evening[1]+1):
                if diagnostics == True :
                    print("E x is ",x,convert_to_xls_col(x))
                Count_E += int(tokens[x])

            # Night
            Count_N = 0
            for x in range(Night1[0], Night1[1] + 1):
                if diagnostics == True :
                    print("N1 x is ",x,convert_to_xls_col(x))
                Count_N += int(tokens[x])

            for x in range(Night2[0], Night2[1]+1):
                if diagnostics == True :
                    print("N2 x is ",x,convert_to_xls_col(x)," ",int(tokens[x]))
                Count_N += int(tokens[x])

            out_file.write("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}\n".format(myStation, myDate, myTotal, \
                                   Count_MR, \
                                   Count_M, \
                                   Count_A, \
                                   Count_ER, \
                                   Count_E, \
                                   Count_N, \
                                   0, \
                                   0))
                
        in_file.close()
        out_file.close()
        
        print ("FINISHED, LINES ", line_no)

def tubes_accumulate(data_path, station_tube_file, total_tube_file):
        diagnostics = False
        in_file = open(data_path + station_tube_file,'r')
        out_file = open(data_path + total_tube_file,'w')

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

        CurrentDate = ''    
        Current_Tot = 0
        Current_MR = 0
        Current_M = 0
        Current_A =0
        Current_ER = 0
        Current_E = 0
        Current_N = 0
        
        for line in in_file:
            line_no +=1

            # First line is the header
            if line_no == 1:
                out_file.write("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}\n".format('Date', 'Total',\
                                                            'Morning Rush','Morning','Afternoon', \
                                                            'Evening Rush','Evening','Night'))
                continue

            # split the line into elements
            tokens = line.strip().split(',')
            if line_no == 2:
                CurrentDate = tokens[1]
            
            myDate = tokens[1]
            if myDate != CurrentDate:
                out_no +=1
                out_file.write("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}\n".format(CurrentDate, Current_Tot,\
                                                            Current_MR,Current_M,Current_A, \
                                                            Current_ER,Current_E,Current_N))
                Current_Tot = 0
                Current_MR = 0
                Current_M = 0
                Current_A =0
                Current_ER = 0
                Current_E = 0
                Current_N = 0
                CurrentDate = myDate
                
            Current_Tot += int(tokens[TotalTrips])
            Current_MR += int(tokens[Morning_rush])
            Current_M += int(tokens[Morning])
            Current_A += int(tokens[Afternoon])
            Current_ER += int(tokens[Evening_rush])
            Current_E += int(tokens[Evening])
            Current_N += int(tokens[Night])

        # Finished file read
        out_no +=1
        out_file.write("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}\n".format(CurrentDate, Current_Tot,\
                                                Current_MR,Current_M,Current_A, \
                                                Current_ER,Current_E,Current_N))

        in_file.close()
        out_file.close()
        print("FINISHED {0} Lines processed, {1} output".format(line_no, out_no))
    
