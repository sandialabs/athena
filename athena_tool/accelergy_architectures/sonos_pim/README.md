# SONOS PIM Architecture Files

This folder contains the relevant configuration files that are used by Timeloop/Accelergy in the ATHENA tool. For more information on ATHENA, see `athena/athena_tool/workflow.md`. Some details about each folder:

- `/arch`: the YAML files describing the architecture and its associated components
- `/constraints`: describes additional constraints that speed up the mapping
- `/PIM_estimation_tables`: contains the necessary technology data for estimating the specific example architecture
- `/mapper`: contains the mapspace exploration knobs

It also contains the VGG16 network problem in `/vgg` that is used for testing. When using ATHENA, the outputs are stored inside `/outputs` by default, but the user may optionally store the output in a different folder.

Inside of `/outputs` is the data of interest after running the ATHENA tool on a given problem. After the run, the following is generated inside `/outputs` for analysis:

##### `detailed_summary.pkl`

A nested list stored in a `pkl` file that contains the most detailed information about each of the layers passed as input to ATHENA. After loading the pickle file, the stats for a layer can be accessed by `layer_stats = stats[layer_name]`, where layer name might be 'vgg_layer9' or otherwise. This will return a nested dictionary that has each level of the layer as its first key and each stat as its second key, e.g. `layer_stats[level_name][stat]`. The following stats are saved:
  - `energy` 
  - `storage_access_energy`
  - `read_energy`
  - `spatial_add_energy`
  - `temporal_add_energy`
  - `addr_generation_energy`
  - `network_energy`
  - `energy_per_access_per_instance`
  - `reads_per_instances`
  - `updates_per_instances`
  - `fills_per_instances`
  - `accesses_per_instances`
  - `instances`
  - `utilization`
  - `multicast`
  - `dist_multicast`
  - `num_hops`
  - `ingresses`
  - `energy_per_hop_per_instance`

Again, each of these statistics and unique to the level of one of the layers included in the  list of ATHENA input files.

##### `*_summary.csv`
The summary file will either be named `short_summary.csv` or `verbose_summary.csv` depending on the verbosity flag of ATHENA (`-v`). This file stores a dataframe that summarizes the totals of all levels in the detailed summary, which is saved to the `.csv` from a pandas DataFrame. It can easily be imported to a notebook or script for quick comparison on the highest level stats of each layer. 

##### `/logs`
This folder will contains logs for each of the layers provided to ATHENA as input. Inside of each log will be the ACCELERGY and TIMELOOP stdout/stderr that is printed when calling the timeloop-mapper tool, as it is all redirected to this file. It can be used for debugging when the ATHENA tool prints no stats or does something else that is unexpected. It also records the execution time for the timeloop-mapper on each layer.
