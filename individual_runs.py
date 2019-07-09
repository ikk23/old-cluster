import numpy as np
import sys

#use for 2d runs
#copy and paste slim output into slim_output.txt
with open("slim_output.txt","r") as f:
    body = f.read()

line_split = body.split('\n')

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
check_chasing = True
capacity = 40000

for line in line_split:
    if line.startswith("SUPPRESSED::"):
        spaced_line = line.split()
        suppressed = 1
        gen_suppressed = int(spaced_line[1])
    if line.startswith("ENDING_AFTER_1000"):
        spaced_line = line.split()
        stopped_1000 = 1
        rate_at_stop = float(spaced_line[1])
    if line.startswith("POP_PERSISTS::"):
        spaced_line = line.split()
        pop_persistance = 1
        gen_persistance = int(spaced_line[1])
    if line.startswith("EQUILIBRIUM::"):
        spaced_line = line.split()
        equilibrium = 1
        gen_equilibrium = int(spaced_line[1])
        check_chasing = False #no longer true chasing

if (check_chasing):
    #only will have chasing if we find a wt allele minimum and a green's coefficient maximum
    wt_min = False
    eq_check = 0.8*2*capacity
    wt = []
    gen = []
    pops = []
    gcs = []
    for line in line_split:
        if line.startswith("WT_ALLELES::"):
            spaced_line = line.split()
            wt_alleles = int(spaced_line[1])
            this_gen = int(spaced_line[2])
            this_popsize = int(spaced_line[3])
            this_gc = float(spaced_line[5]) #gc space here
            wt.append(wt_alleles)
            gen.append(this_gen)
            pops.append(this_popsize)
            gcs.append(this_gc)

    #determine if there was a wt allele minimum
    last_gen = len(gen) - 1
    for i in range(len(wt)):
        #check 1: have at least 5 generations occurred since tracking began
        #or was this at least 5 generations prior to the end of the simulation?
        if (i > 4) and (i < (last_gen - 4)):
            this_count = wt[i]
            #check 2: is the wt count less than 80% of its eq value?
            if (this_count < eq_check):
                last_count = wt[i-1]
                next_count = wt[i+1]
                #check 3: was the last generation's wt allele count higher
                if (last_count > this_count) and (next_count > this_count):
                    prior_three = wt[(i-3):i]
                    next_three = wt[(i+1):(i+4)]
                    prior_avg = np.average(prior_three)
                    next_avg = np.average(next_three)
                    #check 4: was the average of the last 3 generations' wt allele
                    #counts higher and was the average of the next 3 generations'
                    #wt allele counts higher?
                    if (prior_avg > this_count) and (next_avg > this_count):
                        wt_min = True #found a minimum
                        print("\n wts")
                        print(wt)
                        print("\n gens")
                        print(gen)
                        gen_wt_min = gen[i]
                        print('\nfound wt min at '+str(gen_wt_min) + '\n')
                        break

    #if we've found a wt allele minimum, now check for a gc maximum
    if wt_min:
        for i in range(len(gcs)):
            #check 1: have at least 5 generations occurred since tracking began
            #or was this at least 5 generations prior to the end of the simulation?
            if (i > 4) and (i < (last_gen - 4)): #need 5 gens on each side
                this_gc_count = gcs[i]
                last_gc_count = gcs[i-1]
                next_gc_count = gcs[i+1]
                #check 2: was the last generation's green's coefficient lower
                #and was the next generation's green's coefficient count lower?
                if (last_gc_count < this_gc_count) and (next_gc_count < this_gc_count):
                    prior_three = gcs[(i-3):i]
                    next_three = gcs[(i+1):(i+4)]
                    prior_avg = np.average(prior_three)
                    next_avg = np.average(next_three)
                    #check 3: was the average of the last 3 generations' green's
                    #coefficients lower and was the average of the next 3 generations'
                    #green's coefficients lower
                    if (prior_avg < this_gc_count) and (next_avg < this_gc_count):
                        #found both a wt_min and gc_max
                        chased = 1
                        gen_gc_max = gen[i]
                        gen_chase_started = min(gen_gc_max, gen_wt_min)
                        print('\nalso found gc max at ' + str(gen_gc_max))
                        print('\n gen chased started is ' + str(gen_chase_started))
                        pos = gen.index(gen_chase_started)
                        #summary stats of chase:
                        gcs_of_interest = gcs[(pos+3):-2]
                        gc_average = np.average(gcs_of_interest)
                        gc_variance = np.var(gcs_of_interest)
                        print('\nAVG GC DURING CHASE='+str(gc_average))
                        popsizes_of_interest = pops[(pos+3):-2]
                        print("\ngcs:")
                        print(gcs)
                        avg_pop_during_chase = np.average(popsizes_of_interest)
                        var_pop_during_chase = np.var(popsizes_of_interest)
                        duration_of_chasing = gen[-1] - gen_chase_started
                        print('\nchasing lasted for ' + str(duration_of_chasing) + 'generations.')
                        break
    else:
        print('no wt min - chase not evaluated')
