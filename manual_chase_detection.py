import numpy as np

"""
Script for comparing chasing detection methods

Run SLiM on your PC and write down the generation that you observed chasing begin.
Then copy and paste the output into a txt file called "slim_output.txt" and
put it in the same working directory as this.
"""

with open("slim_output.txt","r") as f:
    body = f.read()

output = body.split('\n')

eq_check = 0.8*2*40000
wt = []
gen = []
pops = []
gcs = []

for line in output:
    if line.startswith("WT_ALLELES::"):
        spaced_line = line.split()
        wt_alleles = int(spaced_line[1])
        this_gen = int(spaced_line[2])
        this_popsize = int(spaced_line[3])
        this_gc = float(spaced_line[5])
        #create separate lists for each number
        wt.append(wt_alleles)
        gen.append(this_gen)
        pops.append(this_popsize)
        gcs.append(this_gc)

#for plotting
print('wts:')
print(wt)
print("\ngcs:")
print(gcs)
print("\ngens:")
print(gen)

wt_detect = False
gc_detect = False

last_gen = len(gen) - 1
for i in range(len(wt)):
    #check 1: did we fall below the wt allele threshold at least 5 gens ago
    #or was this at least 5 generations prior to the end of the simulation?
    if (i > 4) and (i < (last_gen - 4)):
        this_count = wt[i]
        if (this_count < eq_check): #is the wt count less than its 80% eq?
            last_count = wt[i-1]
            next_count = wt[i+1]
            #check 2: was the last generation's wt allele count higher
            #and was the next generation's wt allele count higher?
            if (last_count > this_count) and (next_count > this_count):
                prior_three = wt[(i-3):i]
                next_three = wt[(i+1):(i+4)]
                prior_avg = np.average(prior_three)
                next_avg = np.average(next_three)
                #check 3: was the average of the last 3 generations' wt allele
                #counts higher and was the average of the next 3 generations'
                #wt allele counts higher?
                if (prior_avg > this_count) and (next_avg > this_count):
                    chased = 1
                    wt_detect = True
                    gen_chased = gen[i]
                    gc_space_at_gen_chased = gcs[i]
                    print('\nWT METHOD- gen: ' + str(gen_chased) + ' wt alleles: ' + str(this_count)+ ' gc: ' + str(gc_space_at_gen_chased))
                    int_pops = pops[i:]
                    avgsize = np.average(int_pops)
                    break

for i in range(len(gcs)):
    #check 1: did we fall below the wt allele threshold at least 5 gens ago
    #or was this at least 5 generations prior to the end of the simulation?
    if (i > 4) and (i < (last_gen - 4)): #need 5 gens on each side
        this_gc_count = gcs[i]
        last_gc_count = gcs[i-1]
        next_gc_count = gcs[i+1]
        #check 2: was the last generation's green's coefficient lower
        #and was the next generation's green's coefficient count lower?
        if (last_gc_count < this_gc_count) and (next_gc_count < this_gc_count):
            prior_three = gcs[(i-3):i] #i - 3:i
            next_three = gcs[(i+1):(i+4)] #(i+1:i+4)
            prior_avg = np.average(prior_three)
            next_avg = np.average(next_three)
            #check 3: was the average of the last 3 generations' green's
            #coefficients lower and was the average of the next 3 generations'
            #green's coefficients lower?
            if (prior_avg < this_gc_count) and (next_avg < this_gc_count):
                gen_first_gc_space_max = gen[i]
                gc_detect = True
                first_gc_max = gcs[i]
                gcs_after_chase = gcs[(i+3):(len(gcs)-3)] #avg this gen + 3 - end minus 3
                avg_gc_chase_onwards = np.average(gcs_after_chase)
                var_gc_chase_onwards = np.var(gcs_after_chase)
                print('GC METHOD- gen: '+str(gen_first_gc_space_max)+ ' wt alleles: '+ str(wt[i])+ ' gc: ' + str(first_gc_max))
                print('avg gc after chase='+str(avg_gc_chase_onwards))
                print('var in gc after chase=' + str(var_gc_chase_onwards))
                break


if wt_detect and gc_detect:
    print('\nBOTH REPORT CHASING!')
    gen_of_start = min(gen_first_gc_space_max, gen_chased)
    print('our start should be ' + str(gen_of_start))
else:
    print('INSUFFICIENT EVIDENCE - NO CHASE')
