# User Guide P2H Python package

## Run simulations and compare results

Before you can run sim_scenarios you have to run in python:

* `import sys`
* `sys.path.append(r”…\Power2Heat\Python”)`

To make a basic simulation, one can use the `Power2Heat/Python/Modules/Simulate/sim_p2h` script. Just specify at the bottom which scenario to use ( e.g. scenario = ‘High Wind’) and run. However, in order to run several different simulations and compare the results, one can also use the other scripts under `Modules/Simulate` and `Modules/Compare` respectively.
Run `sim_scenarios` to simulate the base case for all scenarios and save the hourly P2H potential to file. Then run `compare_scenarios` (found in Modules/Compare) to plot/print results. The plot/plots are saved to file in the folder `“…/Pwer2Heat/Python/Plots”`.
Analog with:

* `sim_waste_excluded/compare_waste_excluded`
* `sim_ac/compare_ac` (here decide if you want to exclude waste or not, by setting exclude_waste to True or False)
* `sim_hydro/compare_hydro`
* `sim_wind_solar_yr/compare_wind_solar_yr`

The files for a simulation with a cost optimal level of installed electric boilers sim_cost/compare_cost are located in the Cost folder (Modules/Cost). To make a plot of the profit use the `cost_opt` script from the same folder. The parameters for the cost calculations are set in the `cost_opt` script, in functions `annualize and `calc_profit`.
`
## Overview
The P2H simulation can be divided into three principal steps, where each step has its corresponding function (function name given in parenthesis): 

1.	calculate hourly heat demand for each region (temp_to_heat)
2.	calculate hourly power residuals and (power_scen_to_res)
3.	calculate hourly P2H potential (sim_p2h)

To give an overview of how the simulations work, each of these functions is explained in a flow chart, see Figure 1, 2 and 3 (these flow charts are also found as a power point presentation in the repository under the Python folder, where they can be edited). The charts show the different (sub-) functions that make up the larger functions, in red and blue rectangles. The arrows indicate that the output from one function is used at input for another (note that in Figure 3, sim_ac is a “subscript” to sim_p2h, wherefore a different type of arrow is chosen). In green ovals are the in-data and in purple rectangles are parameters that are set dependent on the simulation. The yellow rectangles with rounded corners frame results. The triangle in Figure 3 marks a class/object. To understand more the function of each function, read the description in the function head (in the Python code).
The followinng figure describes the temp_to_heat script, going from temperature data and annual DH loads to hourly heat demands for each region:

![Image One](https://github.com/GersHub/P2HSweden/blob/master/Power2Heat/User%20guide/Pics/on.png)

The followinng figure describes the power_scen_to_res script, calculating the hourly power residual based on scenario data and historic power data.
![Image Two](https://github.com/GersHub/P2HSweden/blob/master/Power2Heat/User%20guide/Pics/two.png)

The followinng figure describes the sim_p2h script, which uses hourly heat loads and power residuals to calculate the hourly P2H potential.
![Image Three](https://github.com/GersHub/P2HSweden/blob/master/Power2Heat/User%20guide/Pics/three.png)

## Model Validation
The scripts `evaluate_model` and `evaluate_model_lulea_data` in the folder Modules/ModelValidation evaluate the model relating outdoor temperatures to heat loads, by comparing the simulated results to historic data. Mean errors are printed to terminal.

## Testing
The Modules/Testing folder contain a series of tests for the accumulator model. All tests can be run by the script `perform_tests`, which prints True for every test that is successful.

## Plot
The Modules/Plot folder contains different scripts and functions for plotting. In order to print hourly power or power residuals, use the script `plot_power`. In order to plot wind, solar or export data for years 2011-2015, use the `yr_data_analysis` and `specify Wind_data.csv`, `Solar_data.csv` or Export_data.csv as argument. To make a plot comparing of power residual against heat demand for different hours, the easiest way right now is to run the `sim_p2h` for your desired scenario. This will give the desired plot and much more.
