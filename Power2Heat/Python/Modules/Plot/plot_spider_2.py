# -*- coding: utf-8 -*-
"""
Created on Mon May 09 08:58:28 2016

@author: Jonatan
"""

from __future__ import division
from spider_plot_2 import *

def p2h_spider():
    """ Make a spider plot where the different scenarios are compared
    for different scenarios.
    """
    
    d = Drawing(400, 400)
    sp = SpiderChart()
    sp.x = 50
    sp.y = 50
    sp.width = 300
    sp.height = 300
    sp.data = [[1, 2, 3], [8, 3, 5], [5, 9, 1]]
    sp.labels = ['Base case', 'Hydro min = 0', 'With accumulation']
    sp.strands.strokeWidth
    d.add(sp)
    return d
    
if __name__ == '__main__':
    d = p2h_spider()
    from reportlab.graphics.renderPDF import drawToFile
    drawToFile(d, 'p2h_spider.pdf')