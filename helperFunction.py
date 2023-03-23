import sys
import pandas as pd


def preprocessData(df,treatmentName='segment',outcomeName='visit'):
    cols = df.columns
    num_cols = list(df._get_numeric_data().columns)

    num_cols.remove(treatmentName)
    num_cols.remove(outcomeName)
    for num_col in num_cols:
        if len(df[num_col].value_counts())<(df.shape[0]/100):
#             print("categorical columns disguised in a numerical column")
            num_cols.remove(num_col)
        else:
            df[num_col] = df[num_col].fillna(df[num_col].mean())

    categoricalCols=list(set(cols) - set(num_cols))
    if treatmentName in categoricalCols:
        categoricalCols.remove(treatmentName)
    if outcomeName in categoricalCols:
        categoricalCols.remove(outcomeName)
#     print("Categorical variables are  ",categoricalCols)
    for catCol in categoricalCols:
#         print("Encoding ",catCol)
        df[catCol] = df[catCol].fillna(df[catCol].mode()[0])
        DictValVsUplift={}
        for val in df[catCol].value_counts().index:
            dataset_slice=df[df[catCol]==val]
            t0j0=dataset_slice[(dataset_slice[treatmentName]==0)&(dataset_slice[outcomeName]==0)].shape[0]
            t0j1=dataset_slice[(dataset_slice[treatmentName]==0)&(dataset_slice[outcomeName]==1)].shape[0]
            t1j0=dataset_slice[(dataset_slice[treatmentName]==1)&(dataset_slice[outcomeName]==0)].shape[0]
            t1j1=dataset_slice[(dataset_slice[treatmentName]==1)&(dataset_slice[outcomeName]==1)].shape[0]

            if (t1j1+t1j0)==0:
                UpliftInThisSlice=-1
            elif (t0j1+t0j1)==0:
                 UpliftInThisSlice=0
            else:
                UpliftInThisSlice=(t1j1/(t1j1+t1j0))-(t0j1/(t0j1+t0j1))
            DictValVsUplift[val]=UpliftInThisSlice
        # print("DictValVsUplift")
        # print(DictValVsUplift)
        OrderedDict={k: v for k, v in sorted(DictValVsUplift.items(), key=lambda item: item[1])}
        encoded_i=0
        for k,v in OrderedDict.items():
            df[catCol] = df[catCol].replace([k],encoded_i)
            encoded_i+=1
#     print("df after encoding categorical variables is ",df)
    df[treatmentName]=df[treatmentName].astype(str)
    return df
