import os
import subprocess
from subprocess import call
print "Input Genome gff File"
A=raw_input()

#Open Genome File
f=open(A)
g=f.readlines()
f.close()

#Extract Genome Sequence
x=0
Genome=False
Sequence=""
for i in g:
	x=x+1
	while x<len(g):
		if ">" in g[x]:
			Genome=True
		if Genome==True:
			Sequence=Sequence+str(g[x])

#Extract regions near assembly gaps, regions of 10+ Ns
x=0
y=0
h=open("Duplicated_Genes", "w")
while x<len(Sequence):
	if Sequence[x]=="N":
		y=y+1
		x=x+1
		if y==10:
			print "N"
			gap1=Sequence[x-1010:x-10]
			Gap=True
			x=x+1
			if Sequence[x+1]!="N" and Gap==True:
				gap2=Sequence[x:x+1000]
			else:
				x=x+1
	x=x+1
	y=0
#Run BLAST regions to either side of the assembly gap
	f=open("temp_query.fasta", "w")
	f.write(str(gap1))
	f.close()
	if Gap==True:
		call(["blastn", "-query", "temp_query.fasta", "-db", A, "-outfmt", "10", "-o", "Duplicates1.csv", "-m", "8"])
		f=open("temp_query.fasta", "w")
		f.write(str(gap2))
		f.close()
		call(["blastn", "-query", "temp_query.fasta", "-db", A, "-outfmt", "10", "-o", "Duplicates2.csv", "-m", "8"])
		found = "no"
#Take hits of over 99% sequence identity from the results files, excluding the first line.		
		with open("Duplicates1.csv", "rb") as f:
			f.next()			
			mycsv = csv.reader(f)
			for row in mycsv:
				text = row[2]
				if float(text) < 99:
				print row
				found = "yes"
			if found == "yes":
				h.write(i)
				h.write("\n")
		with open("Duplicates2.csv", "rb") as f:
			f.next()			
			mycsv = csv.reader(f)
			for row in mycsv:
				text = row[2]
				if float(text) < 99:
				print row
				found = "yes"
			if found == "yes":
				h.write(i)
				h.write("\n")
		Gap=False
