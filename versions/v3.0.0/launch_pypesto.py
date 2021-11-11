import pypesto
import pypesto.petab
import pypesto.optimize as optimize
import os
import numpy as np

dir_name = os.path.dirname(__file__)
yaml_config = os.path.join(dir_name, 'PEtab_PL_v3_0_0', 'v3.0.0.yaml')

importer = pypesto.petab.PetabImporter.from_yaml(yaml_config)
objective = importer.create_objective(guess_steadystate=False)
problem = importer.create_problem(objective)

optimizer = optimize.ScipyOptimizer()

# engine = pypesto.engine.SingleCoreEngine()
engine = pypesto.engine.MultiProcessEngine()

optimize_options = optimize.OptimizeOptions(startpoint_resample=True)

# do the optimization
result = optimize.minimize(problem=problem, optimizer=optimizer,
                           n_starts=1, engine=engine, options=optimize_options)
