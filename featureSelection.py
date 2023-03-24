'''
Author: Mina Rafla (Orange Innovation Lannion) 
'''


from UMODL_SearchAlgorithm import ExecuteGreedySearchAndPostOpt
from helperFunction import preprocessData
import sys
import pandas as pd

def getImportantVariables_UMODL_ForMultiProcessing(data):#contains colName treatmentNameyName
#     treatmentName=arg[3]
#     y_name=arg[2]
#     colName=arg[1]
#     data=arg[0]
    VariableVsImportance={}
#     featureImportance,ValuesDistro=UMODL_SearchAlgorithm.ExecuteGreedySearchAndPostOpt(data[[colName,treatmentName,y_name]],0)
    featureImportanceAndBounds=ExecuteGreedySearchAndPostOpt(data)
#     VariableVsImportance[colName]=featureImportance
#     return VariableVsImportance
    return featureImportanceAndBounds

def getTheBestVar(data,features,treatmentName,outcomeName):
    VarVsImportance={}
    VarVsDisc={}
    for feature in features:
        print("feature is ",feature)
        VarVsImportance[feature],VarVsDisc[feature]=getImportantVariables_UMODL_ForMultiProcessing(data[[feature,treatmentName,outcomeName]])
    VarVsImportance={k: v for k, v in sorted(VarVsImportance.items(), key=lambda item: item[1])}
    return VarVsImportance

def UMODL_FS(df,treatmentName,outcomeName,LogFileName="log"):
    stdoutOrigin=sys.stdout
    sys.stdout = open(LogFileName+".txt", "w")

    cols=list(df.columns)

    cols.remove(treatmentName)
    cols.remove(outcomeName)
    df=df[cols+[treatmentName,outcomeName]]

    features=list(df.columns[:-2])

    df=preprocessData(df,treatmentName,outcomeName)
    ListOfVarsImportance=getTheBestVar(df,features,treatmentName,outcomeName)
#     print(getTheBestVar(df,features))

    sys.stdout.close()
    sys.stdout=stdoutOrigin
    
    return ListOfVarsImportance
    