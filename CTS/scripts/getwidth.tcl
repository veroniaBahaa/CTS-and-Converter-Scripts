#!/usr/bin/tclsh

set cellname [file rootname [lindex $argv 0]]
set celfile ${cellname}.cel
set lefname [lindex $argv 1]

if [catch {open $lefname r} flef] {
   puts stderr "Error: can't open file $lefname for input"
   return
}

if [catch {open $celfile r} fcel] {
   puts stderr "Error: can't open file $celfile for input"
   return
}
set totalwidth 0
set instlist {}
set filllist {}
while {[gets $fcel line] >= 0} {
      if [regexp {[ \t]*cell[ \t]*([0-9]+)[ \t]+([^ \t]+)} $line \
		lmatch instnum instname] {
         lappend instlist $instname
	 gets $fcel line
	 regexp {[ \t]*left[ \t]+([-]*[0-9]+)[ \t]+right[ \t]+([-]*[0-9]+)} $line \
		lmatch left right
	 incr totalwidth [expr {$right - $left}]
      }
}

# Diagnostic information
set out [file rootname [lindex $argv 0]]
set outfile ${out}.width 
#set outfile [open "step1.width" w]
if [catch {open $outfile w} fout] {
   puts stderr "Error: can't open file for output"
   return
}
puts stdout ""
puts stdout "getWidth.tcl:"
puts $fout "$totalwidth"
puts stdout "total width = $totalwidth"
puts stdout ""
