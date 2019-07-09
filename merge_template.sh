#!/bin/bash
USER=ikk23
JOB_ID=
#$ -S /bin/bash
#$ -cwd
#$ -N
#$ -o
#$ -M ikk23@cornell.edu
#$ -m a
#$ -l h_rt=00:20:00

# Create working directory for job:
WORKDIR=/SSD/$USER/$JOB_ID
mkdir -p $WORKDIR
# Run from wd, not from home - IMPORTANT
cd $WORKDIR

#this is where the script and slim file are located
SCRIPT_LOCATION=/home/ikk23/slim
