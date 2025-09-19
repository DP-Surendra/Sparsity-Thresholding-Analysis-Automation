import pandas as pd
def color(x):
    if x.iloc[0]:
        return 'Green'
    elif x.iloc[1]:
        return 'Orange'
    else:
        return None
    
    
def Merging_Type(sheet_cpa,sheet_cp, parent_level, orange_thr):
    def Level(i, row,sheet_cpa, sheet_cp, parent_level, orange_thr):
        # for i,row in sheet_cpa.iterrows():
        cl=sheet_cpa['Colour'][i]
        temp = sheet_cpa[sheet_cpa[sheet_cpa.columns[parent_level*2+1]] == row.iloc[parent_level*2+1]]
        if cl:
            # plat_ind.append(row[:(granularity+parent_level)*2])
            return 'Individual'
        else:
            if temp['Overall thr'].sum()>0:
               
                if sheet_cpa[(sheet_cpa[sheet_cpa.columns[parent_level*2+1]] == row.iloc[parent_level*2+1]) & (pd.isnull(sheet_cpa['Colour']))]['Overall Spend %'].sum()>orange_thr:
                    # plat_other.append(row[:(granularity+parent_level)*2])
                    return f'Merged at {sheet_cpa.columns[parent_level*2+1]}'
                else:
                    return f'Merged at {sheet_cpa.columns[parent_level*2-1]}'
            else:
                b=sheet_cp[sheet_cp[sheet_cp.columns[parent_level*2+1]] == row.iloc[parent_level*2+1]]
                if not b.empty:
                    if int(b['Overall thr'].sum())>0:
                    # plat_other.append(row[:(granularity+parent_level)*2])
                        return f'Merged at {sheet_cpa.columns[parent_level*2+1]}'
                    else:
                        return f'Merged at {sheet_cpa.columns[parent_level*2-1]}'
                else:
                    return f'Merged at {sheet_cpa.columns[parent_level*2-1]}'
    for i,row in sheet_cpa.iterrows():
        sheet_cpa.loc[i, 'Merging type'] = Level(i, row,sheet_cpa, sheet_cp, parent_level, orange_thr)
    return sheet_cpa

def Audience_Others(sheet_cpa, parent_level, granularity, len_granularity):
    a=list(sheet_cpa.columns[:len_granularity])
    b=a+['Merging type']
    df=pd.DataFrame(columns=b)
    for idx, row in sheet_cpa.iterrows():
        if row['Merging type'] == 'Individual':
            values = list(row[:2*(parent_level+granularity)])  # Convert to list
            values = values + [None] * (len(df.columns)-1 - len(values))
            df.loc[len(df)] = values+ [row['Merging type']]
        elif row['Merging type'] == f'Merged at {sheet_cpa.columns[parent_level*2+1]}':
            values = list(row[:2*(parent_level+granularity)])
            values = values + [None] * (len(df.columns)-1 - len(values))
            values[2*(parent_level+granularity)-2] = row.iloc[2*(parent_level+granularity)-2]
            values[2*(parent_level+granularity)-1]="Others"
            df.loc[len(df)] = values+[row['Merging type']]
        else:
            values=list(row[:2*parent_level+2])
            values = values + [None] * (len(df.columns)-1 - len(values))
            df.loc[len(df)] = values+[row['Merging type']]
    # df.drop_duplicates(inplace=True)
    return df

def Platform_Others(sheet_cpa, parent_level,granularity, len_granularity):
    df=pd.DataFrame(columns=sheet_cpa.columns)
    for idx, row in sheet_cpa.iterrows():        
        if row['Merging type']=='Individual' or row['Merging type']==f"Merged at {sheet_cpa.columns[parent_level*2+1]}":
            values = list(row[:2*(parent_level+granularity)])  # Convert to list
            values = values + [None] * (len(df.columns)-1 - len(values))
            df.loc[len(df)] = values+ [row['Merging type']]
        else:
            values = list(row[:2*(parent_level)+2])
            values[2*(parent_level)+1]="Others"
            values = values + [None] * (len(df.columns)-1 - len(values))
            df.loc[len(df)] = values+ [row['Merging type']]
    # df.drop_duplicates(inplace=True)
    return df
