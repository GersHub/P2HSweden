# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 08:50:51 2016

@author: Jonatan

Goal: Construct a case where you would have liked to take heat from both
        accumulators if it was available, but because of the regional
        restrictions, you only take heat from the one relevant
"""

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from Modules.Accumulation.simulation import sim
from Modules.Results.plot_results import plot_compare_p2h

# make up demand data for two DH networks
q_dict = {'lund':     np.array([3, 26, 27, 23, 20, 20, 20, 9, 3, 4])}

# make up power data
P_res = np.array([8, 5, 7, 2, 1, 0, 500, 0, 7, 0])

# set accumulation transfer limits
transfer_limits = {}
for city in q_dict:
    transfer_limits[city] = 1000

result = sim(q_dict, P_res, transfer_limits)

storage = result['storage']
acs = result['acs']

for index, q in storage['lund']:
    if q > storage['lund'][index] + P_res[index]:
        if storage['lund'][index]

# now redo the same test but now with a limited transfer to and
# from the accumulator

q_dict['lund_lim_transfer'] = q_dict.pop('lund')
result2 = sim(q_dict, P_res)

storage.update(result2['storage'])
acs.update(result2['acs'])


for key, value in acs.iteritems():
    print key,  'accumulator has storage capacity', value.max_storage, \
                'GWh and transfer capacity', value.max_transfer, 'GW'
                
plt.plot(1)
plt.clf()
for key, value in storage.iteritems():
    plt.plot(value/acs[key].max_storage, label = key)
plt.legend(bbox_to_anchor = (0, 1))
plt.ylabel('Storage [%]')
plt.xlabel('Time [h]')
plt.ylim(-0.1, 1.1)

                
            
        
        

