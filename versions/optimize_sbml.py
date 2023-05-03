import os
import petab
from libsbml import writeSBMLToFile
base_dir = os.path.dirname(os.path.abspath(__file__))

# Options
fig2yaml = {"Figure 9": os.path.join(base_dir, "v4.0.0", "results_20230120", "v4.0.0_plot.yaml")}

for yaml in fig2yaml.values():
    # Load PEtab problem
    petab_problem = petab.Problem.from_yaml(yaml)
    doc = petab.sbml.get_model_for_condition(petab_problem, "wt")
    fn = os.path.splitext(yaml)[0].rstrip("plot")
    writeSBMLToFile(doc[0], fn + "optimized.sbml")
