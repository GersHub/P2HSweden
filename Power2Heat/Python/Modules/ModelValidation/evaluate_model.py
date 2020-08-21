# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 09:46:42 2016

@author: Jonatan
"""
from __future__ import division
from read_Kraftringen_data import read_Kraftringen_data, lin_int_nan
import matplotlib.pyplot as plt
import numpy as np
from Modules.DH.calc_heat_curve import calc_heat_curve 
from scipy import optimize

# read Kraftringen data from file
k_data = read_Kraftringen_data()

def lin_int(q, t_start, t_end):
    """ replace section of data by linear interpolation between
    boundary values
    """
    q[t_start:t_end] = np.linspace(q[t_start], q[t_end], t_end - t_start) 
    return q       

plt.plot(k_data['lund'])

# make a list of tuples containing start and end indices for periods of
# outliers
out_index = [(4930, 5002), (5747, 5912), (6015, 6017), (6086, 6089), 
             (6578, 6596)]
             
for tup in out_index:
    k_data['lund'] = lin_int(k_data['lund'], tup[0], tup[1])
    
plt.plot(k_data['lund'])

t = range(len(k_data['lund']))

#plt.plot(t, k_data['lund'])

# Calculate total loads for Lund, Lomma and Eslöv
q_tot = {}
q_tot['lund'] = np.sum(k_data['lund'])
q_tot['eslov'] = np.sum(k_data['eslov'])
q_tot['lomma'] = np.sum(k_data['lomma'])

t_ext = -16

# Use model to simulate data
q = {}
for key,value in q_tot.iteritems():
    heat_curve, design_heat = calc_heat_curve(k_data['T'], value, t_ext)
    q[key] = heat_curve

# Compare real data to simulated, plotting against temperature
plt.figure(0)
real_data, = plt.plot(k_data['T'], k_data['lund'], '.', label='Kraftringen data')
sim_data, = plt.plot(k_data['T'], q['lund'], '.', label = 'Simulated data')
plt.xlabel('Temperature [$^\circ$C]')
plt.ylabel('DH heat demand [MW_th]')
plt.title('Lund data')
plt.legend(handles=[real_data, sim_data])

plt.figure(1)
plt.plot(k_data['T'], k_data['lomma'], '.', k_data['T'], q['lomma'], '.')


mean_diff = {}

# calculate mean error
for key, value in q.iteritems():
    mean_diff[key] = np.mean(np.abs(value - k_data[key])/k_data[key])
    print 'Mean error for', key, 'is:', mean_diff[key]
    
# make linear regression for real heat demand as function of temperatures ?

    

##
# look for time dependence on hour of day
##
#q_tot_day = np.zeros(24)
#
#for i, q in enumerate(k_data['lund']):
#    q_tot_day[np.remainder(i, 24)] += q
#    
#q_mean_day = q_tot_day/365
#plt.figure(3)
#plt.clf()
#plt.plot(q_mean_day)
#plt.plot(np.mean(k_data['lund'])*np.ones(24))
#
#
#q_tot_day = np.zeros(24*7)
#
#for i, q in enumerate(k_data['lund']):
#    q_tot_day[np.remainder(i, 24*7)] += q
#    if i == 52*7*24 - 1:
#        break
#    
#q_mean_day = q_tot_day/52
#plt.figure(4)
#plt.clf()
#plt.plot(q_mean_day)
#plt.plot(np.mean(k_data['lund'])*np.ones(24*7))
#for i in range(7):
#    plt.axvline(i*24) 



# make piecewise linear regression

def piecewise_linear(x, y0, k1, k2):
    return np.piecewise(x, [x < 15], [lambda x:k1*x + y0-k1*15, lambda x:k2*x + y0-k2*15])
    
for key in k_data:
    p , e = optimize.curve_fit(piecewise_linear, k_data['T'], k_data[key])
    xd = np.linspace(-20, 30, 100)
    plt.figure(5)
    plt.clf()
    plt.plot(k_data['T'], k_data[key], "o")
    plt.plot(xd, piecewise_linear(xd, *p))    
    
    mean_diff_perfect_lin ={}
    
    # calculate mean error
    mean_diff_perfect_lin = np.mean(np.abs(piecewise_linear(k_data['T'], *p) - k_data[key])/k_data[key])
    print 'Mean error for perfect lin reg for', key, ' is:', mean_diff_perfect_lin

# plotting against fraction of power residual?

####
## plotting over time
####

#plt.figure(2)
##plt.plot(t[:24*7], k_data['T'][:24*7], t[:24*7], k_data['lund'][:24*7])
#
#fig, ax1 = plt.subplots()
#ax1.plot(t[:24*7], k_data['T'][:24*7], 'b-')
#ax1.set_xlabel('time (s)')
## Make the y-axis label and tick labels match the line color.
#ax1.set_ylabel('Temperature', color='b')
#for tl in ax1.get_yticklabels():
#    tl.set_color('b')
#
#
#ax2 = ax1.twinx()
#ax2.plot(t[:24*7], k_data['lund'][:24*7], 'r')
#ax2.set_ylabel('DH heat demand', color='r')
#for tl in ax2.get_yticklabels():
#    tl.set_color('r')
#    
#for i in range(7):
#    plt.axvline(i*24)    
#    
#plt.show()
