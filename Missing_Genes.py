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
		x=x+1
		while ">" not in h[x]:
			gene=gene+str(h[x])
			x=x+1
		genes.add(gene)
	x=x+1

with open("Missing_Genes.txt","w") as g:
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
call(["/home/alex/tRNAscan-SE-1.3.1/trnascan-1.4", B+"/"+str(i), "-o", "/home/alex/tRNA_Output/tRNAs_"+str(i)])
	f=open("/home/alex/tRNA_Output/tRNAs_"+str(i))
	h=f.readlines()
	f.close()
	s=0
	tRNAs=[]
	sequences=[]
	amino_acids=[]
	for n in h:
		s=s+1
		if "position" in n and "intron" not in n:
			numbers=re.findall("\d+", i)
			tRNAs.append(n)
			sequence=str(h[s])
			sequence=sequence.replace("potential tRNA sequence=","", 1)
			sequences.append(sequence)
		if "tRNA predict as" in n:
			amino_acid=str(n)
			amino_acid=amino_acid.replace("tRNA predict as a tRNA- ", "", 1)
			amino_acids.append(amino_acid)
		if "anticodon includes unknown bases" in n:
			amino_acid=str(n)
			amino_acids.append(amino_acid)
	print sequences
	tRNAs2=[]
	tested = list()
	tested1=[]
	v=0
	sequences2=[]
	amino_acids2=[]
	if sequences != []:
		while v<len(sequences):
			if "nn" not in str(sequences[v]):
				tRNAs2.append(tRNAs[v])
				sequences2.append(sequences[v])
				amino_acids2.append(amino_acids[v])
			v=v+1
	k=A+"/"+i
	m=open(k)
	l=m.readlines()
	f=open(B+"With_tRNAs", "w")
	for line in l:
		if "ORIGIN" not in line:
			f.write(str(line))
		else:
			w=0
			for target in tRNAs2:
				f.write("     tRNA            ")
				extranumbers=re.findall("\d+", target)
				if extranumbers[1] < extranumbers[0]:
					f.write("complement(")
				f.write(str(extranumbers[0]))
				f.write("..")
				f.write(str(extranumbers[1]))
				if extranumbers[1] < extranumbers[0]:
					f.write(")")
				f.write("\n")
				f.write("                      /gene=")
				f.write("tRNA "+str(amino_acids2[w][0:3]))
				f.write("\n")
				f.write("                      /note="+str(amino_acids2[w][4:]))	
				w=w+1
			f.write(str(line))
