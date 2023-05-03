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
base_dir = os.path.join(os.path.dirname(__file__), '..', '..')
run = '05'
par_row = 30
version = 'v4.0.0'
date = '20230321'
sacess_fn = os.path.join(base_dir, 'PEtab_PLang_problem_v41.xlsx')
parameter_table_fn = os.path.join(base_dir, version, f'parameters_{version}_v16.tsv')

out_file = os.path.join(base_dir, version, f'results_{date}', f'parameters_{version}_optimized.tsv')
#############################################################

# Read in saccess
xl = pd.ExcelFile(sacess_fn)
sheet_names = xl.sheet_names
last_sheet = sheet_names[-1]
print(f'Reading sheet {last_sheet}.')
sacess_df = xl.parse(last_sheet, header=par_row, index_col=0)
res = sacess_df.loc[['lowerBound', 'upperBound',
                     f'SaCeSS local solver DHC run{run}'], :].iloc[:, 1:]

# Read in parameters_v*_optimized.tsv
parameter_df = pd.read_csv(parameter_table_fn, sep='\t')

# Update lowerBoundary, upperBoundary and nominalValue
df = copy.copy(parameter_df)
active_lb = []
active_ub = []
found_header = 0
for i in range(len(parameter_df)):
    par_id = parameter_df.loc[i, 'parameterId']
    # Update nominalValue
    if par_id in res.columns:
        found_header += 1
        lb_ub = list(res[par_id].iloc[[0,1]])
        if parameter_df.loc[i, 'estimate'] != 1:
            raise Exception(f'Parameter {par_id} should not have been estimated.')
        val = res[par_id].iloc[2]
        if parameter_df.loc[i, 'parameterScale'] == 'log':
            val = np.exp(float(val))
            lb_ub = [np.exp(x) if x not in ['"-Inf"', '"-inf"'] else 0. for x in lb_ub]
        elif parameter_df.loc[i, 'parameterScale'] == 'log10':
            val = 10**val
            lb_ub = [10**x if x not in ['"-Inf"', '"-inf"'] else 0. for x in lb_ub]
        elif parameter_df.loc[i, 'parameterScale'] != 'lin':
            scale = parameter_df.loc[i, 'parameterScale']
            raise Error(f'parameterScale must be either `lin`, `log` or `log10`, but is {scale}.')
        df.loc[i, 'nominalValue'] = val
        # Update bounds
        nominal = parameter_df.loc[i, 'nominalValue']
        if par_id[0] != 'o':
            lb, ub = lb_ub
            if lb != 0 and val < 1.01 * lb:
                new_bounds = [nominal/(ub/lb), nominal]
                active_lb.append(par_id)
                print(f'lb: {par_id}')
            elif val > ub / 1.01:
                if lb != 0:
                    new_bounds = [nominal, nominal*(ub/lb)]
                else:
                    new_bounds = [nominal, nominal*100]
                active_ub.append(par_id)
                print(f'ub: {par_id}')
            else:
                new_bounds = [lb, ub]
            df.loc[i, 'lowerBound'] = new_bounds[0]
            df.loc[i, 'upperBound'] = new_bounds[1]

print(f'Found {found_header} parameters.')
if found_header != len(res.columns) or found_header == 0:
    raise Exception(f'Found {found_header} parameters, but expected {len(res.columns)}. Check `par_row`.')

ab_report = f'Shifted {len(active_lb)} lower and {len(active_ub)} upper boundaries.'
print(ab_report)
with open(os.path.join(base_dir, version, f'results_{date}', 'active_bounds.txt'), 'w') as f:
    f.write(ab_report)
df.to_csv(out_file, sep='\t', index=False)
