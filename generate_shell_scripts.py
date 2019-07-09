import sys

"""
Use this file on the cluster to create many .sh scripts to run SLiM at set parameters.

A .sh generate file will need to call this with:

<generate_shell_scripts.py> <dimension_type> <interest_drive> <changing>

-Note: use create_generate_shell_script.py to generate this

dimension_type includes: 1d_same_site, 1d_distant_site, 1d_shredder,
2d_same_site, 2d_distant_site, 2d_shredder

interest_drive includes: tads_aut, tade_supp, tads_y, x_shredder,
y_shredder, female_sterile, male_sterile, both_sterile, wt_drop

changing includes: beta_speed, fit_effic, density, inbreeding, resistance
"""

for arg in sys.argv:
    if arg.startswith("1d_same_site"):
        slim_file = "1d_same_site_spatial.slim"
        python_file = "1d_same_site_parsing.py"
        dimension = "1d"
    if arg.startswith("1d_distant_site"):
        slim_file = "1d_distant_site_spatial.slim"
        python_file = "1d_distant_site_parsing.py"
        dimension = "1d"
    if arg.startswith("1d_shredder"):
        slim_file = "1d_shredder_drives_spatial.slim"
        python_file = "1d_shredder_drives_parsing.py"
        dimension = "1d"
    if arg.startswith("2d_same_site"):
        slim_file = "2d_same_site_spatial.slim"
        python_file = "2d_same_site_parsing.py"
        dimension = "2d"
    if arg.startswith("2d_distant_site"):
        slim_file = "2d_distant_site_spatial.slim"
        python_file = "2d_distant_site_parsing.py"
        dimension = "2d"
    if arg.startswith("2d_shredder"):
        slim_file = "2d_shredder_drives_spatial.slim"
        python_file = "2d_shredder_drives_parsing.py"
        dimension = "2d"
    if arg.startswith("wt_drop"):
        interest_drive = "wt_drop"
        abbrev = "WT" + "_" + dimension
    if arg.startswith("female_sterile"):
        interest_drive = "female_sterile"
        abbrev = "FEMALE" + "_" + dimension
    if arg.startswith("male_sterile"):
        interest_drive = "male_sterile"
        abbrev = "MALE" + "_" + dimension
    if arg.startswith("both_sterile"):
        interest_drive = "both_sterile"
        abbrev = "BOTH" + "_" + dimension
    if arg.startswith("x_shredder"):
        interest_drive = "x_shredder"
        abbrev = "X" + "_" + dimension #ex: X_1d
    if arg.startswith("y_shredder"):
        interest_drive = "y_shredder"
        abbrev = "Y"+ "_" + dimension
    if arg.startswith("tads_aut"):
        interest_drive = "tads_aut"
        abbrev = "TADS_AUT"+ "_" + dimension
    if arg.startswith("tade_supp"):
        interest_drive = "tade_supp"
        abbrev = "TADE_SUPP"+ "_" + dimension
    if arg.startswith("tads_y"):
        interest_drive = "tads_y"
        abbrev = "TADS_Y" + "_" + dimension
    if arg.startswith("beta_speed"):
        changing = "beta_speed"
        temp_line = "Beta{}_Speed{}_" #add abbreviation
        values1 = [2.0 ,2.5,3.0,3.5,4.0,4.5,5.0,5.5,6.0,6.5,7.0,7.5,8.0,8.5,9.0,9.5,10.0,10.5,11.0,11.5,12.0]
        if dimension=="2d":
            values2 = [0.0100,0.0125,0.0150,0.0175,0.0200,0.0225,0.0250,0.0275,0.0300,0.0325,0.0350,0.0375,0.0400,0.0425,0.0450,0.0475,0.0500,0.0525,0.0550,0.0575, 0.0600]
        else:
            values2 = [0.002, 0.0025, 0.003, 0.0035, 0.004, 0.0045, 0.005, 0.0055, 0.006, 0.0065, 0.007, 0.0075, 0.008, 0.0085, 0.009, 0.0095, 0.01, 0.0105, 0.011, 0.0115, 0.012]
        size1 = 21 #size of beta list
        size2 = 21 #size of speed list
        param1 = "beta="
        param2 = "speed="
    if arg.startswith("fit_effic"):
        changing = "fit_effic"
        temp_line = "Fit{}_Efficiency{}_"
        values1 = [0.80,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.90,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99,1.00]
        values2 = [0.80,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.90,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99,1.00]
        size1 = 21
        size2 = 21
        param1 = "fitness="
        param2 = "efficiency="
    if arg.startswith("density"):
        changing = "density"
        temp_line = "Capacity{}_Drop{}_"
        if dimension=="2d":
            values1 = [10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000, 110000, 120000, 130000, 140000, 150000, 160000, 170000, 180000, 190000, 200000]
            values2 = [101, 202, 303, 404, 505, 606, 707, 808, 909, 1010, 1111, 1212, 1313, 1414, 1515, 1616, 1717, 1818, 1919, 2020]
        else:
            #fill in 1d equivalents later
            values1 = [157, 471, 785, 1100, 1414, 1728, 2042, 2356, 2670, 2985, 3299]
            values2 = [2, 5, 8, 11, 14, 17, 21, 24, 27, 30, 33]
        size1 = 20
        size2 = 20
        param1 = "capacity="
        param2 = "drop_size="
    if arg.startswith("inbreeding"):
        changing = "inbreeding"
        temp_line = "Avoidance{}_Penalty{}_"
        values1 = [-1.0,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
        values2 = [0.00,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.00]
        size1 = 21
        size2 = 21
        param1 = "avoidance="
        param2 = "penalty="
    if arg.startswith("resistance"):
        changing = "resistance"
        temp_line = "R1_Rate{}_"
        values1 = [0, 1e-06, 1.2589254117941661e-06, 1.584893192461114e-06, 1.9952623149688787e-06,\
        2.5118864315095823e-06, 3.162277660168379e-06, 3.981071705534969e-06, 5.011872336272725e-06,\
        6.30957344480193e-06, 7.943282347242822e-06, 1e-05, 1.2589254117941661e-05,\
        1.584893192461114e-05, 1.9952623149688786e-05, 2.5118864315095822e-05, 3.1622776601683795e-05,\
        3.9810717055349695e-05, 5.011872336272725e-05, 6.309573444801929e-05, 7.943282347242822e-05,\
        0.0001, 0.00012589254117941674, 0.00015848931924611142, 0.00019952623149688788,\
        0.00025118864315095795, 0.00031622776601683794, 0.00039810717055349735, 0.0005011872336272725,\
        0.000630957344480193, 0.0007943282347242813, 0.001]
        size1 = 32
        param1 = "r1_rate="

full_line = temp_line + abbrev #ex: Fit{}_Efficiency{}_X_1d

with open("template_shell_script.sh", 'r') as f:
    script = f.read()
lines = script.split('\n')
lines[22] = "cp $SCRIPT_LOCATION/" + slim_file + " ."
lines[23] = "cp $SCRIPT_LOCATION/" + python_file + " ."
script_list_txt_file = ""
script_no = 0

if changing!="density" and changing!="resistance":
    for i in range(size1):
        for d in range(size2):
            param1_value = str(values1[i])
            param1_line = param1 + param1_value #full line for parameter; ex: beta=2
            param2_value = str(values2[d])
            param2_line = param2 + param2_value
            lines[2]=("JOB_ID=" + full_line).format(param1_value, param2_value)
            lines[5] = ("#$ -N " + full_line).format(param1_value, param2_value)
            lines[6] = ("#$ -o "+ full_line + ".csv").format(param1_value, param2_value)
            lines[28] = "python " + python_file + " " + slim_file + " " + interest_drive +\
            " " + changing + " " + param1_line + " " + param2_line
            if script_no==0:
                lines[28]+=' init' #first file gets the csv header
            current_script = '\n'.join(lines)
            script_name = (full_line + ".sh").format(param1_value, param2_value)
            with open(script_name, 'w+') as f:
                f.write(current_script)
            script_list_txt_file += "\nqsub " + script_name + "\n"
            script_no+=1
else:
    for i in range(size1):
        param1_value = str(values1[i])
        param1_line = param1 + param1_value #full line for parameter; ex: beta=2

        if changing == "density":
            param2_value = str(values2[i])
            param2_line = param2 + param2_value
            lines[2]=("JOB_ID=" + full_line).format(param1_value, param2_value)
            lines[5] = ("#$ -N " + full_line).format(param1_value, param2_value)
            lines[6] = ("#$ -o "+ full_line + ".csv").format(param1_value, param2_value)
            lines[28] = "python " + python_file + " " + slim_file + " " + interest_drive +\
            " " + changing + " " + param1_line + " " + param2_line
            if script_no==0:
                lines[28]+=' init' #first file gets the csv header
            current_script = '\n'.join(lines)
            script_name = (full_line + ".sh").format(param1_value, param2_value)
        else:
            lines[2]=("JOB_ID=" + full_line).format(param1_value)
            lines[5] = ("#$ -N " + full_line).format(param1_value)
            lines[6] = ("#$ -o "+ full_line + ".csv").format(param1_value)
            lines[28] = "python " + python_file + " " + slim_file + " " + interest_drive +\
            " " + changing + " " + param1_line
            if script_no==0:
                lines[28]+=' init' #first file gets the csv header
            current_script = '\n'.join(lines)
            script_name = (full_line + ".sh").format(param1_value)

        with open(script_name, 'w+') as f:
            f.write(current_script)

        script_list_txt_file += "\nqsub " + script_name + "\n"
        script_no+=1

# a text file will be created in order to help submit all the .sh files
#ex: list_fit_effic_X.txt
with open(("list_" + changing +"_" + abbrev + ".txt"), 'w+') as f:
    f.write(script_list_txt_file)
