#Create a list of unaligned files that we'll need to align

#Import needed python modules 
import os
import sys
import glob
import subprocess
from Bio import SeqIO
from Bio.Seq import Seq
from Bio import Phylo


#Cretate a string variable that stores the folder path to the input files
file_name = "At_1G68100.fasta" 

input_folder_path = "/shared/forsythe/BB485/Week06/Brass_CDS_seqs/"

full_path_to_file = input_folder_path + file_name

print(full_path_to_file)
#Perform multiple sequence alignments 


#Perform phylogenetic tree construction using IQtree 


#Perform tree topology tests with biopython 



#Store output