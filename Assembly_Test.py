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

#Extract regions near assembly gaps
x=0
Genome=False
Sequence=""
for i in g:
	x=x+1
	if ">" in g[x]:
		Genome=True
	while Genome==True and x<len(g):
		Sequence=Sequence+str(g[x])
h=open("Duplicated_Genes", "w")
for i in g:
	if "assembly_gap" in i:
		coords1=int(re.findall("\d+", i))
		coords2=re.findall("..\d+",i)
		coords2=int(coords2.replace("..", ""))
		gap1=g[coords1-1000:coords1]
		gap2=g[coords2:coords2+1000]
		f=open("temp_query.fasta", "w")
		f.write(str(gap1))
		f.close()
		call(["blastn", "-query", "temp_query.fasta", "-db", A, "-outfmt", "10", "-o", "Duplicates1.csv", "-m", "8"])
		f=open("temp_query.fasta", "w")
		f.write(str(gap2))
		f.close()
		call(["blastn", "-query", "temp_query.fasta", "-db", A, "-outfmt", "10", "-o", "Duplicates2.csv", "-m", "8"])
		found = "no"
		with open("Duplicates.csv", "rb") as f:
			f.next()			
			mycsv = csv.reader(f)
			for row in mycsv:
				text = row[2]
				if float(text) < 1e-200:
				print row
				found = "yes"
			if found == "yes":
			h.write(i)
			h.write("\n")
