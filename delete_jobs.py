temp_line = "Beta{}_Speed{}_" #add abbreviation
values1 = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] #beta values
values2 = [0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.010, 0.011, 0.012]
size1 = 11 #size of beta list
size2 = 11 #size of speed list

c = 1974592

txt = ''

while c < 1974664:
    txt += "qdel " + str(c) + " \n"
    c = c+1

with open('rm_jobs.txt', 'w+') as f:
    f.write(txt)
