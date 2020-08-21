# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 08:51:49 2016

@author: Jonatan

simulate for one or several scenarios and compare to standard
"""

from __future__ import division
from sim_p2h import temp_to_heat, power_scen_to_res, sim_p2h
from Modules.Compare.read_results import read_results
from Modules.Plot.plot_results import plot_compare_scenarios

# define a scenario, stored in a dictionary
my_scenario = {}

my_scenario["Nuclear"] = 0
my_scenario["Hydro"] = 65
my_scenario["Other"] = 15
my_scenario["Wind"] = 60
my_scenario["Solar"] = 25
my_scenario["Consumption"] = 170

# give a name for your scenario
my_scenario["Name"] = "Jonatan's scenario"

# choose scenario to compare to
comp_scen = 3

# read heat curve
heat_curves, design_heat_loads = temp_to_heat()

# calculate power residual
P_res = power_scen_to_res(scenario = my_scenario)

# simulate P2H, results are written to file
sim_p2h(P_res, heat_curves, design_heat_loads, my_scenario)

# store results in a dictionary
results = {}

# read my scenario
results[my_scenario['Name']] = read_results(my_scenario["Name"])

# read other scenario
results['Scenario_{}'.format(comp_scen)] = read_results(comp_scen)

# compare scenarios
plot_compare_scenarios(results, my_scenario['Name'])


