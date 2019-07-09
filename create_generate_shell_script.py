import sys

"""
Use this file on your PC to generate one .sh script that can be submitted to the
cluster in order to run the generate_shell_scripts.py

Call at the command line with:

create_generate_shell_script.py <dimension_type> <interest_drive> <changing>

dimension_type includes: 1d_same_site, 1d_distant_site, 1d_shredder,
2d_same_site, 2d_distant_site, 2d_shredder

interest_drive includes: tads_aut, tade_supp, tads_y, x_shredder,
y_shredder, female_sterile, male_sterile, both_sterile, wt_drop

changing includes: beta_speed, fit_effic, density, inbreeding, resistance
"""

#figure out what will go in the command call
for arg in sys.argv:
    if arg.startswith("1d_same_site"):
        dimension_type = "1d_same_site"
        dimension = "1d"
    if arg.startswith("1d_distant_site"):
        dimension_type = "1d_distant_site"
        dimension = "1d"
    if arg.startswith("1d_shredder"):
        dimension_type = "1d_shredder"
        dimension = "1d"
    if arg.startswith("2d_same_site"):
        dimension_type = "2d_same_site"
        dimension = "2d"
    if arg.startswith("2d_distant_site"):
        dimension_type = "2d_distant_site"
        dimension = "2d"
    if arg.startswith("2d_shredder"):
        dimension_type = "2d_shredder"
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
        abbrev = "X" + "_" + dimension
    if arg.startswith("y_shredder"):
        interest_drive = "y_shredder"
        abbrev = "Y" + "_" + dimension
    if arg.startswith("tads_aut"):
        interest_drive = "tads_aut"
        abbrev = "TADS_AUT" + "_" + dimension
    if arg.startswith("tade_supp"):
        interest_drive = "tade_supp"
        abbrev = "TADE_SUPP" + "_" + dimension
    if arg.startswith("tads_y"):
        interest_drive = "tads_y"
        abbrev = "TADS_Y" + "_" + dimension
    if arg.startswith("beta_speed"):
        changing = "beta_speed"
    if arg.startswith("fit_effic"):
        changing = "fit_effic"
    if arg.startswith("density"):
        changing = "density"
    if arg.startswith("inbreeding"):
        changing = "inbreeding"
    if arg.startswith("resistance"):
        changing = "resistance"

with open("generate_template.sh", 'r') as f:
    script = f.read()
lines = script.split('\n')

lines[2] = "JOB_ID=generate_" + changing + "_" + abbrev #ex: generate_fit_effic_Y_2d
lines[5] = "#$ -N generate_" + changing + "_" + abbrev
lines[24] = "python generate_shell_scripts.py " + dimension_type + " " +\
interest_drive + " " + changing
new_script = '\n'.join(lines)

generate_shell_name = "generate_" + changing + "_" + abbrev + ".sh"

with open(generate_shell_name,'w+') as f:
    f.write(new_script)
