#Create a list of unaligned files that we'll need to align

#Import needed python modules 
import os
import sys
import glob
import subprocess
from Bio import SeqIO
from Bio.Seq import Seq
from Bio import Phylo

#Create list to store output of my loop
top_list = list()


#Create a string variable that stores the folder path to the input files
file_name = "At_1G68100.fasta" 

input_folder_path = "/shared/forsythe/BB485/Week06/Brass_CDS_seqs/"

#full_path_to_file = input_folder_path + file_name

#print(full_path_to_file)

###Start For loop HERE 
input_file_path_list = glob.glob(input_folder_path+"*.fasta")
print(input_file_path_list)

for temp_file in input_file_path_list[0:10]: ###Remove 0-10 to do full run
    print(temp_file)

    full_path_to_file = temp_file
    print(full_path_to_file)


    ##Perform multiple sequence alignments using MAFFt

    #Create a folder for storing mafft output 
    out_folder_path = "/scratch/villalon/BB485/Week06/mafft_out/"

    # Create a new file path pointing to the output directory (this is how we tell mafft what to name the output)
    new_file_path = full_path_to_file.replace(input_folder_path, out_folder_path)

    #print(new_file_path)

    # Create a command string (this is what get called using the 'system call'.
    aln_cmd = 'mafft --auto --quiet '+full_path_to_file+' > '+new_file_path

    #Check the command
    #print(aln_cmd)

    #Run the command
    os.system(aln_cmd) #Uncomment this once you've double-checked that it's looking good.


    ##Perform phylogenetic tree construction using IQtree 

    #Create the command. -nt 2 means two threads. If running this from within a job submission, you could use more threads to make it go faster.
    tree_command = f"iqtree -s {new_file_path} -m TEST -nt 2"

    #Check the command 
    #print(tree_command)

    #Run the command using a 'system call'
    os.system(tree_command) #uncomment once you've check the command

    ##Perform tree topology tests with biopython 

    #Read in the tree and store as phylo object

    tree_file = new_file_path.replace(".fasta", ".fasta.treefile")
    #print(tree_file)

    temp_tree = Phylo.read(tree_file, "newick")


    #Loop through the tips in the tree to find which one contains Es (the outgroup)
    for tip in temp_tree.get_terminals():
        if "Es_" in tip.name:
            es_tip = tip
            #Stope the loop once we found the correct tip
            break
        
    #Root the tree by the outgroup taxon
    temp_tree.root_with_outgroup(es_tip)
        
    #Get a list of all terminal (aka tips) branches
    all_terminal_branches = temp_tree.get_terminals()
        
    #Loop through the branches and store the names of the tips of each
    for t in all_terminal_branches:
        if "Bs_" in t.name:
            Bs_temp=t 
        elif "Cr_" in t.name:
            Cr_temp=t
        elif "At_" in t.name:
            At_temp=t
        else:
            out_temp=t
            
    #Make lists of pairs of branches, so that we can ask which is monophyletic
    P1_and_P2=[Bs_temp, Cr_temp]
    P1_and_P3=[Bs_temp, At_temp]
    P2_and_P3=[Cr_temp, At_temp]
        

    #Use series of if/else statements to ask which pair in monophyletic
    if bool(temp_tree.is_monophyletic(P1_and_P2)):
        topo_str = "12top"
    elif bool(temp_tree.is_monophyletic(P1_and_P3)):
        topo_str = "13top"
    elif bool(temp_tree.is_monophyletic(P2_and_P3)):
        topo_str = "23top"
    else:
        topo_str = "Unknown"


    top_list.append(topo_str)

##End for loop here 


##Store output
# Print the full list
#print(top_list)

###Print end results 
print(f"Total number of trees: {len(top_list)}")
print(f"Number of 12top trees: {top_list.count('12top')}")
print(f"Number of 13top trees: {top_list.count('13top')}")
print(f"Number of 23top trees: {top_list.count('23top')}")
print(f"Number of Unknown trees: {top_list.count('Unknown')}")

#remove [0:10] 
#remove the mafft files 
#run this within a job