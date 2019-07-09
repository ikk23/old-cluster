import sys
import subprocess
import numpy as np

"""
Use this file for parsing 1d_shredder_drives_spatial.slim file output.

Each individual .sh file will call this python script with:

python 1d_shredder_drives_parsing.py 1d_shredder_drives_spatial.slim <interest_drive>
<changing> <param1=param1value> <param2=param2value> <init>

interest_drive for this includes: x_shredder, y_shredder, or wt_drop

changing includes:
    1. beta_speed: then param1 is "beta=" and param2 is "speed="
    2. fit_effic: then param1 is "fitness=" and param2 is "efficiency="
    3. density: then param1 is "density=" and there is NO param2.
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
                    male_only_drop,
                    female_only_drop,
                    num_grnas,
                    r1_rate,
                    speed,
                    x_shredder,
                    y_shredder,
                    track_by_cell,
                    track_ripleys_l,
                    number_of_cells,
                    no_drop):
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
    defineConstant(\"MALE_ONLY_DROP\", {});\n\
    defineConstant(\"FEMALE_ONLY_DROP\", {});\n\
    defineConstant(\"NUM_GRNAS\", {});\n\
    defineConstant(\"R1_OCCURRENCE_RATE\", {});\n\
    defineConstant(\"SPEED\", {});\n\
    defineConstant(\"X_SHREDDER\", {});\n\
    defineConstant(\"Y_SHREDDER\", {});\n\
    defineConstant(\"TRACK_BY_CELL\", {});\n\
    defineConstant(\"TRACK_RIPLEYS_L\", {});\n\
    defineConstant(\"NUMBER_OF_CELLS\", {});\n\
    defineConstant(\"NO_DROP\", {});\n    /*".format(
                    capacity,
                    density_interaction_distance,
                    fitness,
                    drop_size,
                    drop_radius,
                    embryo_resistance_rate,
                    germline_resistance_rate,
                    beta,
                    "T" if heterozygous_drop else "F",
                    "T" if male_only_drop else "F",
                    "T" if female_only_drop else "F",
                    num_grnas,
                    r1_rate,
                    speed,
                    "T" if x_shredder else "F",
                    "T" if y_shredder else "F",
                    "T" if track_by_cell else "F",
                    "T" if track_ripleys_l else "F",
                    number_of_cells,
                    "T" if no_drop else "F")

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


def parse_slim_out(slim_output):
    """
    Arguments: slim output to parse, capacity for chase analysis, and
    an indication of whether we want to track bin times

    Returns:
        1. Number of generations from when the starting bin [0.25-0.3]'s
        population size fell below / to half of its equilibrium value
        (<= 0.5*CAPACITY/20) until when the ending bin [0.75-0.8] reached this.
        Note: If the population-persistance or equilibrium state prevented this
        progression, this entry is 0.
    Returns:
        2. Whether the drive suppressed (0 or 1)
        3. Generation suppressed (10,000 or gen_suppressed) - drop is generation 0

        4. Whether the drive chased (0 or 1)
        5. Generation chasing began (gen_chase_started or 10,000)
        6. Green's coefficient average from (gen_chase_started+3):(ending_gen-3)
        (gc_average or 10,000)
        7. Green's coefficient variance from (gen_chase_started+3):(ending_gen-3)
        (gc_variance or 10,000)
        8. Average population size from (gen_chase_started+3):(ending_gen-3)
        (avg_pop_during_chase or 1,000,000)
        9. Variance in population size from (gen_chase_started+3):(ending_gen-3)
        (var_pop_during_chase or 1,000,000)
        10. Duration of chasing (last_gen - gen_chase_started or 10,000)

        -Note: chasing occurs when there is less than 10 individuals in a slice and
        more than 50 individuals to the left

        11. Whether a wt population-persistance state occurred (drive was LOST
        but the population persisted) (0 or 1).
        12. Generation population-persistance state occurred (10,000 or gen).
        13. Whether an equilibrium state occurred (drive reached a 100%
        frequency but the population persisted) (0 or 1)
        14. Generation equilibrium state occurred (10,000 or gen)
        -applicable to the x-shredder
        -note: this means chasing is not measured

        15. Whether the simulation was stopped after 1000 generations (0 or 1)
        16. Rate of one drive if the simulation was stopped after 1000
        generations (10000 or rate)
        17. Drive thickness from five generations after the drop to the
        chasing gen - 5 if chasing occurred or the suppression gen - 5 if suppression
        occurred
    """
    line_split = slim_output.split('\n')

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
        popsizes_of_interest = pops[(gen_chase_started+3):-2]
        avg_pop_during_chase = np.average(popsizes_of_interest)
        var_pop_during_chase = np.var(popsizes_of_interest)
        duration_of_chasing = gen[-1] - gen_chase_started
        thickness_of_interest = thickness_accum[:(gen_chase_started-4)]
        thickness = np.average(thickness_of_interest)
    else:
        #if chasing didn't occur, then suppression must have...
        #unless this was an equilibrium state x-shredder
        if suppressed == 1:
            thickness_of_interest = thickness_accum[:(gen_suppressed-4)]
            thickness = np.average(thickness_of_interest)
        else:
            thickness = np.average(thickness_accum)

    return (time_elapsed, suppressed, gen_suppressed, chased, gen_chase_started, gc_average,\
    gc_variance, avg_pop_during_chase, var_pop_during_chase, duration_of_chasing,\
    pop_persistance, gen_persistance, equilibrium, gen_equilibrium,\
    stopped_1000, rate_at_stop, thickness)


def cfg_params():
    """
    Configure parameters from command line.
    """
    # Default values:
    capacity = 3927
    density_interaction_distance = 0.002
    fitness = 0.95
    drop_size = 40
    drop_radius = 0.01
    embryo_resistance_rate = 0.0
    germline_resistance_rate = 0.99
    beta = 6
    heterozygous_drop = True
    male_only_drop = False
    female_only_drop = False
    num_grnas = 1
    r1_rate = 0.0
    speed = 0.008
    x_shredder = False
    y_shredder = False
    track_by_cell = True
    track_ripleys_l = False
    number_of_cells = 40
    no_drop = False
    print_csv_header = False

    for arg in sys.argv:
        if arg.startswith("x_shredder"):
            x_shredder = True
            heterozygous_drop = False
            male_only_drop = True
        if arg.startswith("y_shredder"):
            y_shredder = True
            female_only_drop = True
            heterozygous_drop = True
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
            germline_resistance_rate = float(arg.split('=')[1])
        if arg.startswith("init"):
            print_csv_header = True

    #result is a giant tuple used to run slim
    return (capacity, density_interaction_distance, fitness, drop_size,\
    drop_radius, embryo_resistance_rate, germline_resistance_rate,\
    beta, heterozygous_drop, male_only_drop, female_only_drop, num_grnas,\
    r1_rate, speed, x_shredder, y_shredder, track_by_cell, track_ripleys_l,\
    number_of_cells, no_drop, print_csv_header)

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

    for arg in sys.argv:
        if arg.startswith("beta_speed"):
            interest_param1 = ("Low-Density Growth Rate", params[7])
            interest_param2 = ("Migration Rate", params[13])
        if arg.startswith("fit_effic"):
            interest_param1 = ("Fitness", params[2])
            interest_param2 = ("Drive Efficiency", params[6])
        if arg.startswith("density"):
            interest_param1 = ("Density", params[0])
            interest_param2 = "None"

    if params[20]:
        head = ",Time Elapsed, Suppressed, Gen Suppressed, Chased, Gen Chased, Avg GC during Chase, Var in GC during Chase, Avg Popsize during Chase, Var in Popsize during Chase, Duration of Chase, Drive Lost, Gen Drive Lost, Equilibrium State, Gen Equilibrium State, Simulation Stopped after 1000, Rate One Drive at End, Thickness\n"
        if interest_param2!= "None":
            csv_str = interest_param1[0] + "," + interest_param2[0] + head
        else:
            csv_str = interest_param1[0] + head
    else:
        csv_str = ""

    generate_slim(filename, params[0], params[1], params[2], params[3],\
    params[4],  params[5],  params[6], params[7], params[8], params[9],\
    params[10], params[11], params[12], params[13], params[14], params[15],
    params[16], params[17], params[18], params[19])

    for i in range(20): #20 replicates
        slim_result = run_slim(filename)
        time_elapsed, suppressed, gen_suppressed, chased, gen_chase_started, gc_average, gc_variance, avg_pop_during_chase, var_pop_during_chase, duration_of_chasing, pop_persistance, gen_persistance, equilibrium, gen_equilibrium, stopped_1000, rate_at_stop, thickness= parse_slim_out(slim_result)
        if interest_param2!= "None":
            csv_line = "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(interest_param1[1],interest_param2[1], time_elapsed, suppressed, gen_suppressed, chased, gen_chase_started, gc_average, gc_variance, avg_pop_during_chase, var_pop_during_chase, duration_of_chasing, pop_persistance, gen_persistance, equilibrium, gen_equilibrium, stopped_1000, rate_at_stop, thickness)
        else:
            csv_line = "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(interest_param1[1], time_elapsed, suppressed, gen_suppressed, chased, gen_chase_started, gc_average, gc_variance, avg_pop_during_chase, var_pop_during_chase, duration_of_chasing, pop_persistance, gen_persistance, equilibrium, gen_equilibrium, stopped_1000, rate_at_stop, thickness)
        csv_str = csv_str + csv_line

    print(csv_str)


if __name__ == "__main__":
    main()
