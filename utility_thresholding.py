
def create_summary(table, merged_columns, granularity,  green_thr, orange_thr, green_active, orange_active):
    temp = {
        'Master Channel':merged_columns+ str(granularity), 
        'Green Threshold': green_thr,
        '% Coverage Spend Green': table['% Spend only Green'].sum(),
        'Orange Threshold': orange_thr,
        '% Coverage Spend Orange': table['% Spend Including Orange'].sum(),
        'Actual Spends Covered': table['Actual Spend Covered - Threshold criteria alone'].sum(),
        '% Active Records Green': green_active,
        'Coverage (% Spend) based on Active records': table['% Spend Green (Active)'].sum(),
        '% Active Records Orange': orange_active,
        'Coverage (% Spend) based on Active records Orange': table['% Spend Orange (Active)'].sum(),
        'Actual Spends Covered in overall criteria': table['Actual Spend Covered Overall'].sum()
    }
    return temp
    

def create_threshold_data(table, green_thr, orange_thr, green_active, orange_active):
    table['Threshold Green'] = (table['%Year Spend Channel'] > green_thr) * 1
    table['Threshold Orange'] = ((table['%Year Spend Channel'] < green_thr)  & (table['%Overall Spend Channel'] > orange_thr)) * 1
    table['threshold'] = ((table['%Year Spend Channel'] > green_thr)  | (table['%Overall Spend Channel'] > orange_thr)) * 1
    table['% Spend only Green'] = table['Overall Spend %'] * table['Threshold Green']
    table['% Spend Including Orange'] = table['Overall Spend %'] * table['threshold']
    table['Actual Spend Covered - Threshold criteria alone'] = table['Overall Spend'] * table['threshold']
    
    table['% Active Week Green'] = (table['%Weekly Year Active'] > green_active) * 1
    table['% Active Week Orange'] = ((table['%Weekly Year Active'] < green_active)  & (table['%Weekly Overall Active'] > orange_active)) * 1
    table['threshold'] = ((table['%Weekly Year Active'] > green_active)  | (table['%Weekly Overall Active'] > orange_active)) * 1
    table['% Spend Green (Active)'] = table['Overall Spend %'] * table['% Active Week Green']
    table['% Spend Orange (Active)'] = table['Overall Spend %'] * table['threshold']
    
    table['Overall Green'] = ((table['Threshold Green']) & (table['% Active Week Green'])) * 1
    table['Overall Orange'] = ((table['Threshold Orange']) & (table['% Active Week Green'])) * 1
    table['Overall thr'] = (table['Overall Green']) | (table['Overall Orange'])
    table['Actual Spend Covered Overall'] = ((table['Overall Green']) | (table['Overall Orange'])) * table['Overall Spend']
    
    return table
    

def create_pivot_table(ndf, pivot_index, pivot_values):

    table = ndf.pivot_table(index=pivot_index, values=pivot_values, aggfunc=lambda x: x.sum())
    table = table.reindex(columns=pivot_values).reset_index()
    
    overall_index = int(table.columns.get_indexer(['Overall Spend%'])[0])
    year_index = int(table.columns.get_indexer(['Year Spend%'])[0])

    table['Overall Spend %'] = (table['Overall Spend%']/table['Overall Spend%'].sum()) * 100
    table['Year Spend %'] = (table['Year Spend%']/table['Year Spend%'].sum()) * 100
    
    overall_spend = table.pop('Overall Spend %')
    year_spend = table.pop('Year Spend %')
    
    table.insert(overall_index, 'Overall Spend %', overall_spend)
    table.insert(year_index, 'Year Spend %', year_spend)
    
    table.drop(columns=['Overall Spend%', 'Year Spend%'], inplace=True)
    
    return table
    