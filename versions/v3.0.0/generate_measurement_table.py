from amici.petab_simulate import PetabSimulator
import petab
import os
import time

dir_name = os.path.dirname(__file__)
petab_dir = os.path.join(dir_name, 'PEtab_PL_v3_0_0_mock')
out_file = os.path.join(petab_dir, 'simulationData_v3.0.0.tsv')
yaml_config = os.path.join(petab_dir, 'v3.0.0.yaml')

petab_problem = petab.Problem.from_yaml(yaml_config)

simulator = PetabSimulator(petab_problem)
print(simulator.working_dir)

s = time.time()
synthetic_data_df = simulator.simulate()
e = time.time()
print(e-s)

s = time.time()
synthetic_data_df = simulator.simulate()
e = time.time()
print(e-s)
simulator.remove_working_dir()

synthetic_data_df.to_csv(out_file, sep='\t')
