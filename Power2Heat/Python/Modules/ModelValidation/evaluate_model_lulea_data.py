# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 09:46:42 2016

@author: Jonatan
"""
from __future__ import division
from read_lulea_data import read_lulea_data
import matplotlib.pyplot as plt
import numpy as np
from Modules.DH.calc_heat_curve import calc_heat_curve 

# read lulea data from file
lulea_data = read_lulea_data()

t = range(len(lulea_data['2012']['q']))

plt.plot(t, lulea_data['2012']['q'])

# Calculate total loads for 2011 and 2012
q_tot = {}
q_tot['2012'] = np.sum(lulea_data['2012']['q'])
q_tot['2011'] = np.sum(lulea_data['2011']['q'])

t_ext = -34

# Use model to simulate data
q = {}
for key,value in q_tot.iteritems():
    q[key], dhl = calc_heat_curve(lulea_data[key]['T'], value, t_ext)

# Compare real data to simulated
plt.clf()
plt.figure(0)
plt.plot(lulea_data['2012']['T'], q['2012'], lulea_data['2012']['T'], lulea_data['2012']['q'], '.')

plt.figure(1)
plt.plot(lulea_data['2011']['T'], q['2011'], lulea_data['2011']['T'], lulea_data['2011']['q'], '.')

mean_diff = {}

# calculate mean error
for key, value in q.iteritems():
    mean_diff[key] = np.mean(np.abs(value - lulea_data[key]['q'])/lulea_data[key]['q'])
    print 'Mean error for', key, 'is:', mean_diff[key]

###
# look for time dependence on hour of day
###
#q_tot_day = np.zeros(24)
#
#for i, q in enumerate(lulea_data['2011']['q']):
#    q_tot_day[np.remainder(i, 24)] += q
#    
#q_mean_day = q_tot_day/365
#plt.figure(3)
#plt.clf()
#plt.plot(q_mean_day)
#
#q_tot_day = np.zeros(24*7)
#
#for i, q in enumerate(lulea_data['2011']['q']):
#    q_tot_day[np.remainder(i, 24*7)] += q
#    if i == 52*7*24 - 1:
#        break
#    
#q_mean_day = q_tot_day/52
#plt.figure(4)
#plt.clf()
#plt.plot(q_mean_day)
#for i in range(7):
#    plt.axvline(i*24) 