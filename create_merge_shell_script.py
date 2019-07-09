import sys

"""
Use this file on your PC to generate the .sh file that will be submitted to the
cluster in order to merge csv files.

Call at the command line with:

create_merge_shell_script.py <dimension_type> <interest_drive> <changing>

dimension_type includes: 1d_same_site, 1d_distant_site, 1d_shredder,
2d_same_site, 2d_distant_site, 2d_shredder

interest_drive includes: tads_aut, tade_supp, tads_y, x_shredder,
y_shredder, female_sterile, male_sterile, both_sterile, wt_drop

changing includes: beta_speed, fit_effic, density, inbreeding, resistance
"""

txt='' #concacenate onto this

#1- figure out which drive this is
for arg in sys.argv:
    if arg.startswith("1d_same_site"):
        dimension = "1d"
        dimension_type = "1d_same_site"
    if arg.startswith("1d_distant_site"):
        dimension = "1d"
        dimension_type = "1d_distant_site"
    if arg.startswith("1d_shredder"):
        dimension = "1d"
        dimension_type = "1d_shredder"
    if arg.startswith("2d_same_site"):
        dimension = "2d"
        dimension_type = "2d_same_site"
    if arg.startswith("2d_distant_site"):
        dimension = "2d"
        dimension_type = "2d_distant_site"
    if arg.startswith("2d_shredder"):
        dimension = "2d"
        dimension_type = "2d_shredder"
    if arg.startswith("wt_drop"):
        interest_drive = "wt_drop"
        abbrev = "WT" + "_" + dimension
    if arg.startswith("female_sterile"):
        interest_drive = "female_sterile"
        abbrev = "FEMALE"+ "_" + dimension
    if arg.startswith("male_sterile"):
        interest_drive = "male_sterile"
        abbrev = "MALE"+ "_" + dimension
    if arg.startswith("both_sterile"):
        interest_drive = "both_sterile"
        abbrev = "BOTH"+ "_" + dimension
    if arg.startswith("x_shredder"):
        interest_drive = "x_shredder"
        abbrev = "X"+ "_" + dimension
    if arg.startswith("y_shredder"):
        interest_drive = "y_shredder"
        abbrev = "Y"+ "_" + dimension
    if arg.startswith("tads_aut"):
        interest_drive = "tads_aut"
        abbrev = "TADS_AUT"+ "_" + dimension
    if arg.startswith("tads_y"):
        interest_drive = "tads_y"
        abbrev = "TADS_Y"+ "_" + dimension
    if arg.startswith("tade_supp"):
        interest_drive = "tade_supp"
        abbrev = "TADE_SUPP"+ "_" + dimension
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
    if arg.startswith("fit_effic"):
        changing = "fit_effic"
        temp_line = "Fit{}_Efficiency{}_"
        values1 = [0.80,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.90,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99,1.00]
        values2 = [0.80,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.90,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99,1.00]
        size1 = 21
        size2 = 21
    if arg.startswith("density"):
        changing = "density"
        temp_line = "Capacity{}_Drop{}_"
        if dimension=="2d":
            values1 = [10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000, 110000, 120000, 130000, 140000, 150000, 160000, 170000, 180000, 190000, 200000]
            values2 = [101, 202, 303, 404, 505, 606, 707, 808, 909, 1010, 1111, 1212, 1313, 1414, 1515, 1616, 1717, 1818, 1919, 2020]
        else:
            values1 = [157, 471, 785, 1100, 1414, 1728, 2042, 2356, 2670, 2985, 3299]
            values2 = [2, 5, 8, 11, 14, 17, 21, 24, 27, 30, 33]
        size1 = 20
        size2 = 20
    if arg.startswith("inbreeding"):
        changing = "inbreeding"
        temp_line = "Avoidance{}_Penalty{}_"
        values1 = [-1.0,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
        values2 = [0.00,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.00]
        size1 = 21
        size2 = 21
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

csv_file_setup = temp_line + abbrev + ".csv" #ex: Beta{}_Speed{}_WT.csv
#ex: Avoidance0.4_Penalty0.2_X_2d.csv

if changing!="density" and changing!="resistance":
    for i in range(size1):
        for d in range(size2):
            param1_value = str(values1[i])
            param2_value = str(values2[d])
            csv_file = csv_file_setup.format(param1_value, param2_value)
            if (i == 0) and (d==0):
                txt += "\ncp $SCRIPT_LOCATION/" + csv_file + " .\n"
            else:
                txt+="cp $SCRIPT_LOCATION/" + csv_file + " .\n"
else:
    #for 1 parameter runs:
    for i in range(size1):
        param1_value = str(values1[i])

        if changing == "density":
            param2_value = str(values2[i])
            csv_file = csv_file_setup.format(param1_value, param2_value)
        else:
            csv_file = csv_file_setup.format(param1_value)

        if (i == 0):
            txt += "\ncp $SCRIPT_LOCATION/" + csv_file + " .\n"
        else:
            txt+="cp $SCRIPT_LOCATION/" + csv_file + " .\n"


txt+= "cp $SCRIPT_LOCATION/merge_all_csvs.py .\n"
txt+= "\npython merge_all_csvs.py " + dimension_type + " " + interest_drive + " " + changing + "\n"
txt+= "\ncp -rf  $WORKDIR/* $SCRIPT_LOCATION\n"
txt+= "\nrm -rf $WORKDIR"

with open("merge_template.sh", 'r') as f:
    script = f.read()
lines = script.split('\n')

lines[2] = "JOB_ID=merge_" + changing + "_" + abbrev
lines[5] = "#$ -N " + "merge_" + changing + "_" + abbrev
lines[6] = "#$ -o " + "data_" + changing + "_" + abbrev + ".csv"
#data will be named, for ex, "data_fit_effic_X_1d.csv"

current_script = '\n'.join(lines)
new_script = current_script + txt

merge_shell_name = "merge_" + changing + "_" + abbrev + ".sh"
#sh script will be named, for ex, "merge_fit_effic_X_1d.sh"

with open(merge_shell_name,'w+') as f:
    f.write(new_script)
