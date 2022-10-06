from msilib.schema import Error
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
# file_dir = '.'
base_dir = os.path.join('C:\\', 'Users', 'wolf5212', 'OneDrive - Nexus365', 'DPhil Project', 'Project04_Full cell cycle modelling',
                        'cell_cycle_petab', 'versions')
run = '08'
version = 'v4.0.0'
date = '20220713'
sacess_fn = os.path.join(base_dir, 'PEtab_PLang_problem_v26.xlsx')
parameter_table_fn = os.path.join(base_dir, version, f'parameters_{version}_v1.tsv')

out_file = os.path.join(base_dir, version, f'results_{date}', f'parameters_{version}_optimized.tsv')
#############################################################

# Read in saccess
xl = pd.ExcelFile(sacess_fn)
sheet_names = xl.sheet_names  
last_sheet = sheet_names[-1]
sacess_df = xl.parse(last_sheet, header=29, index_col=0)
res = sacess_df.loc[['lowerBound', 'upperBound',
                     f'SaCeSS local solver DHC run{run}'], :].iloc[:, 1:]
print(res.columns)

# Read in parameters_v*_optimized.tsv
parameter_df = pd.read_csv(parameter_table_fn, sep='\t')

# Update lowerBoundary, upperBoundary and nominalValue
df = copy.copy(parameter_df)
count = 0
for i in range(len(parameter_df)):
    par_id = parameter_df.loc[i, 'parameterId']  
    # Update nominalValue
    if par_id in res.columns:
        print(par_id)
        lb_ub = list(res[par_id].iloc[[0,1]])
        if parameter_df.loc[i, 'estimate'] != 1:
            raise Exception(f'Parameter {par_id} should not have been estimated.')
        val = res[par_id].iloc[2]
        if parameter_df.loc[i, 'parameterScale'] == 'log':
            val = np.exp(val)
            lb_ub = [np.exp(x) if x != '"-inf"' else 0. for x in lb_ub]
        elif parameter_df.loc[i, 'parameterScale'] == 'log10':
            val = 10**val
            lb_ub = [10**x if x != '"-inf"' else 0. for x in lb_ub]
        elif parameter_df.loc[i, 'parameterScale'] != 'lin':
            scale = parameter_df.loc[i, 'parameterScale']
            raise Error(f'parameterScale must be either `lin`, `log` or `log10`, but is {scale}.')
        df.loc[i, 'nominalValue'] = val
        # Update bounds
        nominal = parameter_df.loc[i, 'nominalValue']
        if nominal != 0 and par_id[0] != 'o':
            lb, ub = lb_ub
            if val < 1.01 * lb:
                new_bounds = [nominal/(ub/lb), nominal]
                count += 1
            elif val > ub / 1.01:
                new_bounds = [nominal, ub*(ub/lb)]
                count += 1
            else:
                new_bounds = [lb, ub]
            df.loc[i, 'lowerBound'] = new_bounds[0]
            df.loc[i, 'upperBound'] = new_bounds[1]

print(f'Shifted {count} boundaries.')
df.to_csv(out_file, sep='\t', index=False)
