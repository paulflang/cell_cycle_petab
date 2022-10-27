import pandas as pd
import numpy as np
import os

idxs = range(1, 11)
d = {}
for i in idxs:
    d[i] = pd.read_csv(os.path.join('.', f'parameters_v4.0.0_v{i}.tsv'), sep='\t')

lbs = np.empty((len(d[1]), len(idxs)))
ubs = np.empty((len(d[1]), len(idxs)))
for k, v in d.items():
    lbs[:, k-1] = v.lowerBound
    ubs[:, k-1] = v.upperBound

print(lbs.shape)
lb = np.min(lbs, axis=1)
print(lb.shape)
ub = np.max(ubs, axis=1)

df = (d[10])
df.lowerBound = lb
df.upperBound = ub

df.to_csv(os.path.join('.', f'parameters_v4.0.0_v11_auto.tsv'), sep='\t')
