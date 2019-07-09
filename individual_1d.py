import numpy as np
import sys

#use for 1d runs
#copy and paste slim output into slim_output.txt
with open("slim_output.txt","r") as f:
    body = f.read()

line_split = body.split('\n')

time_elapsed = 0
suppressed = 0
gen_suppressed = 10000
chased = 0
gen_chase_started = 10000
gc_average = 10000
gc_variance = 10000
avg_pop_during_chase = 1000000
var_pop_during_chase = 1000000
duration_of_chasing = 10000
pop_persistance = 0
gen_persistance = 10000
equilibrium = 0
gen_equilibrium = 10000
stopped_1000 = 0
rate_at_stop = 10000
thickness_accum = []
thickness = 100000 #will indicate something went wrong

for line in line_split:
    if line.startswith("TIMED_GENS::"):
        spaced_line = line.split()
        time_elapsed = int(spaced_line[1])
        print("time elapsed: " + str(time_elapsed))
    if line.startswith("SUPPRESSED::"):
        spaced_line = line.split()
        suppressed = 1
        gen_suppressed = int(spaced_line[1])
        print("suppressed in gen: " + str(gen_suppressed))
    if line.startswith("ENDING_AFTER_1000"):
        spaced_line = line.split()
        stopped_1000 = 1
        rate_at_stop = float(spaced_line[1])
        print("simulation ran till 1000")
    if line.startswith("POP_PERSISTS::"):
        spaced_line = line.split()
        pop_persistance = 1
        gen_persistance = int(spaced_line[1])
        print("drive lost in gen: " + str(gen_persistance))
    if line.startswith("EQUILIBRIUM::"):
        spaced_line = line.split()
        equilibrium = 1
        gen_equilibrium = int(spaced_line[1])
        print("equilibrium state in gen: " + str(gen_equilibrium))
    if line.startswith("THICKNESS::"):
        spaced_line = line.split()
        thickness_accum.append(float(spaced_line[1]))

#if an equilibrium state was achieved, this is skipped
if (equilibrium==0):
    for line in line_split:
        if line.startswith("CHASE_GEN::"):
            spaced_line = line.split()
            chased = 1
            gen_chase_started = int(spaced_line[1])
            print("CHASE IN GENERATION: " + str(gen_chase_started))
            break #only get the first chase

# if a chasing state was found, find the gc average and variance
# and the pop size average and variance from 3 gens after the chase
# to 3 generations from the end
# also find the duration of chasing and stop averaging drive thickness
# 3 generations from the chase
if (chased == 1):
    gen = []
    pops = []
    gcs = []
    for line in line_split:
        if line.startswith("WT_ALLELES::"):
            spaced_line = line.split()
            this_gen = int(spaced_line[2])
            this_popsize = int(spaced_line[3])
            this_gc = float(spaced_line[5]) #gc space here
            gen.append(this_gen)
            pops.append(this_popsize)
            gcs.append(this_gc)

    gcs_of_interest = gcs[(gen_chase_started+3):-2]
    gc_average = np.average(gcs_of_interest)
    gc_variance = np.var(gcs_of_interest)
    print("gc avg: " + str(gc_average) + " gc var: " + str(gc_variance))
    popsizes_of_interest = pops[(gen_chase_started+3):-2]
    avg_pop_during_chase = np.average(popsizes_of_interest)
    var_pop_during_chase = np.var(popsizes_of_interest)
    print("pop avg: " + str(avg_pop_during_chase) + " pop var: " + str(var_pop_during_chase))
    duration_of_chasing = gen[-1] - gen_chase_started
    print("chase lasted for: "+str(duration_of_chasing))
    thickness_of_interest = thickness_accum[:(gen_chase_started-4)]
    thickness = np.average(thickness_of_interest)
    print("thickness average, acct for chase = " + str(thickness))
else:
    #if chasing didn't occur, then suppression must have...
    #unless this was an equilibrium state x-shredder
    print("NO CHASE")
    if suppressed == 1:
        thickness_of_interest = thickness_accum[:(gen_suppressed-4)]
        thickness = np.average(thickness_of_interest)
        print("thickness average, acct for supp = " + str(thickness))
    else:
        thickness = np.average(thickness_accum)
        print("thickness average, no chase and no supp = " + str(thickness))
