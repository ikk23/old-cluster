#!/bin/bash
USER=ikk23
JOB_ID=
#$ -S /bin/bash
#$ -cwd
#$ -N
#$ -o
#$ -M ikk23@cornell.edu
#$ -m a
#$ -j y
#$ -l h_rt=23:00:00
#$ -l h_vmem=30G

# Create working directory for job:
WORKDIR=/SSD/$USER/$JOB_ID
mkdir -p $WORKDIR
# Run from wd, not from home - IMPORTANT
cd $WORKDIR

#this is where the script and slim file are located
SCRIPT_LOCATION=/home/ikk23/slim
#copy files over to the new directory
cp $SCRIPT_LOCATION/1d_same_site_spatial.slim .
cp $SCRIPT_LOCATION/1D_same_site.py .

PATH=$PATH:/home/ikk23/slim_install/build
export PATH

python shredder_supp.py shredder_drives_vectorized.slim x_shredder fit_effic fitness=0.8 efficiency=0.8

#copy the excel file back into my slim-build folder
cp -rf  $WORKDIR/* $SCRIPT_LOCATION

#remove this scratch directory
rm -rf $WORKDIR
