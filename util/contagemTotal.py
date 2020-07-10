# -*- coding: utf-8 -*-
"""
Spyder Editor

Este é um arquivo de script temporário.
"""
def contatemTotal(pathfile):
    import pandas as pd

    df = pd.read_csv(pathfile)

    values = list()

    for i in df.itertuples():
        values.append(i)
    
    cvs_total = dict()
    total = 0
    for i in range(len(values)):
        for j in range(len(values[0])):
            if j >= 3:
                total += values[i][j]
            cvs_total[str(values[i][2])] = total
        total = 0
    #print(cvs_total)
    return cvs_total