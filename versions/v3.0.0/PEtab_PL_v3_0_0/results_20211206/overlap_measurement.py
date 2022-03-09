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
out_file = os.path.join(file_dir, 'duplicated.tsv')
yaml_config = os.path.join(file_dir, 'v3.0.0_plot.yaml')
t_start = 3*3600
t_rep = 5*3600  # duration of the overlap
noise_parameter = 'noiseParameter2'
#############################################################

petab_problem = petab.Problem.from_yaml(yaml_config)
observable_ids = CategoricalDType(np.unique(petab_problem['observableId']), ordered=True)
simulation_condition_ids = CategoricalDType(np.unique(petab_problem['simulationConditionId']), ordered=True)

doubling_time = np.round(np.max(petab_problem['time'])/3600) * 3600
if doubling_time != np.ceil(np.max(petab_problem['time'])/3600) * 3600:
    raise Exception('Could not auto-detect doubling_time.')

# Shift start
start_piece = petab_problem['time'] < t_start
start_df = petab_problem.iloc[start_piece, :]
start_df['time'] = start_df['time'] + doubling_time
middle_df = petab_problem.iloc[not start_piece, :]
t_offset = np.min(middle_df['time'])
df = pd.concat(middle_df, start_df).reset_index()
df['time'] = df['time'] - t_offset

df['observableId'] = df['observableId'].astype(observable_ids)
df['simulationConditionId'] = df['simulationConditionId'].astype(simulation_condition_ids)
df = df.sort_values(['simulationConditionId', 'observableId', 'time'])

# Append duplication
overlap_piece = df['time'] < t_rep
df['noiseFormula'] = noise_parameter
df.loc[overlap_piece, 'noiseFormula'] = '0.5*' + noise_parameter
overlap_df = df.iloc[overlap_piece, :]
overlap_df['time'] = overlap_df['time'] + doubling_time
df = pd.concat(df, overlap_df).reset_index()

df['observableId'] = df['observableId'].astype(observable_ids)
df['simulationConditionId'] = df['simulationConditionId'].astype(simulation_condition_ids)
df = df.sort_values(['simulationConditionId', 'observableId', 'time'])

df.to_csv(out_file, sep='\t', index=False)
print(df)
