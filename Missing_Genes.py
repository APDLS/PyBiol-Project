import os
import subprocess
from subprocess import call
import csv
print "Input Annotated Genome File"
A=raw_input()
print "Input Raw Genome File"
B=raw_input()
print "Input Reference Genes FASTA File"
C=raw_input()

#Open Genes File
f=open(C)
h=f.readlines()
f.close()

#Define set
genes=set()
x=0
#Add genes to set
for line in h:
	if ">" in line:
		gene=str(line)
		while ">" in g[x]:
			gene=gene+"\n"+str(g[x])
			x=x+1
		genes.add(gene)
	x=x+1

g = open("Missing_Genes.txt","w")
for i in genes:
	f=open("Temp_Genes.fasta","w")
	f.write(str(i))
	f.close()
	Annotation_Missing=False
	call(["blastx", "-db", A, "-query", "Temp_Genes.fasta", "-outfmt", "10", "-out", "Temp.csv"])
	found = "no"
	with open("Temp.csv", "rb") as f:
		mycsv = csv.reader(f)
		for row in mycsv:
			text = row[10]
			if float(text) < 1e-10:
				print row
				found = "yes"
		if found == "no":
			g.write(i)
			g.write("\n")
			print "Annotation Missing "+str(i)
			Annotation_Missing=True
	if Annotation_Missing=True:
		call(["blastx", "-db", B, "-query", "Temp_Genes.fasta", "-outfmt", "10", "-out", "Temp.csv"])
		found = "no"
		with open("Temp.csv", "rb") as f:
			mycsv = csv.reader(f)
			for row in mycsv:
				text = row[10]
				if float(text) < 1e-10:
					print row
					found = "yes"
			if found == "no":
				g.write("Missing in Assembly:"+i)
				g.write("\n")
				print "Assembly Missing "+str(i)
g.close()
