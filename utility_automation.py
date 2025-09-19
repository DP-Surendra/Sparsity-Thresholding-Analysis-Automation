
import pandas as pd

def filter_df(df, filter_dict):
    """
    filter_df : handles dataframe filtering using passed dict.
    Inputs :
        - df : type pd.DataFrame
        - filter_dict : type dict
    Returns :
        - df : filtered dataframe using filter_dict
    """

    # Filter df based on key, value pairs.
    # Value will be of type list.
    # filter_dict = {"Column name" : ["Entry 1", "Entry 2", "Entry 3"]}
    for key, value_list in filter_dict.items():
        # print(key)
        if isinstance(value_list, list):
            df = df[df[key].isin(value_list)].copy()
        elif isinstance(value_list, str):
            df = df[df[key].isin([value_list])].copy()

    return df



def generate_filter_dict(df_summary, common_filter, level_summary, target_metric):
    """
    generate_filter_dict : generates filter dict and target dict based on summary dataframe.
    Inputs :
        - df_summary : type pd.DataFrame - summary sheet with defs
        - common_filter : type dict - common filter dictionary for brand filters etc.
        - level_summary : type dict - level information {"L1" : "L1 Definitions"}
        - target_metric : type str - Target metric to choose in summary dataframe
    Returns :
        - target_dict : dict which holds target variable info {"Row 102" : "Impressions"}
        - filter_dict : dict which holds filter info {"Row 102" : {"Master Channel" : "TV",
                                                                    "Platform" : "A-one"} }
    """
    filter_dict = {}
    target_dict_Impression= {}
    target_dict_Cost={}

    # print(common_filter)
    # Filter summary df based on common_filter.
    df_summary = filter_df(df_summary, common_filter)

    # If target metric is empty, fill it with zero.
    df_summary[target_metric[0]] = df_summary[target_metric[0]].fillna(0)
    df_summary[target_metric[1]] = df_summary[target_metric[1]].fillna(0)

    # Convert rows to corresponding filter info.
    for i, dictt in enumerate(df_summary.to_dict("records")):
        filter_dict[f"Row {i}"] = {}
        target_dict_Impression[f"Row {i}"] = dictt[target_metric[0]]
        target_dict_Cost[f"Row {i}"]=dictt[target_metric[1]]

        for col, valuee in level_summary.items():
            # Add key, value pairs only if entry exists and not null.
            if not pd.isnull(dictt[col]) and dictt[col] != "":
                filter_dict[f"Row {i}"][dictt[col]] = [dictt[valuee]]

    return target_dict_Impression, target_dict_Cost,filter_dict



def generate_pivoted_df(df, user_key, date_col, fil_cols, target_Impression, target_Cost, prefix):
    if target_Impression != 0:
        if target_Impression==target_Cost:
            req_cols = [date_col] + fil_cols + [target_Impression]
        else:
            req_cols = [date_col] + fil_cols + [target_Impression]+[target_Cost]
       
        df = df[req_cols].copy()
        df.loc[:, target_Impression] = df[target_Impression].fillna(0)
        df.loc[:, target_Impression] = df[target_Impression].astype("float")
        
        df.loc[:, target_Cost] = df[target_Cost].fillna(0)
        df.loc[:, target_Cost] = df[target_Cost].astype("float")
    

        # df = df.groupby(req_cols).sum().reset_index()
        

        df.loc[:, "Merged"] = df[fil_cols].apply(lambda row: "|".join(f"{col}|{val}" for col, val in row.items()
        if pd.notna(val) and str(val).strip() != "" ), axis=1)
    
        df = df.drop(columns=fil_cols)

        merged_str = list(df["Merged"].unique())[0]
        
        df_imp = df.groupby([date_col, "Merged"])[target_Impression].sum().reset_index()
        df_cost=df.groupby([date_col, "Merged"])[target_Cost].sum().reset_index()
        
        df_impression = df_imp.pivot(index=date_col, columns="Merged", values=target_Impression).reset_index()
        df_cost = df_cost.pivot(index=date_col, columns="Merged", values=target_Cost).reset_index()
    
        merged_str = prefix + "|" + merged_str
        df_impression.columns = [date_col, merged_str]
        df_cost.columns = [date_col, merged_str]
        # print(f"Generated Pivot for {user_key}")

    else:
        print(f"src.helpers.helper.generate_pivoted_df {user_key} target is empty")

    return df_impression, df_cost



def generate_tagged_df(
    df_in, common_filter, filter_dict, target_dict_Impression, target_dict_Cost, date_col, date_format, prefix
):
    """
    generate_tagged_df : generates dict using filtering from common_dict, filter_dict, target_dict
    Inputs :
        - df_in : type pd.DataFrame - raw data data frame
        - common_dict : type dict - common filter dictionary for brand filters etc.
        - filter_dict : type dict - filter dictionary for brand filters etc.
        - target_dict : type dict - dictionary which has target information.
        - date_col : type str - date column name
        - date_format : type str - date format
    Returns :
        - df_dict : type dict - dict which holds filter key and corresponding data frame.
    """
    # try:

    # d-type checks for input variables.
    if not isinstance(common_filter, dict):
        raise Exception("generate_tagged_df : common_dict d-type mismatch")
    if not isinstance(filter_dict, dict):
        raise Exception("generate_tagged_df : filter_dict d-type mismatch")
    if not isinstance(target_dict_Impression, dict):
        raise Exception("generate_tagged_df : target_dict d-type mismatch")
    if not isinstance(target_dict_Cost, dict):
        raise Exception("generate_tagged_df : target_dict d-type mismatch")
    if not isinstance(date_col, str):
        raise Exception("generate_tagged_df : date_col d-type mismatch")
    if not isinstance(date_format, str):
        raise Exception("generate_tagged_df : date_format d-type mismatch")
    if not isinstance(df_in, pd.DataFrame):
        raise Exception("generate_tagged_df : definitionsummary is not a data frame")

    if len(common_filter.keys()) == 0:
        raise Exception("generate_tagged_df : common_dict is empty")
    if len(filter_dict.keys()) == 0:
        raise Exception("generate_tagged_df : filter_dict is empty")
    if len(target_dict_Impression.keys()) == 0:
        raise Exception("generate_tagged_df : target_dict is empty")
    if len(target_dict_Cost.keys()) == 0:
        raise Exception("generate_tagged_df : target_dict is empty")

    if df_in.shape[0] == 0:
        raise Exception("generate_tagged_df : definitionsummary Data Frame is empty")

    df_dict_impression = {}
    df_dict_cost = {}
    
    # Filter df_in with common filter.
    df_in = filter_df(df_in, common_filter)
    for user_key, fil_dict in filter_dict.items():
        # print(fil_dict)
        df_in[date_col] = pd.to_datetime(df_in[date_col], format=date_format)
        df = filter_df(df_in, fil_dict)
        req_cols = [date_col] + list(fil_dict.keys()) + [target_dict_Impression[user_key]]

        if df.shape[0] != 0:
            # print(df, user_key, date_col, list(fil_dict.keys()), target_dict[user_key], prefix)

            df_pivot_impression, df_pivot_cost= generate_pivoted_df(
                df,
                user_key,
                date_col,
                list(fil_dict.keys()),
                target_dict_Impression[user_key],
                target_dict_Cost[user_key],
                prefix,
            )
            df_pivot_impression[date_col] = df_pivot_impression[date_col].astype("datetime64[ns]")
            df_dict_impression[user_key] = df_pivot_impression.fillna(0)
            
            df_pivot_cost[date_col] = df_pivot_cost[date_col].astype("datetime64[ns]")
            df_dict_cost[user_key] = df_pivot_cost.fillna(0)

            # print("Merged :", user_key, df.shape, df_pivot_impression.shape, fil_dict)

    # except Exception as ex:
    #     print("src.helpers.helper.generate_tagged_df :", ex)

    return df_dict_impression, df_dict_cost

def generate_merge_df(tagged_df, date_col, start_date, end_date, date_format):
    df_merge = pd.DataFrame()
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    # df_merge[date_col] = pd.date_range(start_date - pd.Timedelta("7d"), end_date)
    df_merge[date_col] = pd.date_range(start_date, end_date)

    for user_key, df_pivot in tagged_df.items():
        if df_pivot.shape[0] != 0 and df_pivot.shape[1] == 2:
            df_pivot[date_col] = df_pivot[date_col].astype("datetime64[ns]")
            df_merge = df_merge.merge(df_pivot, on=date_col, how="left")

            # print("Merged :", user_key, df_pivot.shape)

        else:
            print("Not Found :", user_key, df_pivot.shape)
            continue

    print(f"Merged df using the dictionary. The final shape is {df_merge.shape}")
    return df_merge