# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 12:49:27 2014

@author: Suzanne
"""
import numpy as np
import pandas as pd
from pylab import plot,show
from numpy import vstack,array
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq

def create_clusters(data_path, cycle_file):
    # data generation
    cycles = pd.read_excel(data_path + cycle_file, 'CycleData', index_col=None, na_values=['NA'])
    # DayType
    cyclesWork = cycles[cycles['DayType'] == 'Work']
    cyclesWorkDry = cyclesWork[cyclesWork['Rainfall'] > 0]

# =================================================================
# 
    cycles = cyclesWorkDry[['Temperature','Humidity','Cycle#']]
    print("Option 1")
    print(cycles.shape)

#    # generate numpy array
#    data = cycles.as_matrix()
#    
#    # computing K-Means with K = 2 (2 clusters)
#    centroids,_ = kmeans(data,2)
#    # assign each sample to a cluster
#    idx,_ = vq(data,centroids)
#    
#    # some plotting using numpy's logical indexing
#    plot(data[idx==0,0],data[idx==0,1],'ob',
#         data[idx==1,0],data[idx==1,1],'or')
#    plot(centroids[:,0],centroids[:,1],'sg',markersize=8)
#    show()
#
#    # add cluster members back onto data
#    cycles['Cluster'] = idx
#
#    cyclesWorkDry0 = cycles[cycles['Cluster'] == 0]
#    cyclesWorkDry1 = cycles[cycles['Cluster'] == 1]
#    # Analyse by cluster
#    print("CLUSTER 0")
#    print(cyclesWorkDry0.shape)
#    print(cyclesWorkDry0.describe())
#    print("")
#    print("CLUSTER 1")
#    print(cyclesWorkDry1.shape)
#    print(cyclesWorkDry1.describe())



# =================================================================
# 
    cycles = cyclesWorkDry[['Temperature','Cycle#']]
    print("Option 2")
    print(cycles.shape)

    # generate numpy array
    data = cycles.as_matrix()
    
    # computing K-Means with K = 2 (2 clusters)
    centroids,_ = kmeans(data,2)
    # assign each sample to a cluster
    idx,_ = vq(data,centroids)
    
    # some plotting using numpy's logical indexing
    plot(data[idx==0,0],data[idx==0,1],'og',
         data[idx==1,0],data[idx==1,1],'ob')
    plot(centroids[:,0],centroids[:,1],'sr',markersize=15)
    show()

    # add cluster members back onto data
    cycles['Cluster'] = idx

    cyclesWorkDry0 = cycles[cycles['Cluster'] == 0]
    cyclesWorkDry1 = cycles[cycles['Cluster'] == 1]
    # Analyse by cluster
    print("CLUSTER 0")
    print(cyclesWorkDry0.shape)
    print(cyclesWorkDry0.describe())
    print(cyclesWorkDry0.sum())
    print("")
    print("CLUSTER 1")
    print(cyclesWorkDry1.shape)
    print(cyclesWorkDry1.describe())
    print(cyclesWorkDry1.sum())

#    CLUSTERS.create_clusters(data_path, cycle_file)
    



def create_test_clusters():
    # data generation
    data = vstack((rand(150,3) + array([.5,.5,.5]),rand(150,3) ))
    
    # computing K-Means with K = 2 (2 clusters)
    centroids,_ = kmeans(data,2)
    # assign each sample to a cluster
    idx,_ = vq(data,centroids)
    
    # some plotting using numpy's logical indexing
    plot(data[idx==0,0],data[idx==0,1],'ob',
         data[idx==1,0],data[idx==1,1],'or')
    plot(centroids[:,0],centroids[:,1],'sg',markersize=8)
    show()

    centroids,_ = kmeans(data,3)
    idx,_ = vq(data,centroids)
    
    plot(data[idx==0,0],data[idx==0,1],'ob',
         data[idx==1,0],data[idx==1,1],'or',
         data[idx==2,0],data[idx==2,1],'og') # third cluster points
    plot(centroids[:,0],centroids[:,1],'sm',markersize=8)
    show()

