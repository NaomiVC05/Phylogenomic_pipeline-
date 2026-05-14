#!/bin/bash
#SBATCH --job-name=run_phylo_analyses
#SBATCH --ntasks-per-node=24
#SBATCH --time=24:0:0
#SBATCH --output=run_phylo.out
#SBATCH --error=run_phylo.err
#SBATCH --mail-user=villalon@oregonstate.edu
#SBATCH --mail-type=END

#How to submit the job:
#sbatch -p forsythe.q -A forsythe run_phylogenomic.sh


python phylogenomic_analyses.py 

#How to check the amount of treefile already ran 
#ls *treefile | wc -l 

#How to check my job:
#squeue -u $USER
