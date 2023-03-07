import os
import petab
from libsbml import writeSBMLToFile
base_dir = os.path.dirname(os.path.abspath(__file__))

# Options
fig2yaml = {
    "Figure 9": os.path.join(base_dir, "v4.0.0", "results_20230307", "v4.0.0_plot.yaml"),
    "Figure S10": os.path.join(base_dir, "v3.0.1", "results_20220421", "v3.0.1_plot.yaml"),
    "Figure S11": os.path.join(base_dir, "v3.2.0", "results_20220421", "v3.2.0_plot.yaml")
    }

for yaml in fig2yaml.values():
    # Load PEtab problem
    petab_problem = petab.Problem.from_yaml(yaml)
    doc = petab.sbml.get_model_for_condition(petab_problem, "wt")[0]
    doc.setLevelAndVersion(3, 1)
    model = doc.getModel()
    for s in model.getListOfSpecies():
        s.setHasOnlySubstanceUnits(True)
    fn = os.path.splitext(yaml)[0].rstrip("plot") + "optimized.sbml"
    writeSBMLToFile(doc, fn)
