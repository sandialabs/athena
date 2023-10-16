```
        ______ __________ ____ _____ _______ ______ _____     _______    _\*/    \*/_
       /      |          |    |     |       |      |     |   /       |_\/%%  ,___, %%\/_
      /       |          |    |     |       |      |     |  /        |/%%/  ( 0,0 ) \%%\/_
     /        |_       __|    |     |   ____/      |     | /         |%%|/  /777``) \|%%%|/
    /    +    | |     | |           |       |            |/     +    |%%%| ////```) |%%%%%|/_
   /          | |     | |     |     |   ____/     |      |           |%%%%////___/ /%%%%%|/_
  /     |     | |     | |     |     |       |     |      |     |     |\%%%%---""---%%%%|/_
 /______|_____/ |_____/ |_____|_____/_______/_____|\_____/_____|_____/ \%%%%%%%%%%%%%%/

```

## ATHENA 

ATHENA is an analytical analysis tool for estimation of the performance of dataflow hardware with analog components.
The tool is based on / leverages the [Timeloop](http://github.com/nvlabs/timeloop) system along with the [Accelergy](https://github.com/Accelergy-Project) energy estimation library. 

The tool uses Accelergy to generate computation and data-movement performance look-up tables with analog components, which have a non-linear computational cost when compared to digital components. This table is generated in a Timeloop compatible format, allowing Timeloop to
generate performance estimates for various architectures.

The software uses the Timeloop+Accelergy hardware description format to generate these tables, but with new components which can represent either a complete analog crossbar array or sub-components of a analog crossbar array.

### Design

ATHENA uses static lookup tools to generate performance estimates for a given architecture. In order to support analog devices, which can have non-linear relationships between the number of computations and energy, we support the analog devices as a set of dummy compute units attached to memory components. In an ATHENA component file, a "fat" PE unit consists of a memory layer attached to a pe layer. The memory layer determines the performance of the crossbar array, while the compute layer allows Timeloop to reason about the total number of computations required for a particular unit of computation. 

The performance lookup tabe is generated before the Timeloop instance is run; this process may take a while if there is a large range of energy and latency values that a particular crossbar array reports. Once generated, this table is re-used for each computation with the same components. 


### Documentation

In addition to this document and the [workflow](#workflow) information, we have a documentation page available at ---GITHUB PAGE LINK---.
To build the documentation locally, you will need to build the Sphnx documentation in the `docs` directory.



### Workflow

ATHENA is designed to be built and run within a container, as the suite of dependencies are complex. To use ATHENA to estimate performance of a hardware architecture, please refer to the [Workflow Guide](./athena_tool/workflow.md).

Defining  new architectures requires using a combination of primitive components and larger compound components. The [Accelergy](https://github.com/Accelergy-Project) library and project documentation provides a good and detailed description of the architecture description files. ATHENA specific hardware components are located in the [sonos_pim](./athena_tool/accelergy_architectures/sonos_pim) directory This directory contains primitive component and example large-scale component architectures.


## Contributing

Feel free to contribute to this project. We welcome any and all contributors to make suggestions, report bugs, or provide enhancements. Any issues should be reported in the github repository issues list. For more information, please contact us through the GitHub issue tracker; we are happy to provide more information, or discuss information about this project. 

## Building the Docker Image:

#### Check out this repo:
```
git clone https://github.com/SandiaLabs/ATHENA/athena.git
git submodule init
git submodule update
```

#### Use conda or python3 to create a new virtual environment
```
# using conda
conda create --name docker-setup python=3.9
conda activate docker-setup
pip install -r requirements.txt

# using python3
python3 -m venv docker-setup
source docker-setup/bin/activate
pip install -r requirements.txt
```

#### Create the Dockerfile using the setup script:
```
python docker_setup.py 
```
The options for building are:
- `--proxy/--no-proxy` (sets the SRN proxy by default, otherwise use --no_proxy)
- `--no-user` (toggles permissions and does not set a UID or GID)
- `--uid` (sets the UID for the user, default sets it to 1000)
- `--gid` (sets the GID for the user, default sets it to 1000)
- `--build` (if you want the script to build the docker image for you)
<!-- - `--version_tag` (if you want to set the tag to something other than 'latest') -->
- `--docker_loc` (Path to the docker exe)

#### Build the docker image
```
docker build -t athena:latest .
```

#### Run the container
```
docker run -it --rm athena:latest 
```
For more information about the current state of using ATHENA in the container, see `athena_tool\workflow.md`


## Citing and Papers 

For more information, please see our SAND REPORT / PAPER And cite this:
### 
### CITATION HERE
