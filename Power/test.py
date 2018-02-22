import random
import sys
import os

core=[]
rows=[]
#width=120
#distance=-280
#space=20
n=0
t=0

def_path=input('Input DEF path: ')
output_path=input('Input Output path: ')
metal1=input('Input metal 1: ')
metal2=input('Input metal 2: ')
via=input('Input via: ')
distance=float(input('Input distance from core area: '))
width=float(input('Input width of metal: '))
space=float(input('Input space between ground and vdd rings: '))
#"C:/Users/ziad/Documents/Visual Studio 2012/Projects/power_ring/power_ring/CSADD_route.def"

f = open(def_path,'r')
w = open(output_path, "w",newline='')


for line in f:

    if 'DIEAREA' in line:
        x=[]
        n=0
        for t in line.split():
            try:
                core.append(float(t))
                if(n<2):
                    w.write(str(float(t)+distance+space)+" ")
                else:
                    w.write(str(float(t)-distance-space) + " ")
                n+=1
            except ValueError:
                pass
                w.write(t+" ")
        w.write("\n"+"\n"+"NONDEFAULTRULES 1 ;" + "\n"
                + "- doubleSpaceRule" + "\n"
                + "+ LAYER " + metal1 + " WIDTH " + str(width) + "\n"
                + "+ LAYER " + metal2 + " WIDTH " + str(width) + "\n"
                + " ;" + "\n"
                + "END NONDEFAULTRULES" + "\n")

    elif 'core' in line:
        l = []
        x=[]
        for t in line.split():
            try:
                l.append(float(t))
                w.write(t+" ")
            except ValueError:
                pass
                w.write(t+" ")
        rows.append(l[1])
        w.write("\n")

    elif 'END PINS' in line:
        l = []
        x = []
        w.write("- gnd + NET gnd_ring" +"\n"
                +"+ LAYER " + metal1 + " ( -20 0 ) ( 25 50 )" + "\n"
                +"+ PLACED ( " + str(core[0] + 0.5 * width + distance) + " " + str(core[1] + 0.5 * width + distance) + " ) N ;" + "\n"
                +"- vdd + NET vdd_ring" + "\n"
                +"+ LAYER " + metal1 + " ( -20 0 ) ( 25 50 )" + "\n"
                +"+ PLACED ( " + str(core[0] + 1.5 * width + distance + space) + " " + str(core[1] + 1.5 * width + distance + space) + " ) N ;" + "\n")
        for t in line.split():
            try:
                l.append(float(t))
                w.write(str(float(t) + 2) + " ")
            except ValueError:
                pass
                w.write(t + " ")
        w.write("\n")

    elif 'PINS' in line:
        l = []
        x=[]
        for t in line.split():
            try:
                l.append(int(t))
                w.write(str(int(t)+2)+" ")
            except ValueError:
                pass
                w.write(t+" ")
        w.write("\n")

    elif 'END NETS' in line:
        l = []
        x = []

        w.write("- gnd_ring" +"\n"
        +"( PIN gnd ) " +"\n"
        +"+ ROUTED " + metal1 + " TAPERRULE doubleSpaceRule ( " + str(core[0] + 0.5 * width + distance) + " " + str(core[1] + 0.5 * width + distance) + " ) ( " + str(core[2] - 0.5 * width - distance) + " * ) " + via + "\n"
        +"+ ROUTED " + metal2 + " TAPERRULE doubleSpaceRule ( " + str(core[2] - 0.5 * width - distance) + " " + str(core[1] + 0.5 * width + distance) + " ) ( * " + str(core[3] - 0.5 * width - distance) + " ) " + via + "\n"
        +"+ ROUTED " + metal1 + " TAPERRULE doubleSpaceRule ( " + str(core[2] - 0.5 * width - distance) + " " + str(core[3] - 0.5 * width - distance) + " ) ( " + str(core[0] + 0.5 * width + distance) + " * ) " + via + "\n"
        +"+ ROUTED " + metal2 + " TAPERRULE doubleSpaceRule ( " + str(core[0] + 0.5 * width + distance) + " " + str(core[3] - 0.5 * width - distance) + " ) ( * " + str(core[1] + 0.5 * width + distance) + " ) " + via +"\n")

        i = 0
        while i < len(rows):
            w.write("+ ROUTED " + metal2 + " TAPERRULE doubleSpaceRule ( " + str(core[0] + 0.5 * width + distance) + " " + str(rows[i]) + " ) " + via + " ( " + str(core[0] + 0.5 * width + distance) + " " + str(rows[i]) + " ) ( " + str(core[2] - 0.5 * width - distance) + " * ) " + via + "\n")
            i += 2

        w.write( "+ ROUTED " + metal2 + " TAPERRULE doubleSpaceRule ( " + str(core[0] + 0.5 * width + distance) + " " + str(2*rows[-1]-rows[-2]) + " ) " + via + " ( " + str(core[0] + 0.5 * width + distance) + " " + str(2*rows[-1]-rows[-2]) + " ) ( " + str(core[2] - 0.5 * width - distance) + " * ) " + via + " ;" +"\n")



        w.write("- vdd_ring" +"\n"+ "( PIN vdd ) " +"\n"
        +"+ ROUTED " + metal1 + " TAPERRULE doubleSpaceRule ( " + str(core[0] + 1.5 * width + distance + space) + " " + str(core[1] + 1.5 * width + distance + space) + " ) ( " + str(core[2] - 1.5 * width - distance - space) + " * ) " + via +"\n"
        +"+ ROUTED " + metal2 + " TAPERRULE doubleSpaceRule ( " + str(core[2] - 1.5 * width - distance - space) + " " + str(core[1] + 1.5 * width + distance + space) + " ) ( * " + str(core[3] - 1.5 * width - distance - space) + " ) " + via +"\n"
        +"+ ROUTED " + metal1 + " TAPERRULE doubleSpaceRule ( " + str(core[2] - 1.5 * width - distance - space) + " " + str(core[3] - 1.5 * width - distance - space) + " ) ( " + str(core[0] + 1.5 * width + distance + space) + " * ) " + via +"\n"
        +"+ ROUTED " + metal2 + " TAPERRULE doubleSpaceRule ( " + str(core[0] + 1.5 * width + distance + space) + " " + str(core[3] - 1.5 * width - distance - space) + " ) ( * " + str(core[1] + 1.5 * width + distance + space) + " ) " + via +"\n")

        i = 1
        while i < len(rows):
            w.write("+ ROUTED " + metal2 + " TAPERRULE doubleSpaceRule ( " + str(core[0] + 1.5 * width + distance + space) + " " + str(rows[i]) + " ) " + via + " ( " + str(core[0] + 1.5 * width + distance + space) + " " + str(rows[i]) + " ) ( " + str(core[2] - 1.5 * width - distance - space) + " * ) " + via + "\n")
            i += 2

        w.write(";"+"\n")

        for t in line.split():
            try:
                l.append(float(t))
                w.write(str(float(t) + 2) + " ")
            except ValueError:
                pass
                w.write(t + " ")
        w.write("\n")

    elif 'NETS' in line:
        l = []
        x=[]
        for t in line.split():
            try:
                l.append(int(t))
                w.write(str(int(t)+2)+" ")
            except ValueError:
                pass
                w.write(t+" ")
        w.write("\n")

    else:
        w.write(line)



  #   text = f.readline()

