import matplotlib
matplotlib.use('Agg')
from amici.petab_simulate import PetabSimulator
import copy
import petab
import os
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

### Options #################################################
file_dir = '.'  # os.path.dirname(__file__)
out_file = os.path.join(file_dir, 'optimisation_rs1')
# res_par = {'file': os.path.join(file_dir, 'PEtab_PLang_problem_v12.xlsx'), 'sheet': 'PEtab_PLANG_real_data_v2_it13', 'best': 'SaCeSS local solver DHC run07'}
yaml_config_plot = os.path.join(file_dir, 'v4.0.0_plot.yaml')
yaml_config = os.path.join(file_dir, '..', 'v4.0.0.yaml')
create_second_cycle = False
#############################################################

# Get parameters (as Series or dict)
# parameter_df = petab.Problem.from_yaml(yaml_config_opt).parameter_df
# res = pd.read_excel(header=29, index_col=0).loc[res_par['best'], :]
# Backtransform parameters
# Plug in and write to *_optimized.tsv

# Simulation
petab_problem = petab.Problem.from_yaml(yaml_config)  # yaml_config_plot)
# petab.flatten_timepoint_specific_output_overrides(petab_problem)

# Second cycle
if create_second_cycle:
    tmp = copy.copy(petab_problem.measurement_df)
    doubling_time = np.round(np.max(tmp['time'])/3600) * 3600
    if doubling_time != np.ceil(np.max(tmp['time'])/3600) * 3600:
        raise Exception('Could not auto-detect doubling_time.')
    tmp['time'] = tmp['time'] + doubling_time
    petab_problem.measurement_df = pd.concat([petab_problem.measurement_df, tmp]).reset_index()
print(1)
print(petab_problem.measurement_df)
print(2)
simulator = PetabSimulator(petab_problem)
print(simulator.working_dir)
print(3)
s = time.time()
optimized_data_df = simulator.simulate()
e = time.time()
print(e-s)
# simulator.remove_working_dir()
print(4)
optimized_data_df.to_csv(out_file + '.tsv', sep='\t', index=False)
print(optimized_data_df)
print(5)

## Plotting
### Options ##########################################################
x_var_name = 'time'
y_var_names = [name for name in petab_problem.observable_df.index]
x_label = 'time (h)'
y_label = 'abundance (AU)'
plt.rcParams['font.size'] = 18
######################################################################

df1 = optimized_data_df.pivot(index='time', columns='observableId', values='measurement')
df2 = petab_problem.measurement_df.pivot(index='time', columns='observableId', values='measurement')

legend_labels = y_var_names
print(6)
# create some data to use for the plot
x = df1.index/3600
y = df1.loc[:, y_var_names] # df.loc[order, y_var_names]
y2 = df2.loc[:, y_var_names]
print(66)
# Determine the size of the figure
print(666)
fig = plt.figure(figsize=(12,10))
print(7)
# the main axes is subplot(111) by default
a = plt.axes([0.15, 0.15, 0.75, 0.75])
a.tick_params(labelsize=14)
sim_lines = plt.plot(x, np.array(y), linewidth=5) # See matplotlib.lines.Line2D for details
a.set_prop_cycle(None) # reset the color cycle
exp_points = plt.plot(x, np.array(y2), 'x')
legend1 = plt.legend(sim_lines, legend_labels, frameon=True, fontsize=14, title='Simulation') #, loc='upper left')
print(8)
plt.legend(exp_points, legend_labels, frameon=True, fontsize=14, loc=2, title='Experiment', title_fontsize=15) #, loc='upper left')
a.add_artist(legend1)
# plt.plot(t, 0.5*s, color=(1, 0, 0), linewidth=3)
plt.xlim(0, np.max(x.max()))
plt.ylim(0, 1.05*np.max(y.max()))
plt.xlabel(x_label, fontsize=18)
plt.ylabel(y_label, fontsize=18)
print(9)
plt.savefig(out_file + '.png')
plt.close()
