import sys, os
import re

if(len(sys.argv)<4):
   print "Usage: python blif2def.py <blif file name> <lef file name> <utilization> <aspect ratio>"
   exit(0)
blifFile = sys.argv[1]
lefFile = sys.argv[2]
utilization = sys.argv[3]
aspectRatio = sys.argv[4]
defFile = "output.def"
fdef = open(defFile, "w")
fblif = open(blifFile, "r")

components = []
pins = []
nets_only = []
nets = {}
numComponents = 0
numPins = 0
numNets = 0
blifContents = fblif.readlines()
for line in blifContents:
  if line.strip().startswith(".gate"):
     componentsLine = line.split()
     gateName = componentsLine[1]
     components.append(gateName)
     for i in range (2, len(componentsLine)):
       connection = componentsLine[i].split("=")
       pin = connection[0]
       net = connection[1]
       key = gateName + "_" + str(numComponents) + " " + pin
       value = net.strip()
       nets[key] = value
       nets_only.append(net.strip())
     numComponents = numComponents + 1
  if line.strip().startswith(".inputs") or line.strip().startswith(".outputs"):
     pinsLine = line.split()
     for pin in pinsLine:
       if not (pin == ".inputs"):
          if not (pin == ".outputs"):
             pins.append(pin.strip())
             numPins = numPins + 1
  if line.strip().startswith(".model"):
     modelName = (line.strip().split())[1]
newNets = []
for i in nets_only:
  if i not in newNets:
    newNets.append(i)

gateName = components[1]
siteName=""
siteHeight = 0
siteWidth = 0
lefScale = 0
lef = open(lefFile, "r")
lefContents = lef.readlines()
for i in range(len(lefContents)):
  if "DATABASE MICRONS" in lefContents[i].strip():
     line = lefContents[i].strip().split()
     lefScale = line[len(line)-2]
     scaleRatio = float(lefScale) / 10
  if lefContents[i].strip().startswith("MACRO " + gateName):
     for j in range(1,9):
       if lefContents[i+j].strip().startswith("SITE"):
          siteName = lefContents[i+j].strip().split()[1]
          break
for i in range(len(lefContents)):
  if lefContents[i].strip().startswith("SITE"):
   if lefContents[i].strip().split()[-1] == siteName:  
     for j in range(1,9):
       if "SIZE" in lefContents[i+j].strip():
         print " width ", lefContents[i+j].strip().split()[1]
         siteWidth = float(lefContents[i+j].strip().split()[1]) * scaleRatio
         siteHeight = float(lefContents[i+j].strip().split()[3]) * scaleRatio
         break
print "name ", siteName
print "width " , siteWidth
print "height " , siteHeight
os.system("./blif2cel.tcl --blif " + blifFile + " --lef " + lefFile + " --cel temp.cel")
os.system("./getwidth.tcl temp " + lefFile)
f_area = open("temp.width", "r")
width = int(f_area.readlines()[0])
cellsArea = width * siteHeight
total_core_area = float(cellsArea)/float(utilization)
w= int((float(total_core_area)/float(aspectRatio))**(0.5))
h = int(total_core_area/w)
x_min = 0
y_min = 0
x_max = x_min + w
y_max = y_min + h

fdef.write("VERSION 5.6 ;\n")
fdef.write("NAMESCASESENSITIVE ON ;\n")
fdef.write("DIVIDERCHAR \"/\" ;\n")
fdef.write("BUSBITCHARS \"<>\" ;\n")
fdef.write("DESIGN " + modelName + " ;\n")
fdef.write("UNITS DISTANCE MICRONS 100 ;\n")
fdef.write("\n")
fdef.write("DIEAREA ( 0.0 0.0 ) ( " + str(x_max) + " " + str(y_max) + " ) ;\n")

rowXStart = 200
rowXEnd = x_max - 200
rowYStart = 200
rowYEnd = y_max - 200
height = int(rowYEnd) - int(rowYStart)
width = int(rowXEnd) - int(rowXStart)
no_of_rows = int(height / siteHeight)
no_horizontal_steps = (width)/int(siteWidth)
start_x = int(rowXStart)
start_y = int(rowYStart) 
flag = False
mirror = ""
vertical_step=0
for i in range(int(no_of_rows)):
     if flag == False:
       fdef.write( "ROW core_SITE_ROW_" + str(i) + " " + siteName + " " +  str(start_x) + " " + str(start_y + vertical_step) + " N DO " +  str(no_horizontal_steps) + " BY 1 STEP " +  str(siteWidth) + " 0 ;\n")
       flag = True
     else:
       fdef.write( "ROW core_SITE_ROW_" + str(i) + " core " + str(start_x) + " " + str(start_y + vertical_step) + " FS DO " +  str(no_horizontal_steps) + " BY 1 STEP " +  str(siteWidth) + " 0 ;\n")
       flag = False
     vertical_step += int(siteHeight)
       

fdef.write("COMPONENTS " + str(numComponents) + " ;\n")
counter = 0
for component in components:
    fdef.write("\t- " + component + ("_") + str(counter) + " " + component + " + UNPLACED ;\n")
    counter = counter + 1
fdef.write("END COMPONENTS\n")
fdef.write("PINS " + str(numPins) + " ;\n")
for pin in pins:
    fdef.write("- " + pin + " + NET " + pin + " ;\n")
fdef.write("END PINS\n")
fdef.write("NETS " + str(len(newNets)) + " ;\n")
for net in newNets:
  fdef.write("- " + net.strip() + "\n")
  for key1,value1 in nets.items():
   if value1 == net:
     fdef.write("\t( " + key1 + " )\n")
  fdef.write(";\n")
fdef.write("END NETS\n")  
fdef.write("END DESIGN\n")
fdef.close()
