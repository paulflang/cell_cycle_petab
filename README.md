# `cell_cycle_petab`

[![DOI](https://zenodo.org/badge/426996673.svg)](https://zenodo.org/badge/latestdoi/426996673)

`cell_cycle_petab` is a repository that stores several cell cycle model versions and their corresponding PEtab problems. The data in the measurement tables stems from snapshot measurements by [Stallaert et al. (2021)](https://github.com/paulflang/cell_cycle_time_course/blob/main/4i_stallaert/raw.md) in RPE1 cells. Pseudo-time courses were reconstructed with [reCAT](https://github.com/tinglab/reCAT). Visualisations of these time courses can be found in the [cell_cycle_time_course](https://github.com/paulflang/cell_cycle_time_course) repository. The model generation process is documented in the [cell_cycle_model](https://github.com/paulflang/cell_cycle_model) repository. For further details, please refer to [Paul Lang's dissertation](https://ora.ox.ac.uk/objects/uuid:888439ad-99ac-4e89-9473-cc4864cf1e94).

![journal pcbi 1011151 g007](https://github.com/user-attachments/assets/91efd64d-4029-41a7-ab6f-fb310962bc9f)

## Models

Models are of different degree of complexity.

* v2.1.4: basic cell cycle model in SBML format.
* v3.0.0: same as v2.1.4 in BNGL.
* v3.0.1: added refinements to reaction rules of v3.0.0.
* v3.1.0: added DNA damage checkpoint (SKP2 and TP53 and CDKN1A).
* v3.2.0: added CDKN1B.
* v4.0.0: added compartments.


## Navigating the repository

This repository contains a `/versions/` directory with subdirectories for the versions mentioned above and Excel documents containing the raw output of the saCeSS optimiser. The `/versions/v*` directories contain YAML files specifying the PEtab problem for the latest optimisation run. Often, preliminary runs had do be performed to refine the optimisation procedure (e.g. updating bounds). Files in `/versions/v*` that are not mentioned in the YAML file were typically used for preliminary runs.

### The `/versions/v*results_/` directories

The `/versions/v*results_/` directories often contain a `sacess_to_petab.py` script, which extracts an optimisation result from Excel (saCeSS raw output) and plugs them as `nominalValues` into a `parameters_v*_optimized.tsv` file. `plot_time_cours.py` scripts simulate the results and produce an `optimisation.tsv` file. Sometimes (manual) modifications such as removing noise parameters from the parameter and observable tables were necessary to run the simulation. `plot_sacess_*_manu.py` scripts use the `optimisation.tsv` file to plot figures in manuscript quality.

## Manuscript figures

Figures for the manuscript *Reusable rule-based cell cycle model explains compartment-resolved dynamics of 16 observables in RPE-1 cells* that show fits of PEtab problems to RPE1 cells can be plotted with the following scrips:

- [Figure 6](/versions/v4.0.0/results_20230414/v4.0.0_manu.png):
    - [`/versions/v4.0.0/results_20230414/plot_sacess_400_manu.py`](/versions/v4.0.0/results_20230414/plot_sacess_400_manu.py)
- [Supplementary Figure 11](/versions/v3.0.1/results_20220421/v3.0.1_manu.png):
    - [`/versions/v3.0.1/results_20220421/plot_sacess_301_manu.py`](/versions/v3.0.1/results_20220421/plot_sacess_301_manu.py)
- [Supplementary Figure 12](/versions/v3.2.0/results_20220421/v3.2.0_manu.png):
    - [`/versions/v3.2.0/results_20220421/plot_sacess_320_manu.py`](/versions/v3.2.0/results_20220421/plot_sacess_320_manu.py)

## Barebones SBML models fitted to RPE1 data

Barebones SBML files with parameters optimized to fit the time courses of RPE1 cells can be found for the following model versions:
- [v3.0.1](/versions/v3.0.1/results_20220421/v3.0.1_optimized.sbml)
- [v3.2.0](/versions/v3.2.0/results_20220421/v3.2.0_optimized.sbml)
- [v4.0.0](/versions/v4.0.0/results_20230414/v4.0.0_optimized.sbml)

# Citation

If you use this repository in your research, please cite [this paper](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1011151):

```
@article{lang_reusable_2024,
	title = {Reusable rule-based cell cycle model explains compartment-resolved dynamics of 16 observables in {RPE}-1 cells},
	doi = {10.1371/journal.pcbi.1011151},
	journal = {PLOS Computational Biology},
	author = {Lang, Paul F. and Penas, David R. and Banga, Julio R. and Weindl, Daniel and Novak, Bela},
	year = {2024},
}
```
