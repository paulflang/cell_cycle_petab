import os
import pandas as pd
import re


base_dir = os.path.dirname(os.path.realpath(__file__))
subsdict = {"Figure 8": (os.path.join(base_dir, "v3.0.0", "cell_cycle_v3.0.0_rescaled.bngl"),
                         os.path.join(base_dir, "v3.0.0", "PEtab_PL_v3_0_0sim", "cell_cycle_v3.0.0_rescaled_sbml.xml"),
                         os.path.join(base_dir, "v3.0.0", "PEtab_PL_v3_0_0sim", "results_20211130", "parameters_v3.0.0_optimized.tsv")),
            "Figure 9": (os.path.join(base_dir, "v4.0.0", "cell_cycle_v4.0.0.bngl"),
                         os.path.join(base_dir, "v4.0.0", "cell_cycle_v4.0.0rs_petab.xml"),
                         os.path.join(base_dir, "v4.0.0", "results_20230120", "parameters_v4.0.0_optimized.tsv"))
                         }

def petabify(text):
    text = re.sub('[^<]'+'!', lambda matchobj: matchobj.group(0)[0]+'_', text)
    text = re.sub('<model id="[a-zA-Z_0-9.]+">', lambda matchobj: re.sub('v[0-9].[0-9].[0-9]', lambda matchobj: matchobj.group(0).replace('.', '_'), matchobj.group(0)), text)
    text = text.replace('()', '').replace('@', '_').replace(':', '__')\
            .replace(').', ')_').replace('(', '_').replace(')', '_')\
            .replace(',', '_').replace('~', '')
    return text

# Read in every line of the bngl, recognise parameter and initial conditionns, and replace them with the values from the tsv
def update_bngl(bngl, tsv):
    with open(bngl, 'r') as f:
        lines = f.readlines()
    par_df = pd.read_csv(tsv, sep='\t')
    for i, line in enumerate(lines):
        if line.startswith('begin parameters'):
            start = i
        elif line.startswith('end parameters'):
            end = i
        elif line.startswith('begin seed species'):
            start_u0 = i
        elif line.startswith('end seed species'):
            end_u0 = i
    counter = 0
    for i, line in enumerate(lines):
        if i > start and i < end:
            par_id = line.split()[0]
            row = par_df.parameterId == par_id
            if sum(row) == 1:
                val = par_df.loc[row, "nominalValue"].iloc[0]
                lines[i] = f'\t{par_id} {val}\n'
                counter += 1
            elif par_id != '#':
                raise Exception(f'{par_id} not found in parameter table')
    print(f'Updated {counter} parameters in {bngl}')
    
    counter = 0
    for i, line in enumerate(lines):
        if i > start_u0 and i < end_u0:
            mol_id = line.split()[0]
            mol_id = 'ic_wt' + petabify(mol_id)
            if mol_id == 'ic_wt_Cyt__CCNB_CDKN1A_CDK1_Thr14_Tyr15u_':
                mol_id = 'ic_wt_Cyt__CCNB_CDK1_Thr14_Tyr15u_CDKN1A_'
            row = par_df.parameterId == mol_id
            if sum(row) == 1:
                val = par_df.loc[row, "nominalValue"].iloc[0]
                lines[i] = f'\t{mol_id} {val}\n'
                counter += 1
            elif par_id != '#':
                raise Exception(f'{mol_id} not found in parameter table')
    print(f'Updated {counter} initial conditions in {bngl}')
    
    outfile = os.path.splitext(bngl)[0] + '_optimized.bngl'            
    with open(outfile, 'w') as f:
        f.writelines(lines)
                         
for key, value in subsdict.items():
    bngl, sbml, tsv = value
    update_bngl(bngl, tsv)
    # update_sbml(sbml, tsv)
    
