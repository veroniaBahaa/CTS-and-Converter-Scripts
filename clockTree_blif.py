import math
import sys, os
import re

if(len(sys.argv)<5):
   print "Usage: python clockTree.py netlistFile lefFile BufferType input_pin output_pin clock_Signal scriptsDir"
   exit(0)
netlistFile = sys.argv[1]
circuit = netlistFile.split(".")
circuitName = circuit[0]
cellType = "Insert" + sys.argv[3] 
cellIn = sys.argv[4]
cellOut = sys.argv[5]
clk = sys.argv[6]
scriptsDir = sys.argv[7]

lef = sys.argv[2]
os.system("cp " + lef + " updated.lef")
os.system("echo MACRO InsertINVX4 > add_to_lef")
os.system("echo CLASS  CORE \; >> add_to_lef")
os.system("echo FOREIGN InsertINVX4 0.000 0.000 \; >> add_to_lef") 
os.system("echo ORIGIN 0.000 0.000 \;  >> add_to_lef")
os.system("echo SIZE 4.800 BY 20.000 \; >> add_to_lef")
os.system("echo SYMMETRY X Y \;  >> add_to_lef")
os.system("echo SITE core \; >> add_to_lef")
os.system("echo PIN A >> add_to_lef")
os.system("echo DIRECTION INPUT \; >> add_to_lef")
os.system("echo PORT >> add_to_lef")
os.system("echo LAYER metal1 \; >> add_to_lef")
os.system("echo RECT 0.400 5.800 1.200 7.400 \; >> add_to_lef")
os.system("echo END >> add_to_lef")
os.system("echo END A >> add_to_lef")
os.system("echo PIN gnd >> add_to_lef")
os.system("echo DIRECTION INOUT \; >> add_to_lef")
os.system("echo USE GROUND \; >> add_to_lef")
os.system("echo SHAPE ABUTMENT \; >> add_to_lef")
os.system("echo PORT >> add_to_lef")
os.system("echo LAYER metal1 \; >> add_to_lef")
os.system("echo RECT 0.400 -0.600 1.200 5.200 \; >> add_to_lef")
os.system("echo RECT -0.400 -0.600 5.200 0.600 \; >> add_to_lef")
os.system("echo RECT 3.600 -0.600 4.400 5.200 \; >> add_to_lef")
os.system("echo END >> add_to_lef")
os.system("echo END gnd >> add_to_lef")
os.system("echo PIN Y >> add_to_lef")
os.system("echo DIRECTION OUTPUT \; >> add_to_lef")
os.system("echo PORT >> add_to_lef")
os.system("echo LAYER metal1 \; >> add_to_lef")
os.system("echo RECT 2.000 1.200 2.800 18.800 \; >> add_to_lef")
os.system("echo END >> add_to_lef")
os.system("echo END Y >> add_to_lef")
os.system("echo PIN vdd >> add_to_lef")
os.system("echo DIRECTION INOUT \; >> add_to_lef")
os.system("echo USE POWER \; >> add_to_lef")
os.system("echo SHAPE ABUTMENT \; >> add_to_lef")
os.system("echo PORT >> add_to_lef")
os.system("echo LAYER metal1 \; >> add_to_lef")
os.system("echo RECT 0.400 10.800 1.200 20.600 \; >> add_to_lef")
os.system("echo RECT -0.400 19.400 5.200 20.600 \; >> add_to_lef")
os.system("echo RECT 3.600 10.800 4.400 20.600 \; >> add_to_lef")
os.system("echo END >> add_to_lef")
os.system("echo END vdd >> add_to_lef")
os.system("echo END InsertINVX4 >> add_to_lef")

os.system("echo MACRO InsertBUFX2 >> add_to_lef")
os.system("echo CLASS  CORE \; >> add_to_lef")
os.system("echo FOREIGN InsertBUFX2 0.000 0.000 \; >> add_to_lef") 
os.system("echo ORIGIN 0.000 0.000 \;  >> add_to_lef")
os.system("echo SIZE 4.800 BY 20.000 \; >> add_to_lef")
os.system("echo SYMMETRY X Y \;  >> add_to_lef")
os.system("echo SITE core \; >> add_to_lef")
os.system("echo PIN A >> add_to_lef")
os.system("echo DIRECTION INPUT \; >> add_to_lef")
os.system("echo PORT >> add_to_lef")
os.system("echo LAYER metal1 \; >> add_to_lef")
os.system("echo RECT 0.400 5.800 1.200 7.400 \; >> add_to_lef")
os.system("echo END >> add_to_lef")
os.system("echo END A >> add_to_lef")
os.system("echo PIN gnd >> add_to_lef")
os.system("echo DIRECTION INOUT \; >> add_to_lef")
os.system("echo USE GROUND \; >> add_to_lef")
os.system("echo SHAPE ABUTMENT \; >> add_to_lef")
os.system("echo PORT >> add_to_lef")
os.system("echo LAYER metal1 \; >> add_to_lef")
os.system("echo RECT 0.400 -0.600 1.200 5.200 \; >> add_to_lef")
os.system("echo RECT -0.400 -0.600 5.200 0.600 \; >> add_to_lef")
os.system("echo RECT 3.600 -0.600 4.400 5.200 \; >> add_to_lef")
os.system("echo END >> add_to_lef")
os.system("echo END gnd >> add_to_lef")
os.system("echo PIN Y >> add_to_lef")
os.system("echo DIRECTION OUTPUT \; >> add_to_lef")
os.system("echo PORT >> add_to_lef")
os.system("echo LAYER metal1 \; >> add_to_lef")
os.system("echo RECT 2.000 1.200 2.800 18.800 \; >> add_to_lef")
os.system("echo END >> add_to_lef")
os.system("echo END Y >> add_to_lef")
os.system("echo PIN vdd >> add_to_lef")
os.system("echo DIRECTION INOUT \; >> add_to_lef")
os.system("echo USE POWER \; >> add_to_lef")
os.system("echo SHAPE ABUTMENT \; >> add_to_lef")
os.system("echo PORT >> add_to_lef")
os.system("echo LAYER metal1 \; >> add_to_lef")
os.system("echo RECT 0.400 10.800 1.200 20.600 \; >> add_to_lef")
os.system("echo RECT -0.400 19.400 5.200 20.600 \; >> add_to_lef")
os.system("echo RECT 3.600 10.800 4.400 20.600 \; >> add_to_lef")
os.system("echo END >> add_to_lef")
os.system("echo END vdd >> add_to_lef")
os.system("echo END InsertBUFX2 >> add_to_lef")
os.system("echo END LIBRARY >> add_to_lef")
with open("updated.lef") as f_lef:
      lef_contents = f_lef.readlines()
del lef_contents[len(lef_contents)-1]
f_lef = open("updated.lef","w")
for line in lef_contents:
    f_lef.write(line)
f_lef.close()
os.system("cat add_to_lef >> updated.lef")

netlist_original=netlistFile
netlist_noFF = []
#count flip flops
flipFlops = 0
flipFlopsLineIndex=[]
with open(netlistFile) as f1:
      netlist = f1.readlines()

index =0
clockTreeNetlist=[]
for line in netlist:
      line = line.strip()
      if line.startswith(".gate DFF") or line.startswith(".model") or line.startswith(".inputs") or line.startswith(".outputs") or line.startswith(".end"):
             clockTreeNetlist.append(line)             
      if not line.startswith(".gate DFF"):
          netlist_noFF.append(line)

for line in clockTreeNetlist:
   if line.startswith(".gate DFF"):
          flipFlops = flipFlops + 1
          flipFlopsLineIndex.append(index)
   index = index + 1

endIndex = len(netlist)
numNodes = 2*flipFlops - 1
numLevels = int(math.log(numNodes,2)) 
bufInput=""
bufOutput=""
unconnected = True
i=0
firstOut = "a0_1"
firstBuf = cellType + "_0_0"
clockTreeNetlist.insert(len(clockTreeNetlist)-1, ".gate " + cellType + " " + str(cellIn)+"=" + str(clk) + " " + str(cellOut) +"=" + str(firstOut) )
for level in range(numLevels):
    nodesInLevel = 2**(level+1)
    for node in range(nodesInLevel):
	bufInput = "a"+str(level) + "_" + str(int((node)/2+1))
        bufOutput =  "a"+str(level+1)+ "_" + str(node+1)
        bufInst = cellType + "_" + str(level+1) + "_" + str(node+1)
        mystr = ".gate " + cellType + " " + str(cellIn)+"=" + str(bufInput) + " "+ str(cellOut) +"=" + str(bufOutput)
        if (level == numLevels -1 and unconnected == True) or level < numLevels-1:
                clockTreeNetlist.insert(len(clockTreeNetlist)-1,mystr)
        if level == numLevels -1 and unconnected == True:
           regex = re.compile(r"CLK=%s.+ "%str(clk))
           clockTreeNetlist[flipFlopsLineIndex[i]] = re.sub(r"CLK=([^\s]+)","CLK="+ bufOutput+ " ",clockTreeNetlist[flipFlopsLineIndex[i]])
           i = i+1
           if i == flipFlops:
              unconnected = False

#step1, place original netlist without CTS
os.system(scriptsDir + "/blif2cel.tcl " + netlist_original + " updated.lef " + "step1.cel")
f20 = open("step1.cel","r")
cel_contents = f20.readlines()
for i in range(len(cel_contents)):
    if cel_contents[i].startswith("pad"):
       if ((cel_contents[i].split(" "))[-1]).startswith("twpin_clk"):
         print i
         for j in range(6):
           if cel_contents[i+j].startswith("pin"):
              cel_contents.insert(i+j,"restrict side B sidespace 0.5\n" )
              print j
              break
f20.close()
f21 = open("step1.cel","w")
for i in cel_contents:
    f21.write(i)
f21.close()
os.system("cp " + scriptsDir + "/default.par "+ "temp.par")
os.system("mv temp.par "+ "step1" + ".par")
os.system(scriptsDir + "/decongest.tcl step1 updated.lef FILL 0.7")
os.system("mv step1.acel step1.cel")
os.system(scriptsDir + "/getwidth.tcl step1 updated.lef")
f_area1 = open("step1.width", "r")
area1 = int(f_area1.readlines()[0])
f_area1.close()

os.system("graywolf " + "step1")
os.system("echo read_lef updated.lef > step1.cfg")
os.system("qrouter -i step1.info -c step1.cfg")
os.system(scriptsDir + "/place2def.tcl step1 FILL")
os.system("mv step1.def " + circuitName+ "_step1.def")
os.system("mv step1.obs " + circuitName+ "_step1.obs")

f_annoCel = open("step1.ncel", "r")
annoCel = f_annoCel.readlines()
for i in range(len(annoCel)):
    annoCel[i] = annoCel[i].strip()
    if annoCel[i].startswith("cell"):
       if "FILL" in annoCel[i]:
           annoCel[i] = re.sub(r"FILL\..+\.","",annoCel[i])
f_annoCel.close()
f_annoCel = open("step1.ncel", "w")
for line in annoCel:
  f_annoCel.write(line)
  f_annoCel.write("\n")
f_annoCel.close()

DFFpositions={}
j=0
with open("step1.ncel") as f3:
      ncel = f3.readlines()
for i in range(len(ncel)):
    ncel[i] = ncel[i].strip()
    if ncel[i].startswith("cell"):
       splitLine = ncel[i].split(" ")
       if splitLine[-1].startswith("DFF"):
         DFFpositions[(splitLine[-1])] = ncel[i+1]

#step2, clock tree
f2 = open("clockTree.blif","w")
for line in clockTreeNetlist:
    f2.write(line)
    f2.write("\n")
f2.close()
os.system(scriptsDir + "/blif2cel.tcl " + "clockTree.blif" + " updated.lef " +   "clockTree.cel")

os.system(scriptsDir + "/getwidth.tcl clockTree updated.lef")
f_area2 = open("clockTree.width", "r")
area2 = int(f_area2.readlines()[0])
f_area2.close()

print "area1 ", area1
print "area2 ", area2
##################################################################################################
diff_area = area1-area2 #original area - clock tree area
buff_width = 480
# add unconnected inverters to fill empty places
num_added_buffs = int(diff_area/buff_width) + 20
print "num_added_buffs" ,num_added_buffs
j=10000
for i in range(num_added_buffs):
    clockTreeNetlist.insert(len(clockTreeNetlist)-1,".gate InsertINVX4 A=" + str(i) + " Y="+str(j))
    j=j+1
f2 = open("clockTree.blif","w")
for line in clockTreeNetlist:
    f2.write(line)
    f2.write("\n")
f2.close()

os.system(scriptsDir + "/blif2cel.tcl " + "clockTree.blif" + " updated.lef " +   "clockTree.cel")

f11=open("clockTree.cel","r")
content = f11.readlines()
for i in range(len(content)):
    content[i] = content[i].strip()
    if content[i].startswith("cell"):
       splitLine = content[i].split(" ")
       if splitLine[-1].startswith("DFF"):
          for key, value in DFFpositions.iteritems():
              if key == splitLine[-1]:
                 content.insert(i+1,value)

for i in range(len(content)):
    if content[i].startswith("pad"):
       if ((content[i].split(" "))[-1]).startswith("twpin_clk"):
         print i
         for j in range(6):
           if content[i+j].startswith("pin"):
              content.insert(i+j,"restrict side B sidespace 0.5\n" )
              print j
              break
f12 = open("step1.cel","w")
for i in range(len(content)):
    content[i] = content[i].replace("nonfixed","fixed")
    f12.write(content[i])
    f12.write("\n")
f12.close()

#place
os.system("mv step1.pl1 step1.pl1_1")
os.system("graywolf " + "step1")
os.system("echo read_lef updated.lef > step1.cfg")
os.system("qrouter -i step1.info -c step1.cfg")
os.system(scriptsDir + "/place2def.tcl step1 FILL 4")
os.system("mv step1.def " + circuitName + "_step_2.def")
os.system("mv step1.obs " + circuitName + "_step_2.obs")

#remove extra inverters from def
f_def = open(circuitName + "_step_2.def","r")
def_content = f_def.readlines()
for line in range(len(def_content)):
    def_content[line] = def_content[line].strip()
    if def_content[line].startswith("- InsertINVX4"):
       def_content[line] = ""
    if def_content[line].startswith("( InsertINVX4_1"):
       del def_content[line:len(def_content)]
       break
def_content.insert(len(def_content)-1,"END NETS")
def_content.insert(len(def_content)-1,"END DESIGN")
f_def2 = open(circuitName + "_step2.def","w")
for line in def_content:
   f_def2.write(line)
   f_def2.write("\n")
f_def2.close()

os.system("echo verbose 1 >> step1.cfg")
os.system("echo catch {layers 4} >> step1.cfg")
os.system("echo via stack 2 >> step1.cfg")
os.system("echo vdd vdd >> step1.cfg")
os.system("echo gnd gnd >> step1.cfg")
os.system("cat " + circuitName + "_step_2.obs >> step1.cfg")
os.system("echo read_def " + circuitName + "_step2.def >> step1.cfg")
os.system("echo qrouter::congestion_route " + circuitName + "_step2.cinfo >> step1.cfg")
os.system("echo qrouter::standard_route >> step1.cfg")
os.system("echo qrouter::write_delays " + circuitName + "_step2.rc >> step1.cfg")
os.system("echo quit >> step1.cfg")
os.system("qrouter -nog -s step1.cfg")

#remove extra inverters
start=-1
end=-1
f50 = open("step1.ncel")
contents=f50.readlines()
for i in range(len(contents)):
   line = contents[i].strip()
   if line.startswith("cell"):
       if ((line.split(" "))[-1]).startswith("InsertINVX4") and start == -1:
          if contents[i+1].strip().startswith("initially fixed"):
            continue
          else:
            start=i
            print "start: ", start
   if line.startswith("pad"):
       end = i
       print "end ", end
       break
del contents[start:end]

#fix buffers, FlipFlops
f12 = open("step1_1.cel","w")
for i in range(len(contents)):
    contents[i] = contents[i].replace("nonfixed","fixed")
    f12.write(contents[i])
    f12.write("\n")
f12.close()

f9 = open("netlist_noFF.blif","w")
for i in netlist_noFF:
    f9.write(i)
    f9.write("\n")
f9.close()
os.system(scriptsDir + "/blif2cel.tcl " + "netlist_noFF.blif" + " updated.lef " +   "netlist_noFF.cel")
with open ("netlist_noFF.cel") as f11:
     netlist_noFF = f11.readlines()
f10 = open("netlist_noFF.cel","w")
for i in netlist_noFF:
    if i.startswith("pad"):
      break
    f10.write(i)
    f10.write("\n")
f10.close()

filenames = ['netlist_noFF.cel','step1_1.cel']
with open('step1.cel', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            outfile.write(infile.read())
os.system("mv step1.pl1 step.pl1_2")
os.system(scriptsDir + "/decongest2.tcl step1 updated.lef FILL 0.6")
os.system("mv step1.acel step1.cel")
os.system("graywolf " + "step1")

os.system("echo read_lef updated.lef > step1.cfg")
os.system("qrouter -i step1.info -c step1.cfg")
os.system(scriptsDir + "/place2def.tcl step1 FILL 4")
os.system("mv step1.def "+ circuitName+".def")
os.system("mv step1.obs "+ circuitName+".obs")

os.system("echo verbose 1 >> step1.cfg")
os.system("echo catch {layers 4} >> step1.cfg")
os.system("echo via stack 2 >> step1.cfg")
os.system("echo vdd vdd >> step1.cfg")
os.system("echo gnd gnd >> step1.cfg")
os.system("cat " + circuitName + ".obs >> step1.cfg")
os.system("echo read_def " + circuitName + ".def >> step1.cfg")
os.system("echo qrouter::congestion_route " + circuitName + ".cinfo >> step1.cfg")
os.system("echo qrouter::standard_route >> step1.cfg")
os.system("echo qrouter::write_delays " + circuitName + ".rc >> step1.cfg")
os.system("echo quit >> step1.cfg")
os.system("qrouter -nog -s step1.cfg")
