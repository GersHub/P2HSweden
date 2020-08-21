# -*- coding: utf-8 -*-
"""
Created on Thu May 26 09:47:41 2016

@author: Jonatan
"""

import matplotlib.pyplot as plt

def plot_compare_p2h(p2h_no_ac, p2h):    
    """Compare p2h potential to the case without accumulator. Values are
    plotted chronologically. """   

    plt.figure(2)
    plt.clf()
    with_ac, = plt.plot(p2h, label = 'with ac')
    no_ac, = plt.plot(p2h_no_ac, label = 'no_ac')
    plt.legend(handles = [with_ac, no_ac])
    plt.xlabel('Time [h]')
    plt.ylabel('P2H [GWh]')

def plot_storage(storage):
    """ Plot the storage over time for the major regions.
    """
    
    plt.figure(6)
    plt.clf()  
    
    st, = plt.plot(storage['Stockholm'], label = 'Stockholm')
    sk, = plt.plot(storage['Skaaane'], label = 'Skaaane')
    g, = plt.plot(storage['Vaastra Gootaland'], label = 'Vaastra Gootaland')
    plt.legend(handles = [st, sk, g])

def plot_compare_p2ac(ac_pot, p2ac):
    """ Compare the potential accumulation to the actual.
    """

    plt.figure(7)
    plt.clf()
    pot, = plt.plot(ac_pot, label = 'Potential')
    res, = plt.plot(p2ac, label = 'Outcome')
    plt.legend(handles = [pot, res])