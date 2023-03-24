'''
Author: Mina Rafla (Orange Innovation Lannion) 
'''


import pandas as pd
from UMODL_SearchAlgorithm import ExecuteGreedySearchAndPostOpt
from helperFunction import preprocessData



def EncodeDataset(df,treatmentName,outcomeName,DesiredOutput='EncodedDataset'):
    cols=list(df.columns)

    cols.remove(treatmentName)
    cols.remove(outcomeName)
    df=df[cols+[treatmentName,outcomeName]]
    
    if DesiredOutput=="EncodedDataset":
        df=preprocessData(df,treatmentName,outcomeName)
    
    VarVsImportance={}
    VarVsDisc={}

    for col in cols:
#         print("feature is ",col)
        VarVsImportance[col],VarVsDisc[col]=ExecuteGreedySearchAndPostOpt(df[[col,treatmentName,outcomeName]])
    
    if DesiredOutput=="Bounds":
        return VarVsDisc
    
    for col in cols:
        if len(VarVsDisc[col]) == 1:
            df.drop(col,inplace=True,axis=1)
            df.drop(col,inplace=True,axis=1)
        else:
            if df[col].max()>VarVsDisc[col][-1]:
                print("SOMETHING STRANGS IS HAPPENING max in train")
            df[col] = pd.cut(df[col], bins=[df[col].min()-0.001]+VarVsDisc[col])

            df[col] = df[col].astype('category')
            df[col] = df[col].cat.codes
    return df