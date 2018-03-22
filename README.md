# CTS-and-Converter-Scripts

This repo includes scripts for clock tree synthesis, power network synthesis, rc2spef conversion, blif2def conversion

## Clock Tree Synthesis (CTS):

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

**scriptsDir**: path to CTS scripts 
folder



## RC2spef converter:

### Usage

./rc2dly -r \<rc\> -l \<liberty\> -s \<spef\>

**rc**: rc file name

**liberty**: stdcell liberty file_name

**spef**: output spef file name



## blif2def converter:

### Usage

python blif2def.py <blif_file_name> <lef_file_name> <utilization> <aspect_ratio>


## Power Synthesis:

### Inputs with examples:

**Input DEF path**: (example: in.def)

**Input Output path**: (example: out.def)

**Input metal 1**: input metal 1 type used at ring (example: metal1)

**Input metal 2**: input metal 2 type used at ring (example: metal2)

**Input via**: input via type used to connect metals (example: M2_M1)

**Input distance from core area**: distance of output ring from core area in the def file (example: -280)

**Input width of metal**: width of metal 1 and metal 2 (example: 120)

**Input space between ground and vdd rings**: distance between rings (example: 20)


## SDF:

### Usage

python sdf.py <designName> <earlyLib> <lateLib> <clk> <output_ports>

