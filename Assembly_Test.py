import os
import subprocess
from subprocess import call
import csv
print "Input Genome gff File"
A=raw_input()

#Open Genome File
f=open(A)
g=f.read()
f.close()

#Extract Genome Sequence
x=0
Genome=False
Sequence=""
while x<len(g):
	if ">" in g[x]:
		Genome=True
	if Genome==True:
		Sequence=Sequence+str(g[x])
	x=x+1

Sequence=Sequence.replace("\n", "")

#Extract regions near assembly gaps, regions of 10+ Ns
x=0
y=0
Gap=False
h=open("Duplicated_Genes", "w")
while x<len(Sequence):
	x=x+1
	while Sequence[x]=="N":
		y=y+1
		x=x+1
		if y==10:
			gap1=Sequence[x-1010:x-10]
			print gap1
			Gap=True
			x=x+1
	if Gap==True and x+1000<len(Sequence):
		gap2=Sequence[x:x+1000]
		x=x+1
	if Gap==True and x+1000>len(Sequence):
		gap2=Sequence[x:len(Sequence)]
		x=x+1
	y=0
	Gap=False
#Run BLAST regions to either side of the assembly gap
	f=open("temp_query.fasta", "w")
	f.write(str(gap1))
	f.close()
	if Gap==True:
		call(["blastn", "-query", "temp_query.fasta", "-db", A, "-out", "Duplicates1.csv", "-outfmt", "10"])
		f=open("temp_query.fasta", "w")
		f.write(str(gap2))
		f.close()
		call(["blastn", "-query", "temp_query.fasta", "-db", A,"-out", "Duplicates2.csv", "-outfmt", "10"])
		found = "no"
#Take hits of over 99% sequence identity from the results files, excluding the first line.		
		with open("Duplicates1.csv", "rb") as f:
			f.next()			
			mycsv = csv.reader(f)
			for row in mycsv:
				text = row[2]
				if float(text) > 99:
					print row
					found = "yes"
			if found == "yes":
				h.write(str(row))
				h.write("\n")
		with open("Duplicates2.csv", "rb") as f:
			f.next()			
			mycsv = csv.reader(f)
			for row in mycsv:
				text = row[2]
				if float(text) > 99:
					print row
					found = "yes"
			if found == "yes":
				h.write(str(row))
				h.write("\n")
