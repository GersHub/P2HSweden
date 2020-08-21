# -*- coding: utf-8 -*-
"""
Created on Mon May 09 09:11:04 2016

@author: Jonatan
"""

from __future__ import division
from spider_plot import *
import matplotlib.pyplot as plt


def p2h_results():
    """ Specifies the data to be plotted, placed in one vector for each
    scenario.
    """
    results = [
        ['Base Case', 'Ex waste', 'With Ac',
         'With Ac, ex waste',
         'Power Cons = 125', 'Power Cons = 170', 'Wind Year 2013',
         'Wind Year 2015'],
         'P2H results', [
                [6.19, 3.77, 8.50, 5.39, 8.60, 3.10, 6.82, 5.38],
                [3.67, 2.94, 4.00, 3.49, 5.75, 1.47, 4.58, 3.07],
                [1.94, 1.23, 2.05, 1.54, 4.74, 0.19, 3.10, 2.56]]            
            ]
    
    return results
    
    
    
if __name__ == '__main__':

    plt.close('all')    
    
    N = 8
    theta = radar_factory(N, frame = 'polygon')
    
    data = p2h_results()
    spoke_labels = data.pop(0)
    
    fig = plt.figure()
    
    colors = ['g', 'r', 'b']
    ax = fig.add_subplot(1, 1, 1, projection = 'radar')
    
    for d, color in zip(data[1], colors):
        ax.plot(theta, d, color = color)
        ax.fill(theta, d, facecolor = color, alpha = 0.25)
    ax.set_varlabels(spoke_labels)
    
    # add legend
    plt.subplot(1, 1, 1)
    labels = ('High W & S', 'High Wind', 'Conservative')
    legend = plt.legend(labels, loc = (0.85, 0.93), labelspacing = 0.1)
    
    #plt.title('Summary of P2H potential results [TWh] ')
        