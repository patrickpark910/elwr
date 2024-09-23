import os, glob
import pandas as pd
import numpy as np

directories = [
    # './A-cladZr-Li091-bu10',
    './A-cladZr-Li139-bu10',
    './A-cladZr-Li141-bu10',
    # './A-cladSS-Li057-bu10',
    # './A-cladSS-Li079-bu10',
    ]

cols = ['EFPD','Burnup','k-eff','std-dev','rho', 
        # 'Pf11%','Pf12%','Pf1tot%','Pf21%','Pf22%','Pf2tot%','Pf31%','Pf32%','Pf3tot%','Pf41%','Pf42%','Pf4tot%','Pf51%','Pf52%','Pf5tot%',
        'Pf11/FA%','Pf12/FA%','Pf1tot/FA%','Pf21/FA%','Pf22/FA%','Pf2tot/FA%','Pf31/FA%','Pf32/FA%','Pf3tot/FA%','Pf41/FA%','Pf42/FA%','Pf4tot/FA%','Pf51/FA%','Pf52/FA%','Pf5tot/FA%',
        'U235_11','U235_12','U235_1tot','U235_21','U235_22','U235_2tot','U235_31','U235_32','U235_3tot','U235_41','U235_42','U235_4tot','U235_51','U235_52','U235_5tot',
        'U238_11','U238_12','U238_1tot','U238_21','U238_22','U238_2tot','U238_31','U238_32','U238_3tot','U238_41','U238_42','U238_4tot','U238_51','U238_52','U238_5tot',
        'PU239_11','PU239_12','PU239_1tot','PU239_21','PU239_22','PU239_2tot','PU239_31','PU239_32','PU239_3tot','PU239_41','PU239_42','PU239_4tot','PU239_51','PU239_52','PU239_5tot',
        'PU240_11','PU240_12','PU240_1tot','PU240_21','PU240_22','PU240_2tot','PU240_31','PU240_32','PU240_3tot','PU240_41','PU240_42','PU240_4tot','PU240_51','PU240_52','PU240_5tot',
        'PU241_11','PU241_12','PU241_1tot','PU241_21','PU241_22','PU241_2tot','PU241_31','PU241_32','PU241_3tot','PU241_41','PU241_42','PU241_4tot','PU241_51','PU241_52','PU241_5tot',
        'PU242_11','PU242_12','PU242_1tot','PU242_21','PU242_22','PU242_2tot','PU242_31','PU242_32','PU242_3tot','PU242_41','PU242_42','PU242_4tot','PU242_51','PU242_52','PU242_5tot',
        'PU_11tot','PU_12tot','PU_1tot','PU_21tot','PU_22tot','PU_2tot','PU_31tot','PU_32tot','PU_3tot','PU_41tot','PU_42tot','PU_4tot','PU_51tot','PU_52tot','PU_5tot',
        'PU_11qual','PU_12qual','PU_1qual','PU_21qual','PU_22qual','PU_2qual','PU_31qual','PU_32qual','PU_3qual','PU_41qual','PU_42qual','PU_4qual','PU_51qual','PU_52qual','PU_5qual',
        'U235','U238','PU239','PU240','PU241','PU242','PUtot','PUqual']

bu_list = [0,0.1,1,5,10,15] # ,20] # ,20,25]
isotope_list = ['U235','U238','PU239','PU240','PU241','PU242']
cells = [111,121,211,221,311,321,411,421,511,521]

u235_start = 4e6*(238.05/(238.05+31.998))*0.035/1e3     # kg
u238_start = 4e6*(238.05/(238.05+31.998))*(1-0.035)/1e3 # kg
n_fa = [0,8,4,4,4,1]

for directory in directories:
    
    file_list = glob.glob(os.path.join(directory, '*.mcode.out'))
    print(file_list)

    for file_name in file_list:
        
        u25,u28,pu49,putot = 11,11,11,11

        with open(file_name, 'r') as file:
            print(f"Reading {file_name}\n")

            
            df = pd.DataFrame(np.zeros((len(bu_list), len(cols))),index=bu_list,columns=cols)
            df.loc[0,'U235'], df.loc[0,'U238'] = u235_start, u238_start
            tb1, tb3, tb6a, tb6b = False, False, False, False

            for line in file:
                line = line.rstrip('\n')

                if "* TABLE 1. REACTIVITY vs TIME/BURNUP *" in line:
                    tb1 = True
                    time, burnup, keff, stddev, rho = [], [], [], [], []
                elif tb1 and len(line.split())==7 and line.lstrip()[0].isdigit():
                    e = line.split()
                    time.append(e[1]), burnup.append(e[3]), keff.append(e[4]), stddev.append(e[5]), rho.append(e[6])
                    # print(keff, stddev, rho)

                if "* TABLE 3. BURNUP/POWER MAP *" in line:
                    tb1, tb3 = False, True
                    df['EFPD'], df['Burnup'], df['k-eff'], df['std-dev'], df['rho'] = time, burnup, keff, stddev, rho

                elif tb3:
                    if line.startswith("Pf(111)"):
                        pf_11 = [float(value)*100 for value in line.split()[1:]]
                        # df['Pf11%'] = pf_11
                    elif line.startswith("Pf(121)"):
                        n_fa1 = n_fa[1]
                        pf_12 = [float(value)*100 for value in line.split()[1:]]
                        # df['Pf12%'] = pf_12
                        pf_1tot = [(a + b) for a, b in zip(pf_11, pf_12)]
                        # df['Pf1tot%'] = pf_1tot
                        df['Pf11/FA%'], df['Pf12/FA%'] = [c/n_fa1 for c in pf_11], [c/n_fa1 for c in pf_12]
                        df['Pf1tot/FA%'] = [c/n_fa1 for c in pf_1tot]

                    elif line.startswith("Pf(211)") or line.startswith("Pf(311)") or line.startswith("Pf(411)"):
                        pf_21 = [float(value)*100 for value in line.split()[1:]]

                    elif line.startswith("Pf(221)") or line.startswith("Pf(321)") or line.startswith("Pf(421)"):
                        pf_22 = [float(value)*100 for value in line.split()[1:]]
                        pf_2tot = [(a + b) for a, b in zip(pf_21, pf_22)]

                        if line.startswith("Pf(221)"):
                            n_fa2 = n_fa[2]
                            # df['Pf21%'], df['Pf22%'], df['Pf2tot%'] = pf_21, pf_22, pf_2tot
                            df['Pf21/FA%'], df['Pf22/FA%'] = [c/n_fa2 for c in pf_21], [c/n_fa2 for c in pf_22] 
                            df['Pf2tot/FA%'] = [c/n_fa2 for c in pf_2tot]
                        elif line.startswith("Pf(321)"):
                            n_fa3 = n_fa[3]
                            # df['Pf31%'], df['Pf32%'], df['Pf3tot%'] = pf_21, pf_22, pf_2tot
                            df['Pf31/FA%'], df['Pf32/FA%'] = [c/n_fa2 for c in pf_21], [c/n_fa2 for c in pf_22] 
                            df['Pf3tot/FA%'] = [c/n_fa3 for c in pf_2tot]
                        elif line.startswith("Pf(421)"):
                            n_fa4 = n_fa[4]
                            # df['Pf41%'], df['Pf42%'], df['Pf4tot%'] = pf_21, pf_22, pf_2tot
                            df['Pf41/FA%'], df['Pf42/FA%'] = [c/n_fa2 for c in pf_21], [c/n_fa2 for c in pf_22] 
                            df['Pf4tot/FA%'] = [c/n_fa4 for c in pf_2tot]

                    elif line.startswith("Pf(511)"):
                        pf_51 = [float(value)*100 for value in line.split()[1:]]
                        # df['Pf51%'] = pf_51
                        df['Pf51/FA%'] = [c for c in pf_51]
                    elif line.startswith("Pf(521)"):
                        pf_52 = [float(value)*100 for value in line.split()[1:]]
                        # df['Pf52%'] = pf_52
                        df['Pf52/FA%'] = [c for c in pf_52] 
                        pf_5tot = [(a + b) for a, b in zip(pf_51, pf_52)]
                        # df['Pf5tot%'] = pf_5tot
                        df['Pf5tot/FA%'] = [c for c in pf_5tot]

                if "* TABLE 6. COMPOSITION TABLE (GRAMS) *" in line:
                    tb3, tb6a = False, True

                elif tb6a:
                    e = line.split()
                    flag = False
                    for i in isotope_list:
                        if len(e) > 10 and e[1] == i:
                            # print(line)
                            for f in [1,2,3,4,5]:
                                for s in [1,2]:
                                    col = f'{i}_{f}{s}'
                                    if (df[col] == 0).all():
                                        # print(line)
                                        d = [0, float(e[3]), float(e[5]), float(e[7]), float(e[9]), float(e[11]),] #float(e[13]),] # float(e[13]), 0]
                                        d = [x/1e3/n_fa[f] for x in d]
                                        # print(i,f,s,d,'\n')
                                        df[col] = d
                                        flag = True
                                        break
                                if flag:
                                    break
                                    # break
                            # break
                    # break

                if "* TABLE 6. COMPOSITION TABLE (GRAMS) (CONT)" in line:
                    tb6a, tb6b = False, True

                elif tb6b:
                    e = line.split()
                    flag = False
                    for i in isotope_list:
                        if len(e) > 2 and e[1] == i: 
                            for f in [1,2,3,4,5]:
                                for s in [1,2]:
                                    col = f'{i}_{f}{s}'
                                    if df[col].iloc[-1] == 0:
                                        df.loc[bu_list[-1],col] = float(e[3])/1e3/n_fa[f]
                                        flag = True
                                        break
                                if flag:
                                    break

                if "* TABLE 7. NEUTRON ABSORPTION RATE TABLE (neutrons/sec) *" in line:
                    tb6a, tb6b = False, False
        

        # Subtotal each isotope per FA = sum seed + blanket
        for b in bu_list:
            for i in isotope_list:
                for f in [1,2,3,4,5]:
                    df.loc[b,f'{i}_{f}tot'] = (df.loc[b,f'{i}_{f}1'] + df.loc[b,f'{i}_{f}2'])
                    # print(b, i, f, df.loc[b,f'{i}_{f}1'] + df.loc[b,f'{i}_{f}2'])

        # Total each isotope in core = Sum of subtotals of isotope in each FA
        for b in bu_list:
            for i in isotope_list:
                df.loc[b, i] = sum(df.loc[b, f'{i}_{f}tot']*n_fa[f] for f in [1,2,3,4,5])
                # df.loc[b,i] = df.loc[b,f'{i}_1tot'] + df.loc[b,f'{i}_2tot'] + df.loc[b,f'{i}_3tot'] + df.loc[b,f'{i}_4tot'] + df.loc[b,f'{i}_5tot']

        # Subtotal total Pu in each of 10 bu zones [11,12,21,22,31,32,41,42,51,52]
        for b in bu_list:
            for f in [1,2,3,4,5]:
                for s in [1,2]:
                    df.loc[b, f'PU_{f}{s}tot'] = sum(df.loc[b, f'{i}_{f}{s}'] for i in ['PU239', 'PU240', 'PU241', 'PU242'])

        # Subtotal Pu in each FA
        for b in bu_list:
            for f in [1,2,3,4,5]:
                df.loc[b, f'PU_{f}tot'] = sum(df.loc[b, f'{i}_{f}tot'] for i in ['PU239', 'PU240', 'PU241', 'PU242'])

        # Subtotal Pu % in each bu zone
        for b in bu_list:
            for f in [1,2,3,4,5]:
                for s in [1,2]:
                    if df.loc[b, f'PU_{f}{s}tot'] == 0:
                        df.loc[b, f'PU_{f}{s}qual'] = 0
                    else:
                        df.loc[b, f'PU_{f}{s}qual'] = df.loc[b, f'PU239_{f}{s}']/df.loc[b, f'PU_{f}{s}tot']*100


        # Subtotal Pu % in each FA
        for b in bu_list:
            for f in [1,2,3,4,5]:
                if df.loc[b, f'PU_{f}tot'] == 0:
                    df.loc[b, f'PU_{f}qual'] = 0
                else:
                    df.loc[b, f'PU_{f}qual'] = df.loc[b, f'PU239_{f}tot']/df.loc[b, f'PU_{f}tot']*100

        for b in bu_list:
            df.loc[b, f'PUtot'] = sum(df.loc[b, i] for i in ['PU239', 'PU240', 'PU241', 'PU242'])
            if df.loc[b, f'PUtot'] == 0:
                df.loc[b, f'PUqual'] = 0
            else:
                df.loc[b, f'PUqual'] = df.loc[b, f'PU239']/df.loc[b, f'PUtot']*100

        print(df)

        df.to_csv(f"./{file_name.split('.')[-3]}.csv", index=False)
        print(f"Wrote {file_name.split('.')[-3]}.csv")
