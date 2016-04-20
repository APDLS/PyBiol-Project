import os
import subprocess
from subprocess import call
print "Input Genome gff File"
A=raw_input()
print "Input Reference Genes FASTA File"
B=raw_input()

#Open Genome File
f=open(A)
g=f.readlines()
f.close()

#Open Reference File
f=open(B)
h=f.read()
f.close()

x=0
call(["blastall", "-d", B, "-i", A, "-outfmt", "10", "-o", "Duplicates.csv", "-m", "8"])

g=open("Duplicated_Genes", "w")
found = "no"
with open("Duplicates.csv", "rb") as f:
	mycsv = csv.reader(f)
	for row in mycsv:
		text = row[10]
		if float(text) < 1e-200:
			print row
			found = "yes"
	if found == "yes":
		g.write(i)
		g.write("\n")
