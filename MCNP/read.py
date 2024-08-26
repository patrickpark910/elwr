import os, glob
import pandas as pd
import numpy as np

directories = [
    './A-cladZr-Li00-bu10',
    ]

cols = ['EFPD','Burnup','k-eff','std-dev','rho','Pf1%','Pf2%','Pf3%','Pf4%','Pf5%','Pf1/FA%','Pf2/FA%','Pf3/FA%','Pf4/FA%','Pf5/FA%','U235','U238','PU239','PU240','PU241','PU242']
bu_list = [0,0.1,1,5,10,15,20,25]
isotope_list = ['U235','U238','PU239','PU240','PU241','PU242']
cells = [111,121,211,221,311,321,411,421,511,521]

u235_start = 4e6*(238.05/(238.05+31.998))*0.035/1e3     # g
u238_start = 4e6*(238.05/(238.05+31.998))*(1-0.035)/1e3 # g

for directory in directories:
    
    file_list = glob.glob(os.path.join(directory, '*.mcode.out'))

    for file_name in file_list:
        with open(file_name, 'r') as file:
            
            df = pd.DataFrame(np.zeros((len(bu_list), len(cols))),index=bu_list,columns=cols)
            df.loc[0,'U235'], df.loc[0,'U238'] = u235_start, u238_start
            tb1, tb3, tb6a, tb6b = False, False, False, False

            for line in file:

                if "* TABLE 1. REACTIVITY vs TIME/BURNUP *" in line:
                    tb1 = True
                    time, burnup, keff, stddev, rho = [], [], [], [], []
                    print('1')
                elif tb1 and len(line.split())==7 and line.lstrip()[0].isdigit():
                    print('2')
                    e = line.split()
                    time.append(e[1]), burnup.append(e[3]), keff.append(e[4]), stddev.append(e[5]), rho.append(e[6])
                    print(keff, stddev, rho)

                if "* TABLE 3. BURNUP/POWER MAP *" in line:
                    tb1, tb3 = False, True
                    df['EFPD'], df['Burnup'], df['k-eff'], df['std-dev'], df['rho'] = time, burnup, keff, stddev, rho

                elif tb3:
                    if line.startswith("Pf(111)"):
                        pf_11 = [float(value) for value in line.split()[1:]]
                    elif line.startswith("Pf(121)"):
                        pf_12 = [float(value) for value in line.split()[1:]]
                        pf_1 = [(a + b)*100 for a, b in zip(pf_11, pf_12)]
                        df['Pf1%'], df['Pf1/FA%'] = pf_1, [c/8 for c in pf_1]

                    elif line.startswith("Pf(211)") or line.startswith("Pf(311)") or line.startswith("Pf(411)"):
                        pf_21 = [float(value) for value in line.split()[1:]]
                    elif line.startswith("Pf(221)") or line.startswith("Pf(321)") or line.startswith("Pf(421)"):
                        pf_22 = [float(value) for value in line.split()[1:]]
                        pf_2 = [(a + b)*100 for a, b in zip(pf_21, pf_22)]
                        pffa_2 = [c/4 for c in pf_2]

                        if line.startswith("Pf(221)"):
                            df['Pf2%'], df['Pf2/FA%'] = pf_2, pffa_2
                        elif line.startswith("Pf(321)"):
                            df['Pf3%'], df['Pf3/FA%'] = pf_2, pffa_2
                        elif line.startswith("Pf(421)"):
                            df['Pf4%'], df['Pf4/FA%'] = pf_2, pffa_2

                    elif line.startswith("Pf(511)"):
                        pf_51 = [float(value) for value in line.split()[1:]]
                    elif line.startswith("Pf(521)"):
                        pf_52 = [float(value) for value in line.split()[1:]]
                        pf_5 = [(a + b)*100 for a, b in zip(pf_51, pf_52)]
                        df['Pf5%'], df['Pf5/FA%'] = pf_5, [c for c in pf_5]

                if "* TABLE 6. COMPOSITION TABLE (GRAMS) *" in line:
                    tb3, tb6a = False, True

                elif tb6a:
                    e = line.split()
                    for i in isotope_list:
                        if len(e) > 10 and e[1] == i: # and e[1] == i:
                            df[i] = df[i] + [0, float(e[3])/1e3, float(e[5])/1e3, float(e[7])/1e3, float(e[9])/1e3, float(e[11])/1e3, float(e[13])/1e3, 0]

                if "* TABLE 6. COMPOSITION TABLE (GRAMS) (CONT)" in line:
                    tb6a, tb6b = False, True
                    print("new line")

                elif tb6b:
                    e = line.split()
                    for i in isotope_list:
                        if len(e) > 2 and e[1] == i: # and e[1] == i:
                            df[i] = df[i] + [0, 0, 0, 0, 0, 0, 0, float(e[3])/1e3]

                if "* TABLE 7. NEUTRON ABSORPTION RATE TABLE (neutrons/sec) *" in line:
                    tb6a, tb6b = False, False
        print(df)
        df.to_csv(f"./{file_name.split('.')[-3]}.csv", index=False)
        print(f"Wrote {file_name.split('.')[-3]}.csv")
