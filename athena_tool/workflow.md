# ATHENA Workflow example on terminal

### Run the docker container

First, boot up the docker container:

```
(base) lgparke@tombstone:~$ docker run -it --rm athena:latest
```

### ATHENA CLI

This is what the `--help` flag current shows for the CLI:

```
root@c74efa9c00b9:/home/ath_usr# athena --help
Usage: athena [OPTIONS] COMMAND [ARGS]...

      ___  ________  _________   ____\|/ ,___, |/|/
     /   |/_  __/ / / / ____/ | / /   |/ (0,0)/ |/_
    / /| | / / / /_/ / __/ /  |/ / /| |/ /)_) |/_
   / ___ |/ / / __  / /___/ /|  / ___ |\_ "" |/_
  /_/  |_/_/ /_/ /_/_____/_/ |_/_/  |_| \|_|/

  Main CLI for using Athena

  To modify architecture configuration, edit the `<arch>_config.yaml` file
  in the architecture folder. This file will define which base architecture
  is chosen, what component files are used, which mapper and constraints are
  applied, and where the outputs should be stored.

  For more information on available commands,
  run `athena <command> --help`.


Options:
  -a, --arch DIRPATH          Folder path to chosen architecture
  -i, --inputs [FILEPATH ..]  Paths of input files to analyze
  -o, --outputs DIRPATH       Redirects the outputs to this folder if
                              specified; the folder must exist before using
                              ATHENA

  -v, --verbose               If verbose flag is set, then a longer summary
                              message is printed and saved to the summary .csv
                              file.

  --help                      Show this message and exit.

Commands:
  init      Initializes ATHENA.
  sanitize  Sanitizes files given their filepaths.
```

### Initialize athena

First, we need to initialize the tool to make sure configurations and package environment are set.

```
root@c74efa9c00b9:/home/ath_usr# athena init
Initializing ATHENA...
File `accelergy_config.yaml` generated.
Added 'table_plug_ins' key to `accelergy_config.yaml`
Adding additional plug-ins to `accelergy_config.yaml`...
  + accelergy-sonos-plug-in to estimator_plug_ins
  + PIM_estimation_tables to table_plug_ins
Updated `accelergy_config.yaml`
```

### Run athena on all vgg layers in verbose mode

After init, we can use the tool to analyze multiple input files and control the verbosity of the summary statement at the end.

Here, we set the verbosity flag `-v` and set the inputs using `-i` by passing all of the vgg layers.

The tool alerts the users of which base architecture is chosen, and checks for additional primitive components to add to the accelergy config file.

It then checks if there are outputs in the output folder (default is used here, but can otherwise be specified), and asks the user if they want to save the previously found files.

I choose 'n' to remove all the current files in the `sonos_pim/outputs` folder, and it tells me.

ATHENA then runs the timeloop-mapper on all of the inputs and prints a summary statement at the end.

The summary statement is saved to a `.csv` file and the details of each layer's run are stored in a `.pkl` file. Logs for each layer are stored in `/outputs/logs`.

```
root@c74efa9c00b9:/home/ath_usr# athena -v -i accelergy_architectures/sonos_pim/vgg/*
Running ATHENA with /home/ath_usr/accelergy_architectures/sonos_pim
  > using `system_SONOS.yaml` as base architecture
Checking primitive components in `accelergy_config.yaml`...

Output files already in outputs, do you want to save them? (y/n): n
Removing contents from output folder...

Calling timeloop-mapper...
  running timeloop on `vgg_layer1`...
    > timeloop-mapper execution took 128.387 seconds
  running timeloop on `vgg_layer2`...
    > timeloop-mapper execution took 129.774 seconds
  running timeloop on `vgg_layer3`...
    > timeloop-mapper execution took 49.738 seconds
  running timeloop on `vgg_layer4`...
    > timeloop-mapper execution took 57.575 seconds
  running timeloop on `vgg_layer5`...
    > timeloop-mapper execution took 52.568 seconds
  running timeloop on `vgg_layer6`...
    > timeloop-mapper execution took 116.147 seconds
  running timeloop on `vgg_layer7`...
    > timeloop-mapper execution took 117.556 seconds
  running timeloop on `vgg_layer8`...
    > timeloop-mapper execution took 160.66 seconds
  running timeloop on `vgg_layer9`...
    > timeloop-mapper execution took 74.302 seconds
  running timeloop on `vgg_layer10`...
    > timeloop-mapper execution took 74.877 seconds
  running timeloop on `vgg_layer11`...
    > timeloop-mapper execution took 46.68 seconds
  running timeloop on `vgg_layer12`...
    > timeloop-mapper execution took 47.333 seconds
  running timeloop on `vgg_layer13`...
    > timeloop-mapper execution took 46.854 seconds
  running timeloop on `vgg_layer14`...
    > timeloop-mapper execution took 47.242 seconds
  running timeloop on `vgg_layer15`...
    > timeloop-mapper execution took 52.152 seconds
  running timeloop on `vgg_layer16`...
    > timeloop-mapper execution took 47.855 seconds

Total runtime took 1249.698630809784 seconds
Summary:
       filename                        problem  utilization   cycles     energy_pJ  energy_per_mac        macs
0    vgg_layer1     [3, 64, 3, 3, 1, 224, 224]     0.002626    50176  2.886150e+09       33.287340    86704128
1    vgg_layer2    [64, 64, 3, 3, 1, 224, 224]     0.056031    50176  9.652946e+11      521.868877  1849688064
2    vgg_layer3   [64, 128, 3, 3, 1, 112, 112]     0.032685    43008  2.541017e+11      274.750884   924844032
3    vgg_layer4  [128, 128, 3, 3, 1, 112, 112]     0.001167  2408448  2.654022e+11      143.484858  1849688064
4    vgg_layer5    [128, 256, 3, 3, 1, 56, 56]     0.002335   602112  9.467273e+11     1023.661539   924844032
5    vgg_layer6    [256, 256, 3, 3, 1, 56, 56]     0.028016   100352  5.611110e+11      303.354414  1849688064
6    vgg_layer7    [256, 256, 3, 3, 1, 56, 56]     0.028016   100352  5.611110e+11      303.354414  1849688064
7    vgg_layer8    [256, 512, 3, 3, 1, 28, 28]     0.074708    18816  1.489750e+11      161.081200   924844032
8    vgg_layer9    [512, 512, 3, 3, 1, 28, 28]     0.130739    21504  2.974902e+11      160.832635  1849688064
9   vgg_layer10    [512, 512, 3, 3, 1, 28, 28]     0.130739    21504  2.974902e+11      160.832635  1849688064
10  vgg_layer11    [512, 512, 3, 3, 1, 14, 14]     0.004669   150528  4.317438e+10       93.365749   462422016
11  vgg_layer12    [512, 512, 3, 3, 1, 14, 14]     0.004669   150528  4.317438e+10       93.365749   462422016
12  vgg_layer13    [512, 512, 3, 3, 1, 14, 14]     0.004669   150528  4.317438e+10       93.365749   462422016
13  vgg_layer14   [25088, 4096, 1, 1, 1, 1, 1]     0.012451    12544  2.059025e+11     2003.713296   102760448
14  vgg_layer15    [4096, 4096, 1, 1, 1, 1, 1]     0.099611      256  3.358803e+10     2002.002691    16777216
15  vgg_layer16    [4096, 1000, 1, 1, 1, 1, 1]     0.038911      160  8.205068e+09     2003.190313     4096000

Verbose summary stored in /home/ath_usr/accelergy_architectures/sonos_pim/outputs/verbose_summary.csv
Detailed summaries of each problem stored in /home/ath_usr/accelergy_architectures/sonos_pim/outputs/detailed_summary.pkl

```
