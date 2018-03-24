# CTS-and-Converter-Scripts

This repo includes scripts for clock tree synthesis, power network synthesis, rc2spef conversion, blif2def conversion

## Clock Tree Synthesis (CTS):

CTS works in 3 steps:

1. Placement of all design cells. Positions of all Flip-flops are recorded and fixed for all coming steps.
2. Placement of Flip-flops and clock-tree buffers only. Clock-tree buffers are constructed as a binary tree. Positions of clock-tree buffers are recored and fixed for the coming step.
3. Placement of all design cells and clock-tree buffers. 

### Setup

1. Download Graywolf https://github.com/rubund/graywolf

2. Compile and install Graywolf.

 - cmake .

 - make

 - sudo make install


### Usage

python clockTree_blif.py \<blif_netlist_file\> \<LEF\> \<buffer_type\> \<input_pin\> \<output_pin\> \<clock_signal\> \<scriptsDir\>

**blif_netlist_file**: path to the netlist required to be placed in blif format

**LEF**: path to LEF file

**buffer_type**: Buffer used in clock tree (for example: BUFX2)

**input_pin**: input pin name of the buffer specified in buffer_type

**output_pin**: output pin name of the buffer specified in buffer_type

**clock_signal**: clock signal name as specified in the blif netlist

**scriptsDir**: path to CTS scripts folder


### Examples:


####SPM

Inputs: SPM.blif, osu035_stdcells.lef

command:

python clockTree_blif.py ./examples/SPM/SPM.blif ./scripts/osu035_stdcells.lef BUFX2 A Y clk ./scripts

Outputs:

SPM_step1.def: def file with placement of all design cells

SPM_step2.def: def file with placement of design Flip-flops and added clock-tree buffers

SPM_def: final placement of all design cells plus clock-tree buffers

SPM_route: routed def file using qrouter


####map

Inputs: map.blif, osu035_stdcells.lef

command:

python clockTree_blif.py ./examples/map/map.blif ./scripts/osu035_stdcells.lef BUFX2 A Y clock ./scripts

Outputs:

map_step1.def: def file with placement of all design cells

map_step2.def: def file with placement of design Flip-flops and added clock-tree buffers

map_def: final placement of all design cells plus clock-tree buffers

map_route: routed def file using qrouter



## RC2spef converter:

### Usage

./rc2spef -r \<rc\> -l \<liberty\> -s \<spef\>

**rc**: rc file name

**liberty**: stdcell liberty file_name

**spef**: output spef file name

### Example:

Inputs: map.rc, osu035_stdcells.lib

Output: map.spef

./rc2spef -r ./example/map.rc -l .example/osu035_stdcells.lib -s ./example/map.spef



## blif2def converter:

### Usage

python blif2def.py <blif_file_name> <lef_file_name> <utilization> <aspect_ratio>


## Power Synthesis:

### Inputs with examples:

**Input DEF path**: (example: "./example/CSADD_route.def")

**Input Output path**: (example: "./example/output.def")

**Input metal 1**: input metal 1 type used at ring (example: "metal1")

**Input metal 2**: input metal 2 type used at ring (example: "metal2")

**Input via**: input via type used to connect metals (example: "M2_M1")

**Input distance from core area**: distance of output ring from core area in the def file (example: -280)

**Input width of metal**: width of metal 1 and metal 2 (example: 120)

**Input space between ground and vdd rings**: distance between rings (example: 20)


## SDF:

### Usage

python sdf.py <design_name> <early_lib> <late_lib> <clk_signal> <output_ports>

### Example

Inputs: simple.v, simple_Early.lib, simple_Late.lib

Outputs: output sdf is generated as out.sdf

Command:

python sdf.py simple simple_Early.lib simple_Late.lib iccad_clk out



## mrouter: 

### Example:

Inputs:

ALU6502.cfg: configuration file. contains information about LEF and DEF files, routing layers and obstructions.

ALU6502_unroute.def: DEF file to be routed

Output:

ALU6502_unroute_route.def: routed DEF file
 
mrouter -v 1 -c ./6502/ALU6502.cfg -p vdd -g gnd -q ALU6502_unroute.def

mrouter can be downloaded from http://wrcad.com/freestuff.html


