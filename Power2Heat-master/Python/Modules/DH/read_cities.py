# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 10:02:04 2016

@author: Gerald
"""

import numpy as np
import os

def read_cities(exclude_waste):
    """ Reads data for yearly total DH demand of all Swedish networks from file
    and compares the locations with GIS data for Swedish cities. Returns a 
    dictionary mapping cities to a list containing counties and DH data.
    """
    
    print 'Sorting networks into regions'
    
    # specify location of GIS files
    dir_DH = os.path.dirname(os.path.abspath(__file__))
    dir_Modules = os.path.dirname(dir_DH)
    dir_Python = os.path.dirname(dir_Modules)
    dir_Power2Heat = os.path.dirname(dir_Python)
    
    file_location = os.path.join(dir_Power2Heat, 'Data', 'GIS',
                                 'ReadyImport6.csv')
    file1_location = os.path.join(dir_Power2Heat, 'Data', 'GIS',
                                 'ReadyImport_backGIs.csv')
    
    file = np.genfromtxt(file_location, delimiter =";",names =True, dtype = None)
    file1 =np.genfromtxt(file1_location, delimiter =";",names =True, dtype = None)
    
    cities1 = file1["AllCities"] # how does this work?
    Category1 = file1["Category"]
    
    ForGis1 = np.zeros(len(cities1))
    
    cities = file["AllCities"]
    states= file["State"]
    DHCity = file["DHCity"]
    Production = file["Production"]
    Waste = file["Waste"]
    
    ForGis = np.zeros(len(cities))
    
    # in order to avoid repetitions in cities, make a dictionary with cities as
    # keys. Map each city to a list with its corresponding indices
    cities_dict = {}
    for index, c in enumerate(cities):
        if c in cities_dict:
            cities_dict[c].append(index)
        else:
            cities_dict[c] = [index]
    
    count = 0
    result = {}
    unlocated_networks = []
    
    # create dict with key = city; value = [state, Demand]
    for xx, dh in enumerate(DHCity):
        loc_found = 0
        for c, index_list in cities_dict.iteritems():
            if dh == c: 
                count =count+1
                if c in result:
                    result[c][1] += Production[xx]
                    result[c][2] += Waste[xx]
                else:
                    result[c] = [states[index_list[0]], Production[xx], Waste[xx]]
                    for ii in index_list:
                        ForGis[ii] = 1
                loc_found = 1            
            else:            
                pass
        if not loc_found:
            unlocated_networks.append(DHCity[xx])
    
    #print unlocated_networks
        
           
    # calculate total heat production       
    q_tot = sum([result[r][1] for r in result]) 
    print "Total production: ", q_tot
           
            
    # create dict with key = state, value = [numberofUnits, sum of production]
            
    StateDict = {}
    result2 = {}
    result3 = {}
    
#    for city, (state, pop) in result.items(): 
#        citycount, totalpop = result2.get(state, (0, 0))
#        result2[state] = (citycount + 1, totalpop + pop)
#    
#    
#    for city, (state, pop) in result.items(): 
#        citycount, totalpop = result2.get(state, (0, 0))
#        result3[state] = (totalpop + pop)
#    fig1 = plt.figure()
#    plt.bar(range(len(result3)), result3.values(), align='center')
#    plt.xticks(range(len(result3)), result3.keys(), rotation='vertical')
#    
#    plt.show()
    
    #check if for GIS
    
    for iii, cc in enumerate(cities1):
       for xxx, dhh in enumerate(DHCity):
           if DHCity[xxx] == cities1[iii]  and {Category1[iii] == "city" or Category1[iii] == "town"}: 
                #print "found in {}".format(ii)
                
                ForGis1[iii] = 1
           else:
                
                pass
    
    
    
    #np.savetxt('D:\\666.txt', np.transpose([cities1,ForGis1]), delimiter =';', fmt='%s')
    return result 
        
        