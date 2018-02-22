# CTS
Setup

1- Download Graywolf https://github.com/rubund/graywolf

2- Compile and install Graywolf.

cmake .

make

sudo make install    


Usage

python clockTree_blif.py <blif_netlist_file> <buffer_type> <input_pin> <output_pin> <clock_signal>

blif_netlist_file: path to the netlist required to be placed in blif format.

buffer_type: Buffer used in clock tree (for example: BUFX2).

input_pin: input pin name of the buffer specified in buffer_type.

output_pin: output pin name of the buffer specified in buffer_type.

clock_signal: clock signal name as specified in the blif netlist.
