import os
import sys
if(len(sys.argv)<5):
   print "Usage: python sdf.py designName earlyLib lateLib clk [output ports]"
   exit(0)

rootName = sys.argv[1]
earlyLib = sys.argv[2]
lateLib = sys.argv[3]
clk = sys.argv[4]
length = len(sys.argv)
numOutputs = length - 5
outputs = []
print length
for h in range(numOutputs):
  outputs.append(sys.argv[length-h-1])

f_timing = open("simple.timing","w")
default_timing = open("default.timing", "w")
f_timing.write("clock " + clk + " 50 50\n")
default_timing.write("clock " + clk + " 50 50\n")
for h in range(numOutputs):
  f_timing.write("rat " + outputs[h] + " 10 10 20 20\n")
f_timing.close()
default_timing.close()


f_conf = open("simple.conf","w")
f_conf.write("set_num_threads 1\n") 
f_conf.write("set_early_celllib_fpath " + earlyLib + "\n")
f_conf.write("set_late_celllib_fpath " + lateLib + "\n")
f_conf.write("set_spef_fpath default.spef\n")
f_conf.write("set_verilog_fpath " + rootName + ".v\n")
f_conf.write("set_timing_fpath simple.timing\n")
f_conf.write("init_timer\n")
f_conf.write("report_timer\n")
f_conf.write("report_worst_paths -numPaths 100000\n")

f_conf.close()



os.system("./OpenTimer < simple.conf > paths.opentimer")
f_in = open("paths.opentimer", "r")
f_out = open("at.conf", "w")
f_out.write("set_num_threads 1\n") 
f_out.write("set_early_celllib_fpath " + earlyLib + "\n")
f_out.write("set_late_celllib_fpath " + lateLib + "\n")
f_out.write("set_spef_fpath default.spef\n")
f_out.write("set_verilog_fpath " + rootName + ".v\n")
f_out.write("set_timing_fpath default.timing\n")
f_out.write("init_timer\n")
f_out.write("report_timer\n")
input_contents = f_in.readlines()
paths=[]
for i in range (len(input_contents)):
  path=[]
  if input_contents[i].startswith("Path"):
     i = i + 1
     while not input_contents[i].startswith("Path") and not input_contents[i].startswith("OpenTimer"):
      #if ":" in input_contents[i]:
      pin = input_contents[i].split()[0]
      #else:
        #pin = input_contents[i].spl()
      f_out.write("report_at -pin " + pin + " -early -rise\n")
      f_out.write("report_at -pin " + pin + " -early -fall\n")
      f_out.write("report_at -pin " + pin + " -late -rise\n")
      f_out.write("report_at -pin " + pin + " -late -fall\n")
      path.append(pin)
      if i == len(input_contents)-1:
        break
      i = i + 1
     paths.append(path)

f_out.close()
os.system("./OpenTimer < at.conf > at.out")
f_arrivalTimes = open("at.out", "r")
#f_arrivalTimes = open("test", "r")
arrivalTimes = f_arrivalTimes.readlines()
early_rise = {}
early_fall = {}
late_rise = {}
late_fall = {}
for j in range (len(arrivalTimes)):
  if "report_at -pin" in arrivalTimes[j]:
   pin = arrivalTimes[j].split()[3]
   if "early" in arrivalTimes[j] and "rise" in arrivalTimes[j]:
     early_rise[pin] = float(arrivalTimes[j+1].strip())
   if "early" in arrivalTimes[j] and "fall" in arrivalTimes[j]:
     early_fall[pin] = float(arrivalTimes[j+1].strip())
   if "late" in arrivalTimes[j] and "rise" in arrivalTimes[j]:
     late_rise[pin] = float(arrivalTimes[j+1].strip())
   if "late" in arrivalTimes[j] and "fall" in arrivalTimes[j]:
     late_fall[pin] = float(arrivalTimes[j+1].strip())
  
outfile = open("out.sdf","w")
cell_iopaths = []
interconnect = []
for path in paths:
  #print path
  k=1
  length = len(path)
  #print "len = ", length 
  while (k < length):
   #print "k= ", k
   name1 = path[length-k]
   name2 = path[length-k-1]
   #print "name1 ", name1
   #print "name2 ", name2
   if name1.split(":")[0] == name2.split(":")[0]:
     cellName = name1.split(":")[0]
     cell_iopaths.append([cellName,name1,name2])
   else:
     interconnect.append([name1,name2])
   k = k + 1
cellType = {}
netlist = open(rootName + ".v","r")
netlist_lines = netlist.readlines()
for iopath in cell_iopaths:
  for line in netlist_lines:
    if iopath[0] in line:
      cellType[iopath[0]] = line.split()[0]

import itertools
cell_iopaths.sort()
cell_iopaths = list(cell_iopaths for cell_iopaths,_ in itertools.groupby(cell_iopaths))
interconnect.sort()
interconnect = list(interconnect for interconnect,_ in itertools.groupby(interconnect))
#print interconnect

outstring = ""
outstring = outstring + "(DELAYFILE\n\t(SDFVERSION \"1.0\")\n\t(DESIGN \"system\")\n\t(VERSION \"1.5\")\n\t(DIVIDER /)\n\t(TIMESCALE 1ps)"
for key, value in cellType.items():
  outstring = outstring + "\n(CELL\n(CELLTYPE \"" + key + "\")\n(INSTANCE " + cellType[key] + ")\n(DELAY\n(ABSOLUTE\n"
  for iopath in cell_iopaths:
    if iopath[0] == key:
     pin1 = iopath[1].split(":")[1]
     pin2 = iopath[2].split(":")[1]
     earlyRise = early_rise[iopath[2]] - early_rise[iopath[1]] 
     earlyFall = early_fall[iopath[2]] - early_fall[iopath[1]] 
     lateRise = late_rise[iopath[2]] - late_rise[iopath[1]] 
     lateFall = late_fall[iopath[2]] - late_fall[iopath[1]]
     outstring = outstring + "(IOPATH " + pin1 + " " + pin2 + " (" + str(earlyRise) + "::" + str(lateRise) + ") (" + str(earlyFall) + "::" + str(lateFall) + "))\n"
  outstring = outstring + ")))\n"

outstring = outstring + "(CELL (CELLTYPE \"system\")\n(INSTANCE *)\n(DELAY\n(ABSOLUTE\n"
for net in interconnect:
  pin1 = net[0]
  pin2 = net[1]
  earlyRise = early_rise[pin2] - early_rise[pin1] 
  earlyFall = early_fall[pin2] - early_fall[pin1] 
  lateRise = late_rise[pin2] - late_rise[pin1] 
  lateFall = late_fall[pin2] - late_fall[pin1]
  outstring = outstring + "(INTERCONNECT " + pin1.replace(":","/") + " " + pin2.replace(":","/") + " (" + str(earlyRise) + "::" + str(lateRise) + ") (" + str(earlyFall) + "::" + str(lateFall) + "))\n"   

outstring = outstring + ")))\n)"     
print outstring   
outfile.write(outstring)
outfile.close()
