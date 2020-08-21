# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 15:52:13 2016

@author: Jonatan
"""

from __future__ import division
from Modules.Simulate.sim_p2h import temp_to_heat
import matplotlib.pyplot as plt

cc, dh = temp_to_heat()

# sum up the heat curves for all counties in order to get a total heat curve
# for the whole country
q_tot = sum(cc.values())

plt.close('all')
plt.plot(q_tot)
plt.xlabel('Time [h]')
plt.ylabel('Heat Load [GW]')