# `cell_cycle_petab`

`cell_cycle_petab` is a repository that stores several cell cycle model versions and their corresponding PEtab problems. The data in the measurement tables stems from snapshot measurements by [Stallaert et al. (2021)](https://github.com/paulflang/cell_cycle_time_course/blob/main/4i_stallaert/raw.md). Pseudo-time courses were reconstructed with [reCAT](https://github.com/tinglab/reCAT). Visualisations of these time courses can be found in the [cell_cycle_time_course](https://github.com/paulflang/cell_cycle_time_course) repository. The model generation process is documented in the [cell_cycle_model](https://github.com/paulflang/cell_cycle_model) repository. For further details, please refer to [Paul Lang's dissertation](https://drive.google.com/file/d/1J0tyVIgoCnaQKdi5yIieM0VjRXsm6spA/view?usp=sharing).

## Models

Models are of different degree of complexity.

* v2.1.4: basic cell cycle model in SBML format.
* v3.0.0: same as v2.1.4 in BNGL.
* v3.0.1: added refinements to reaction rules of v3.0.0.
* v3.1.0: added DNA damage checkpoint (SKP2 and TP53 and CDKN1A).
* v3.2.0: added CDKN1B.
* v4.0.0: added compartments.
