import pandas as pd
import os
import numpy as np
import json

def generate(df,cols, parent_level, cols_to_select):
    base_dictt = dict()
    spends_dictt = dict()
    
    if cols_to_select:
        df = df.iloc[-cols_to_select:]

    for col in df.columns:
        base_dictt[col] = list(df[col])
        spends_dictt[col] = sum(base_dictt[col])


    spend_threshold_dict = dict()
    
    for key, target_sum in spends_dictt.items():
        # print(key, target_sum)
        split_list = key.split("|")
        strr1  = '|'.join(split_list[:parent_level*2+1])
        req_cols = []
        for ele, summ in spends_dictt.items():
            ele_split = ele.split("|")
            strr2 = '|'.join(ele_split[:parent_level*2+1])
            if strr1 == strr2:
                req_cols.append(ele)

        target_sum = 0
        for col in req_cols:
            target_sum = target_sum + spends_dictt[col]

        if target_sum != 0:
            spend_threshold_dict[key] = (spends_dictt[key]/target_sum)*100
        else:
            spend_threshold_dict[key] = 0

    max_dict = dict()
    nz_count_dict = dict()
    threshold_dict = dict()
    for key, ele_list in base_dictt.items():
        max_dict[key] = 0
        len = 0
        non_zero_count = 0
        for ele in ele_list:
            if ele != 0 :
                len = len+1
                non_zero_count = non_zero_count +1
                if len > max_dict[key]:
                    max_dict[key] = len
            else:
                len = 0

        nz_count_dict[key] = non_zero_count
        if non_zero_count != 0:

            threshold_dict[key] = (max_dict[key]/non_zero_count)*100
        else:

            threshold_dict[key] = 0

    return spends_dictt, spend_threshold_dict, threshold_dict



def create_daily_data(df, date,target_col,granurality_level, parent_level):

    filtered_df=pd.DataFrame({"Merged":list(df.columns[1:])})
    filtered_df["Merged"] = filtered_df["Merged"].astype(str)
    filtered_df["Merged"] = filtered_df["Merged"].str.replace('|', '', n=1)
    # Find max splits
    max_splits = filtered_df["Merged"].str.count(r'\|').max() + 1
    filtered_df_split = filtered_df["Merged"].str.split('|', n=max_splits-1, expand=True)
    filtered_df_split.columns = granurality_level[:filtered_df_split.shape[1]]
    filtered_df = pd.concat([filtered_df, filtered_df_split], axis=1)
    filtered_df.drop("Merged", axis=1)
    
    df_t=df.set_index(date).T
 
    filtered_df['year_mu*0.15']=0.15*np.array(df_t.T[-365:].T.mean(axis=1))
    filtered_df['overall_mu*0.15'] = 0.15*np.array(df_t.mean(axis=1))
    filtered_df['%Overall Active']=(np.array(df_t)>np.array(filtered_df[['overall_mu*0.15']])).mean(axis=1) * 100
    filtered_df['%Year Active']=(np.array(df_t.T[-365:].T)>np.array(filtered_df[['year_mu*0.15']])).mean(axis=1) * 100
    filtered_df['%Overall NonZero']=(np.array(df_t)>0).mean(axis=1) * 100
    filtered_df['%Year NonZero']=(np.array(df_t.T[-365:].T)>0).mean(axis=1) * 100
    filtered_df.drop(['year_mu*0.15','overall_mu*0.15'],axis=1,inplace=True)
    

    
    cols_to_select = 365
    y_spends_dictt,y_spend_threshold_dict, y_threshold_dict = generate(df.drop(date, axis=1),granurality_level, parent_level, cols_to_select) 

    cols_to_select = False
    spends_dictt,spend_threshold_dict, threshold_dict = generate(df.drop(date, axis=1),granurality_level, parent_level, cols_to_select) 

    report_df = pd.DataFrame({'Key' : spend_threshold_dict.keys(),
                                f"Overall {target_col}":spends_dictt.values(),
                                f"Year {target_col}":y_spends_dictt.values(),
                                "%Overall Cont" : threshold_dict.values(),
                                "%Year Cont" : y_threshold_dict.values(),
                                f"%Overall {target_col}" : spend_threshold_dict.values(),
                                f"%Year {target_col}" : y_spend_threshold_dict.values(),
                                })
    filtered_df[[f"Overall {target_col}",f"Year {target_col}","%Overall Cont", "%Year Cont",f"%Overall {target_col}",f"%Year {target_col}"]] = report_df[[f"Overall {target_col}",f"Year {target_col}","%Overall Cont", "%Year Cont",f"%Overall {target_col}",f"%Year {target_col}"]]
    return filtered_df


def create_weekly_data(df, date, target_col, granurality_level, parent_level):
    filtered_df=pd.DataFrame({"Merged":list(df.columns[1:])})
    filtered_df["Merged"] = filtered_df["Merged"].astype(str)
    filtered_df["Merged"] = filtered_df["Merged"].str.replace('|', '', n=1)
    # Find max splits
    max_splits = filtered_df["Merged"].str.count(r'\|').max() + 1
    filtered_df_split = filtered_df["Merged"].str.split('|', n=max_splits-1, expand=True)
    filtered_df_split.columns = granurality_level[:filtered_df_split.shape[1]]
    filtered_df = pd.concat([filtered_df, filtered_df_split], axis=1)
    filtered_df.drop("Merged", axis=1)
    
    df_w=df.copy()
    df_w[date] = pd.to_datetime(df_w[date])
    df_w['week'] = df_w[date].dt.isocalendar().week
    df_w['year'] = df_w[date].dt.year
    df_w["year_week"] = df_w['year'].astype(str) +"-"+ df_w['week'].astype(str).str.zfill(2)
    df_weekly = df_w.groupby("year_week", as_index=False).sum(numeric_only=True)

    df_weekly=df_weekly.drop([ "year", 'week'], axis=1)
   
    
    df_t = df_weekly.set_index('year_week').T
    filtered_df['year_mu*0.15'] = 0.15*np.array(df_t.T[-52:].T.mean(axis=1))
    filtered_df['overall_mu*0.15'] = 0.15*np.array(df_t.mean(axis=1))
    filtered_df['%Weekly Overall Active']=(np.array(df_t)>np.array(filtered_df[['overall_mu*0.15']])).mean(axis=1) * 100

    filtered_df['%Weekly Year Active']=(np.array(df_t).T[-52:].T>np.array(filtered_df[['year_mu*0.15']])).mean(axis=1) * 100
    filtered_df.drop(['year_mu*0.15','overall_mu*0.15'],axis=1,inplace=True)

    cols_to_select = 52
    y_spends_dictt,y_spend_threshold_dict, y_threshold_dict = generate(df_weekly.drop('year_week',axis=1), granurality_level, parent_level, cols_to_select)

    cols_to_select = False
    spends_dictt,spend_threshold_dict, threshold_dict = generate(df_weekly.drop(['year_week'],axis=1),granurality_level, parent_level, cols_to_select)
    # generate report dict
    report_df = pd.DataFrame({'Key' : spend_threshold_dict.keys(),
                                f"Weekly Overall {target_col}":spends_dictt.values(),
                                f"Weekly Year {target_col}":y_spends_dictt.values(),
                                "%Weekly Overall Cont" : threshold_dict.values(),
                                f"%Weekly Overall {target_col} channel" : spend_threshold_dict.values(),
                                "%Weekly Year Cont" : y_threshold_dict.values(),
                                f"%Weekly Year {target_col} channel" : y_spend_threshold_dict.values(),
                                })

    filtered_df[[f"Weekly Overall {target_col}",f"Weekly Year {target_col}","%Weekly Overall Cont", "%Weekly Year Cont",f"%Weekly Overall {target_col} channel",f"%Year {target_col} channel"]] = report_df[[f"Weekly Overall {target_col}",f"Weekly Year {target_col}","%Weekly Overall Cont", "%Weekly Year Cont",f"%Weekly Overall {target_col} channel",f"%Weekly Year {target_col} channel"]]

    return filtered_df


def create_pivot_ready_data(spend_daily,imp_daily,imp_weekly):

    pivot_df = imp_daily
    pivot_df["Overall Spend"] = spend_daily["Overall Spend"]
    pivot_df["Overall Spend%"] = (pivot_df["Overall Spend"] / pivot_df["Overall Spend"].sum())
    pivot_df["Year Spend"] = spend_daily["Year Spend"]
    pivot_df["Year Spend%"] = (pivot_df["Year Spend"] / pivot_df["Year Spend"].sum())
    pivot_df["%Overall Spend Channel"] = spend_daily["%Overall Spend"]
    pivot_df["%Year Spend Channel"] = spend_daily["%Year Spend"]

    pivot_df["%Weekly Overall Active"] = imp_weekly["%Weekly Overall Active"]
    pivot_df["%Weekly Year Active"] = imp_weekly["%Weekly Year Active"]
    pivot_df["%Weekly Overall Cont"] = imp_weekly["%Weekly Overall Cont"]
    pivot_df["%Weekly Year Cont"] = imp_weekly["%Weekly Year Cont"]

    return pivot_df
