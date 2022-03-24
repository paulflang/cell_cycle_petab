import os
import numpy as np
import pandas as pd
import warnings

### Options #################################################
file_dir = '.'  # os.path.dirname(__file__)
version = 'v3.0.1'
sbml_path = os.path.join(file_dir, '..', 'cell_cycle_' + version + '_petab.xml')
bngl_path = os.path.join(file_dir, 'cell_cycle_' + version + '.bngl')
parameter_path = os.path.join(file_dir, 'parameters_' + version + '.tsv')

bngl_out = os.path.join(file_dir, 'cell_cycle_' + version + '_test.bngl')
#############################################################

par_df = pd.read_csv(parameter_path, sep='\t')
 
def parse_line(line):
    line = line[:line.find('#')]
    id, val = line.split(' ', 1)
    val = val.strip('() ')
    if '/' in val:
        operator = '/'
    elif '*' in val:
        operator = '*'
    else:
        operator = None
    vals = val.split(operator) + ['']
    vals = [val.strip() for val in vals]
    val, factor = vals[:2]
    if factor:
        factor = float(factor)
    else:
        operator = ''
    if (not operator) and factor:
        raise Error('Could not recover the operator.')
    if operator and not factor:
        raise Error('Could not recover the factor.')
    return (id.lstrip('\t'), float(val), operator, factor)
    
def get_new_val(id, val, operator, factor):
    if any(char in '()@:,~' for char in id):
        id = id.replace('()', '').replace('@', '_').replace(':', '__')\
            .replace(').', ')_').replace('(', '_').replace(')', '_')\
            .replace(',', '_').replace('~', '').replace('!', '_')
        id = 'ic_wt' + id
    df = par_df.set_index('parameterId')
    if id in df.index:
        val = df.loc[id, 'nominalValue']
    else:
        warnings.warn(f'{id} not found in parameter table')
    if operator == '*':
        new_val = val/factor
    elif operator == '/':
        new_val = val*factor
    else:
        new_val = val
    return new_val
    
# Read BNGL
model = bytearray('', 'utf8')
with open(bngl_path) as f:
    parameter = False
    ic = False
    while True:
        line = f.readline()
        if not line:
            break
        if all(char == ' ' for char in line[:line.find('#')]):
            model.extend(bytes(line, 'utf8'))
            continue
        if 'end parameters' in line:
            parameter = False
        if 'end seed species' in line:
            ic = False
        if parameter:
            id, val, operator, factor = parse_line(line)
            new_val = get_new_val(id, val, operator, factor)
            line = f'\t{id} {new_val}{operator}{factor}\n'
        if ic:
            id, val, operator, factor = parse_line(line)
            new_val = get_new_val(id, val, operator, factor)
            line = f'\t{id} {new_val}{operator}{factor}\n'
        if parameter and ic:
            raise Error('BNGL file corrupted.')
        if 'begin parameters' in line:
            parameter = True
        if 'begin seed species' in line:
            ic = True
        model.extend(bytes(line, 'utf8'))

with open(bngl_out, 'w') as f:
    f.write(model.decode())
