#!/bin/bash
USER=ikk23
JOB_ID=generate_resistance_FEMALE_2d
#$ -S /bin/bash
#$ -cwd
#$ -N generate_resistance_FEMALE_2d
#$ -o S.$JOB_ID.out
#$ -M ikk23@cornell.edu
#$ -m a
#$ -j y
#$ -l h_rt=00:05:00

# Create working directory for job:
WORKDIR=/SSD/$USER/$JOB_ID
mkdir -p $WORKDIR
# Run from wd, not from home - IMPORTANT
cd $WORKDIR

#this is where the script and slim file are located
SCRIPT_LOCATION=/home/ikk23/slim
#copy files over to the new directory
cp $SCRIPT_LOCATION/generate_shell_scripts.py .
cp $SCRIPT_LOCATION/template_shell_script.sh .

python generate_shell_scripts.py 2d_same_site female_sterile resistance

#copy the excel file back into my slim-build folder
cp -rf  $WORKDIR/* $SCRIPT_LOCATION

#remove this scratch directory
rm -rf $WORKDIR
