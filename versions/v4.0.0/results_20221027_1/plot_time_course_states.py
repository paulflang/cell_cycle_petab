import matplotlib
matplotlib.use('Agg')
from amici.petab_simulate import PetabSimulator
from amici.petab_objective import simulate_petab
import copy
import petab
import os
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

### Options #################################################
file_dir = '.'  # os.path.dirname(__file__)
out_file = os.path.join(file_dir, 'optimisation_states')
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
petab_problem = petab.Problem.from_yaml(yaml_config_plot)  # yaml_config_plot)
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
res = simulator.simulate()
amici_model = simulator.amici_model
res = simulate_petab(petab_problem, amici_model)
rdata = res['rdatas'][0].x

resmat = np.empty((len(rdata), len(rdata[0])))
for i in range(len(rdata)):
    resmat[i, :] = rdata[i]

sn = amici_model.getStateNames()
df = pd.DataFrame(data=resmat, columns=sn)

print(df)
df.to_csv(os.path.join(file_dir, 'results_20221027_1_states.csv'))
