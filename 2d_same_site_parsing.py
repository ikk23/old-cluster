import sys
import subprocess
import numpy as np

"""
Use this file for parsing 2d_same_site_spatial.slim file output.

Each individual .sh file will call this python script with:

python 2d_same_site_parsing.py 2d_same_site_spatial.slim <interest_drive>
<changing> <param1=param1value> <param2=param2value> <init>

interest_drive for this includes: female_sterile, male_sterile, both_sterile,
tade_supp, and wt_drop

changing includes:
    1. beta_speed: then param1 is "beta=" and param2 is "speed="
    2. fit_effic: then param1 is "fitness=" and param2 is "efficiency="
    3. density: then param1 is "density=" and there is NO param2.
    4. inbreeding: then param1 is "avoidance=" and param2 is "efficiency="
    5. all: this is for trying to find "drive sensitive parameters".
    Many parameters may be passed in.
    6. resistance: then param1 is "r1_rate=" and there is NO param2.
"""

def generate_slim(filename,
                    capacity,
                    density_interaction_distance,
                    fitness,
                    drop_size,
                    drop_radius,
                    embryo_resistance_rate,
                    germline_resistance_rate,
                    beta,
                    heterozygous_drop,
                    homing_drive,
                    num_grnas,
                    recessive_female_drive,
                    recessive_male_drive,
                    r1_rate,
                    speed,
                    track_by_cell,
                    track_ripleys_l,
                    number_of_cells,
                    no_drop,
                    tade,
                    tade_suppression,
                    tade_double,
                    tads_autosomal_suppression,
                    tads_modification,
                    tare,
                    x_linked_drive,
                    inbreeding_avoidance_factor,
                    inbreeding_fecundity_penalty):
    """
    Configure a slim input file to be run and parsed.
    Slim file configuration is based on args to this function.
    :return: None. Generates a file.
    """
    # Configure the head of the slim file to reflect desired parameters.
    slim_head = "initialize() {\n    " +\
    "defineConstant(\"CAPACITY\", {});\n\
    defineConstant(\"DENSITY_INTERACTION_DISTANCE\", {});\n\
    defineConstant(\"DRIVE_FITNESS_VALUE\", {});\n\
    defineConstant(\"DROP_SIZE\", {});\n\
    defineConstant(\"DROP_RADIUS\", {});\n\
    defineConstant(\"EMBRYO_RESISTANCE_RATE\", {});\n\
    defineConstant(\"GERMLINE_RESISTANCE_RATE\", {});\n\
    defineConstant(\"GROWTH_AT_ZERO_DENSITY\", {});\n\
    defineConstant(\"HETEROZYGOUS_DROP\", {});\n\
    defineConstant(\"HOMING_DRIVE\", {});\n\
    defineConstant(\"NUM_GRNAS\", {});\n\
    defineConstant(\"RECESSIVE_FEMALE_STERILE_SUPPRESSION_DRIVE\", {});\n\
    defineConstant(\"RECESSIVE_MALE_STERILE_SUPPRESSION_DRIVE\", {});\n\
    defineConstant(\"R1_OCCURRENCE_RATE\", {});\n\
    defineConstant(\"SPEED\", {});\n\
    defineConstant(\"TRACK_BY_CELL\", {});\n\
    defineConstant(\"TRACK_RIPLEYS_L\", {});\n\
    defineConstant(\"NUMBER_OF_CELLS\", {});\n\
    defineConstant(\"NO_DROP\", {});\n\
    defineConstant(\"TADE\", {});\n\
    defineConstant(\"TADE_SUPPRESSION\", {});\n\
    defineConstant(\"TADE_DOUBLE_RESCUE\", {});\n\
    defineConstant(\"TADS_AUTOSOMAL_SUPPRESSION\", {});\n\
    defineConstant(\"TADS_MODIFICATION\", {});\n\
    defineConstant(\"TARE\", {});\n\
    defineConstant(\"X_LINKED_DRIVE\", {});\n\
    defineConstant(\"INBREEDING_AVOIDANCE_FACTOR\", {});\n\
    defineConstant(\"INBREEDING_FECUNDITY_PENALTY\", {});\n    /*".format(
                    capacity,
                    density_interaction_distance,
                    fitness,
                    drop_size,
                    drop_radius,
                    embryo_resistance_rate,
                    germline_resistance_rate,
                    beta,
                    "T" if heterozygous_drop else "F",
                    "T" if homing_drive else "F",
                    num_grnas,
                    "T" if recessive_female_drive else "F",
                    "T" if recessive_male_drive else "F",
                    r1_rate,
                    speed,
                    "T" if track_by_cell else "F",
                    "T" if track_ripleys_l else "F",
                    number_of_cells,
                    "T" if no_drop else "F",
                    "T" if tade else "F",
                    "T" if tade_suppression else "F",
                    "T" if tade_double else "F",
                    "T" if tads_autosomal_suppression else "F",
                    "T" if tads_modification else "F",
                    "T" if tare else "F",
                    "T" if x_linked_drive else "F",
                    inbreeding_avoidance_factor,
                    inbreeding_fecundity_penalty)

    # Add body from file.
    with open(filename, 'r') as f:
        slim_body = f.read()

    slim_full = slim_head + slim_body

    # Write final string to file.
    with open("py_gen_" + filename, 'w+') as f:
        f.write(slim_full)


def run_slim(filename):
    """
    Runs slim on file "py_gen_slimfile.slim".
    :return: Slim output as a string.
    """
    slim = subprocess.Popen(["slim", "py_gen_" + filename],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    out = slim.communicate()[0]
    return out


def parse_slim_out(slim_output, capacity):
    """
    Arguments: slim output to parse

    Returns:
        1. Whether the drive suppressed (0 or 1)
        2. Generation suppressed (10,000 or gen_suppressed) - drop is generation 0

        3. Whether the drive chased (0 or 1)
        4. Generation chasing began (gen_chase_started or 10,000)
        5. NONDRIVE green's coefficient average from (gen_chase_started+3):(ending_gen-3)
        (gc_average or 10,000)
        6. NONDRIVE green's coefficient variance from (gen_chase_started+3):(ending_gen-3)
        (gc_variance or 10,000)
        7. OVERALL green's coefficient average from (gen_chase_started+3):(ending_gen-3)
        (overall_gc_average or 10,000)
        8. OVERALL green's coefficient variance from (gen_chase_started+3):(ending_gen-3)
        (overall_gc_variance or 10,000)
        9. Average population size from (gen_chase_started+3):(ending_gen-3)
        (avg_pop_during_chase or 1,000,000)
        10. Variance in population size from (gen_chase_started+3):(ending_gen-3)
        (var_pop_during_chase or 1,000,000)
        11. Duration of chasing (last_gen - gen_chase_started or 10,000)

        -only considered to have chased if there was both a wt allele minimum
        and a NONDRIVE green's coefficient maximum.
        -If there was NOT both of these, then chased = 0; gen_chase_started = 10,000;
        gc_average=10,000; gc_variance = 10,000; and avg_pop_during_chase = 1,000,000.
        -If there WAS both of these, then:
            -chased = 1
            -gen_chase_started = the minimum of gen_min_wt_alleles and
            gen_max_greens_coeff (most of the time, this is the
            gen_max_greens_coeff- when the wt cluster first forms)
            -gc_average = the average NONDRIVE green's coefficient from the
            (gen_chase_started+3):(ending_gen-3)
            -gc_variance = the variance in NONDRIVE green's coefficient from the
            (gen_chase_started+3):(ending_gen-3)
            -overall_gc_average = the average OVERALL green's coefficient from the
            (gen_chase_started+3):(ending_gen-3)
            -overall_gc_variance = the variance in OVERALL green's coefficient from the
            (gen_chase_started+3):(ending_gen-3)
            -avg_pop_during_chase = the average population size from the
            (gen_chase_started+3):(ending_gen-3)
            -duration of chasing = the number of generations examined where
            chasing occurred (last_gen - gen_chase_started)

        12. Whether a wt population-persistance state occurred (drive was LOST
        but the population persisted) (0 or 1).
        13. Generation population-persistance state occurred (10,000 or gen).

        14. Whether an equilibrium state occurred (drive reached a 100%
        frequency but the population persisted) (0 or 1)
        15. Generation equilibrium state occurred (10,000 or gen)
        -applicable to the x-shredder
        -note: this means there was no true chasing

        16. Whether the simulation was stopped after 1000 generations (0 or 1)
        17. Rate of one drive if the simulation was stopped after 1000
        generations (10000 or rate)

        18. Whether r1 resistance occurred / 10,000 r1 alleles formed (0 or 1)
        19. Generation at which r1 resistance occurred (gen or 10,000)
    """
    line_split = slim_output.split('\n')

    suppressed = 0
    gen_suppressed = 10000
    chased = 0
    gen_chase_started = 10000
    gc_average = 10000
    gc_variance = 10000
    overall_gc_average = 10000
    overall_gc_variance = 10000
    avg_pop_during_chase = 1000000
    var_pop_during_chase = 1000000
    duration_of_chasing = 10000
    pop_persistance = 0
    gen_persistance = 10000
    equilibrium = 0
    gen_equilibrium = 10000
    stopped_1000 = 0
    rate_at_stop = 10000
    r1_resistance = 0
    gen_r1_resistance = 10000


    check_chasing = False

    for line in line_split:
        if line.startswith("SUPPRESSED::"):
            spaced_line = line.split()
            suppressed = 1
            gen_suppressed = int(spaced_line[1])
        if line.startswith("POTENTIAL_CHASE::"):
            check_chasing = True
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
        if line.startswith("RESISTANCE::"):
            spaced_line = line.split()
            r1_resistance = 1
            gen_r1_resistance = int(spaced_line[1])

    if (check_chasing):
        #only will have chasing if we find a wt allele minimum and a green's
        #coefficient maximum
        wt_min = False
        eq_check = 0.8*2*capacity
        wt = []
        gen = []
        pops = []
        gcs = []
        overall_gcs = []
        for line in line_split:
            if line.startswith("WT_ALLELES::"):
                spaced_line = line.split()
                wt_alleles = int(spaced_line[1])
                this_gen = int(spaced_line[2])
                this_popsize = int(spaced_line[3])
                this_gc = float(spaced_line[5]) #gc space here
                this_overall_gc = float(spaced_line[7])
                wt.append(wt_alleles)
                gen.append(this_gen)
                pops.append(this_popsize)
                gcs.append(this_gc)
                overall_gcs.append(this_overall_gc)

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
                    #and was the next generation's wt allele count higher?
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
                            gen_wt_min = gen[i]
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
                        #green's coefficients lower?
                        if (prior_avg < this_gc_count) and (next_avg < this_gc_count):
                            #found both a wt_min and gc_max
                            chased = 1
                            gen_gc_max = gen[i]
                            gen_chase_started = min(gen_gc_max, gen_wt_min)
                            pos = gen.index(gen_chase_started)
                            #summary stats of chase:
                            gcs_of_interest = gcs[(pos+3):-2]
                            gc_average = np.average(gcs_of_interest)
                            gc_variance = np.var(gcs_of_interest)
                            popsizes_of_interest = pops[(pos+3):-2]
                            avg_pop_during_chase = np.average(popsizes_of_interest)
                            var_pop_during_chase = np.var(popsizes_of_interest)
                            overall_gcs_of_interest = overall_gcs[(pos+3):-2]
                            overall_gc_average = np.average(overall_gcs_of_interest)
                            overall_gc_variance = np.var(overall_gcs_of_interest)
                            duration_of_chasing = gen[-1] - gen_chase_started
                            break

    return (suppressed, gen_suppressed, chased, gen_chase_started, gc_average,\
    gc_variance, overall_gc_average, overall_gc_variance, avg_pop_during_chase,\
    var_pop_during_chase, duration_of_chasing, pop_persistance, gen_persistance,\
    equilibrium, gen_equilibrium, stopped_1000, rate_at_stop, r1_resistance,\
    gen_r1_resistance)


def cfg_params():
    """
    Configure parameters from command line.
    """
    # Default values:
    capacity = 50000
    density_interaction_distance = 0.01
    fitness = 0.95
    drop_size = 505
    drop_radius = 0.01
    embryo_resistance_rate = 0.05 #default 0.05
    germline_resistance_rate = 0.05
    beta = 6
    heterozygous_drop = True
    homing_drive = True
    num_grnas = 1
    recessive_female_drive = False
    recessive_male_drive = False
    r1_rate = 0.0
    speed = 0.04
    track_by_cell = True
    track_ripleys_l = False
    number_of_cells = 64
    no_drop = False
    tade = False
    tade_suppression = False
    tade_double = False
    tads_autosomal_suppression = False
    tads_modification = False
    tare = False
    x_linked_drive = False
    inbreeding_avoidance_factor = 0.0
    inbreeding_fecundity_penalty = 0.0
    print_csv_header = False

    for arg in sys.argv:
        if arg.startswith("wt_drop"):
            no_drop = True
        if arg.startswith("female_sterile"):
            recessive_female_drive = True
            #new defaults
            fitness = 0.92
            germline_resistance_rate = 0.08
            speed = 0.035
            beta = 8
        if arg.startswith("male_sterile"):
            recessive_male_drive = True
        if arg.startswith("both_sterile"):
            recessive_female_drive = True
            recessive_male_drive = True
        if arg.startswith("capacity="):
            capacity = int(arg.split('=')[1])
        if arg.startswith("drop_size="):
            drop_size = int(arg.split('=')[1])
        if arg.startswith("beta="):
            beta = float(arg.split('=')[1])
        if arg.startswith("speed="):
            speed = float(arg.split('=')[1])
        if arg.startswith("fitness="):
            fitness = float(arg.split('=')[1])
        if arg.startswith("efficiency="):
            germline_resistance_rate = 1-float(arg.split('=')[1])
        if arg.startswith("avoidance="):
            inbreeding_avoidance_factor = float(arg.split('=')[1])
        if arg.startswith("penalty="):
            inbreeding_fecundity_penalty = float(arg.split('=')[1])
        if arg.startswith("r1_rate="):
            r1_rate = float(arg.split('=')[1])
        if arg.startswith("init"):
            print_csv_header = True

    #result is a giant tuple used to run slim
    return (capacity, density_interaction_distance, fitness, drop_size,\
    drop_radius, embryo_resistance_rate, germline_resistance_rate, beta,\
    heterozygous_drop, homing_drive, num_grnas, recessive_female_drive,\
    recessive_male_drive, r1_rate, speed, track_by_cell, track_ripleys_l,\
    number_of_cells, no_drop, tade, tade_suppression,tade_double,\
    tads_autosomal_suppression, tads_modification, tare,x_linked_drive,\
    inbreeding_avoidance_factor, inbreeding_fecundity_penalty, print_csv_header)

def main():
    """
    0. Configure from command line.
    1. Generate slim files with varying parameters.
        -figure out which parameters are of interest
    2. Run slim files as they are generated.
    3. Parse desired information from slim output.
    4. Output parsed information to csv file.
    """
    filename = sys.argv[1]
    # Now get args from cl:
    params = cfg_params()

    #not all of these may be used
    interest_param1 = "None"
    interest_param2 = "None"
    interest_param3 = "None"
    interest_param4 = "None"

    for arg in sys.argv:
        if arg.startswith("beta_speed"):
            interest_param1 = ("Low-Density Growth Rate", params[7])
            interest_param2 = ("Migration Rate", params[14])
        if arg.startswith("fit_effic"):
            interest_param1 = ("Fitness", params[2])
            interest_param2 = ("Drive Efficiency", 1-params[6])
        if arg.startswith("density"):
            interest_param1 = ("Density", params[0])
        if arg.startswith("inbreeding"):
            interest_param1 = ("Avoidance Factor", params[26])
            interest_param2 = ("Fecundity Penalty", params[27])
        if arg.startswith("all"):
            interest_param1 = ("Fitness", params[2])
            interest_param2 = ("Efficiency", 1-params[6])
            interest_param3 = ("Beta", params[7])
            interest_param4 = ("Speed", params[14])
        if arg.startswith("resistance"):
            interest_param1 = ("R1 Rate", params[13])

    if params[28]:
        head = ",Suppressed, Gen Suppressed, Chased, Gen Chased, Avg Nondrive GC during Chase, Var in Nondrive GC during Chase, Avg Overall GC during Chase, Var in Overall GC During Chase, Avg Popsize during Chase, Var in Popsize during Chase, Duration of Chase, Drive Lost, Gen Drive Lost, Equilibrium State, Gen Equilibrium State, Simulation Stopped after 1000, Rate One Drive at End, R1 Resistance Occurred, Gen 10000 R1 Alleles Formed\n"
        #only one parameter varied
        if interest_param2 == "None":
            csv_str = interest_param1[0] + head
        #two parameters varied
        elif interest_param3 == "None":
            csv_str = interest_param1[0] + "," + interest_param2[0] + head
        #four parameters varied
        else:
            csv_str = interest_param1[0] + "," + interest_param2[0] + "," + interest_param3[0] + "," + interest_param4[0] + head
    else:
        csv_str = ""

    generate_slim(filename, params[0], params[1], params[2], params[3],\
    params[4],  params[5],  params[6], params[7], params[8], params[9],\
    params[10], params[11], params[12], params[13], params[14], params[15],\
    params[16], params[17], params[18], params[19], params[20], params[21],\
    params[22], params[23], params[24], params[25], params[26], params[27])

    for i in range(20): #number of replicates
        slim_result = run_slim(filename)
        suppressed, gen_suppressed, chased, gen_chase_started, gc_average, gc_variance, overall_gc_average, overall_gc_variance, avg_pop_during_chase, var_pop_during_chase, duration_of_chasing, pop_persistance, gen_persistance, equilibrium, gen_equilibrium, stopped_1000, rate_at_stop, r1_resistance, gen_r1_resistance = parse_slim_out(slim_result, params[0])
        #only one parameter varied
        if interest_param2 == "None":
            csv_line = "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(interest_param1[1], suppressed, gen_suppressed, chased, gen_chase_started, gc_average, gc_variance, overall_gc_average, overall_gc_variance, avg_pop_during_chase, var_pop_during_chase, duration_of_chasing, pop_persistance, gen_persistance, equilibrium, gen_equilibrium, stopped_1000, rate_at_stop, r1_resistance, gen_r1_resistance)
        #two parameters varied
        elif interest_param3 == "None":
            csv_line = "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(interest_param1[1],interest_param2[1], suppressed, gen_suppressed, chased, gen_chase_started, gc_average, gc_variance, overall_gc_average, overall_gc_variance, avg_pop_during_chase, var_pop_during_chase, duration_of_chasing, pop_persistance, gen_persistance, equilibrium, gen_equilibrium, stopped_1000, rate_at_stop, r1_resistance, gen_r1_resistance)
        #four parameters varied
        else:
            csv_line = "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(interest_param1[1], interest_param2[1], interest_param3[1], interest_param4[1], suppressed, gen_suppressed, chased, gen_chase_started, gc_average, gc_variance, overall_gc_average, overall_gc_variance, avg_pop_during_chase, var_pop_during_chase, duration_of_chasing, pop_persistance, gen_persistance, equilibrium, gen_equilibrium, stopped_1000, rate_at_stop, r1_resistance, gen_r1_resistance)
        csv_str = csv_str + csv_line
    print(csv_str)


if __name__ == "__main__":
    main()
