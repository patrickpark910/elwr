import os, glob
import pandas as pd
import numpy as np

directories = [
#    './B-fa25-cladSS-clean',
#    './B-fa25-cladZr-clean',
#    './A-cladSS-clean', 
#    './A-cladSS-Li0_1mg', 
#    './A-cladSS-Li01mg',
#    './A-cladSS-Li05mg',
#    './A-cladSS-Li10mg',
#    './A-cladSS-Li15mg',
#    './A-cladZr-clean', 
#    './A-cladZr-Li0_1mg', 
#    './A-cladZr-Li01mg',
#    './A-cladZr-Li05mg',
#    './A-cladZr-Li10mg',
#    './A-cladZr-Li15mg',
#    './A-cladSS-clean',
    './A-cladZr-Li35mg',
    ]


for directory in directories:
    
    file_list = glob.glob(os.path.join(directory, '*.mcode.out'))

    for file_name in file_list:
        with open(file_name, 'r') as file:
            isotope_list = ["U235","U238","PU239","PU240","PU241","PU242"]
            df = pd.DataFrame(columns=isotope_list)
            tb6a, tb6b = False, False

            # Read the file line by line
            for line in file:
                # Check if the line contains "TABLE 6."
                
                if "* TABLE 6. COMPOSITION TABLE (GRAMS) *" in line:
                    tb6a = True

                elif tb6a:
                    e = line.split()
                    for i in isotope_list:
                        if len(e) > 2 and e[1] == i: # and e[1] == i:
                            c = []
                            c.extend([e[3],e[5],e[7],e[9],e[11],e[13]])
                            df[i] = c

                if "* TABLE 6. COMPOSITION TABLE (GRAMS) (CONT)" in line:
                    tb6a, tb6b = False, True
                    df.loc[len(df)] = [np.nan] * df.shape[1]
                    print("new line")

                elif tb6b:
                    e = line.split()
                    for i in isotope_list:
                        if len(e) > 2 and e[1] == i: # and e[1] == i:
                            df.loc[6,i] = e[3]

                if "* TABLE 7. NEUTRON ABSORPTION RATE TABLE (neutrons/sec) *" in line:
                    tb6a, tb6b = False, False
        print(file_name)
        df.to_csv(f"./{file_name.split('.')[-3]}.csv", index=False)
        print(f"Wrote {file_name.split('.')[-3]}.csv")
