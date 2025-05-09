import pandas as pd
import openpyxl
import random

def update_buffer():
    # Pull data from the excel spreadsheet
    buffer_df = pd.read_excel('datasheet.xlsx', sheet_name='buffer', engine='openpyxl')

    row_boundary = buffer_df.index[buffer_df.iloc[:, 0] == 'TARIFFS'].tolist()[0]
    column_boundary = list(buffer_df.loc[[row_boundary]].to_numpy()[0]).index("EXPORTS")

    # Stats
    resource_df = buffer_df.iloc[:row_boundary - 1, :column_boundary]

    # Tariffs
    tar_df_full = buffer_df.iloc[row_boundary + 2:, :column_boundary]
    tar_df = buffer_df.iloc[row_boundary + 2:, :column_boundary]

    # Products
    prod_df_full = buffer_df.iloc[row_boundary + 2:, column_boundary:]
    prod_df = buffer_df.iloc[row_boundary + 2:, column_boundary:]

    prod_df.columns = tar_df.columns
    prod_df.iloc[:, 0] = tar_df.iloc[:, 0].values

    tar_df = tar_df.reset_index(drop=True)
    prod_df = prod_df.reset_index(drop=True)

    #print(prod_df)
    #print(tar_df)
    #print(resource_df)

    countries = list(tar_df.columns[1:])

    # Extract matrice data

    rsrc_ext_hc_loc = tar_df.index[tar_df.iloc[:, 0] == 'Resource Extraction (High Carbon)'].tolist()[0]
    rsrc_ext_lc_loc = tar_df.index[tar_df.iloc[:, 0] == 'Resource Extraction (Low Carbon)'].tolist()[0]

    indust_hc_loc = tar_df.index[tar_df.iloc[:, 0] == 'Industrial (High Carbon)'].tolist()[0]
    indust_lc_loc = tar_df.index[tar_df.iloc[:, 0] == 'Industrial (Low Carbon)'].tolist()[0]

    cons_g_hc_loc = tar_df.index[tar_df.iloc[:, 0] == 'Consumer Goods (High Carbon)'].tolist()[0]
    cons_g_lc_loc = tar_df.index[tar_df.iloc[:, 0] == 'Consumer Goods (Low Carbon)'].tolist()[0]

    agric_hc_loc = tar_df.index[tar_df.iloc[:, 0] == 'Agriculture (High Carbon)'].tolist()[0]
    agric_lc_loc = tar_df.index[tar_df.iloc[:, 0] == 'Agriculture (Low Carbon)'].tolist()[0]

    energy_hc_loc = tar_df.index[tar_df.iloc[:, 0] == 'Energy (High Carbon)'].tolist()[0]
    energy_lc_loc = tar_df.index[tar_df.iloc[:, 0] == 'Energy (Low Carbon)'].tolist()[0]

    t_rsrc_ext_hc_df = tar_df.iloc[1:rsrc_ext_lc_loc - 1, 1:]
    t_rsrc_ext_lc_df = tar_df.iloc[1 + rsrc_ext_lc_loc:indust_hc_loc - 1, 1:]

    t_indust_hc_df = tar_df.iloc[1 + indust_hc_loc:indust_lc_loc - 1, 1:]
    t_indust_lc_df = tar_df.iloc[1 + indust_lc_loc:cons_g_hc_loc - 1, 1:]

    t_cons_g_hc_df = tar_df.iloc[1 + cons_g_hc_loc:cons_g_lc_loc - 1, 1:]
    t_cons_g_lc_df = tar_df.iloc[1 + cons_g_lc_loc:agric_hc_loc - 1, 1:]

    t_agric_hc_df = tar_df.iloc[1 + agric_hc_loc:agric_lc_loc - 1, 1:]
    t_agric_lc_df = tar_df.iloc[1 + agric_lc_loc:energy_hc_loc - 1, 1:]

    t_energy_hc_df = tar_df.iloc[1 + energy_hc_loc:energy_lc_loc - 1, 1:]
    t_energy_lc_df = tar_df.iloc[1 + energy_lc_loc:, 1:]

    p_rsrc_ext_hc_df = prod_df.iloc[1:rsrc_ext_lc_loc - 1, 1:]
    p_rsrc_ext_lc_df = prod_df.iloc[1 + rsrc_ext_lc_loc:indust_hc_loc - 1, 1:]

    p_indust_hc_df = prod_df.iloc[1 + indust_hc_loc:indust_lc_loc - 1, 1:]
    p_indust_lc_df = prod_df.iloc[1 + indust_lc_loc:cons_g_hc_loc - 1, 1:]

    p_cons_g_hc_df = prod_df.iloc[1 + cons_g_hc_loc:cons_g_lc_loc - 1, 1:]
    p_cons_g_lc_df = prod_df.iloc[1 + cons_g_lc_loc:agric_hc_loc - 1, 1:]

    p_agric_hc_df = prod_df.iloc[1 + agric_hc_loc:agric_lc_loc - 1, 1:]
    p_agric_lc_df = prod_df.iloc[1 + agric_lc_loc:energy_hc_loc - 1, 1:]

    p_energy_hc_df = prod_df.iloc[1 + energy_hc_loc:energy_lc_loc - 1, 1:]
    p_energy_lc_df = prod_df.iloc[1 + energy_lc_loc:, 1:]

    # Update production using tariffs
    for i, country in enumerate(countries): # rows
        for j in range(len(countries)):  # columns
            old_p_rsrc_ext_hc = p_rsrc_ext_hc_df.iloc[i, j]
            p_rsrc_ext_hc_df.iloc[i, j] *= (1 - t_rsrc_ext_hc_df.iloc[i, j] / 100 * 0.25)

            old_p_rsrc_ext_lc = p_rsrc_ext_lc_df.iloc[i, j]
            p_rsrc_ext_lc_df.iloc[i, j] *= (1 - t_rsrc_ext_lc_df.iloc[i, j] / 100 * 0.25)

            old_p_indust_hc = p_indust_hc_df.iloc[i, j]
            p_indust_hc_df.iloc[i, j] *= (1 - t_indust_hc_df.iloc[i, j] / 100 * 0.25)

            old_p_indust_lc = p_indust_lc_df.iloc[i, j]
            p_indust_lc_df.iloc[i, j] *= (1 - t_indust_lc_df.iloc[i, j] / 100 * 0.25)

            old_p_cons_g_hc = p_cons_g_hc_df.iloc[i, j]
            p_cons_g_hc_df.iloc[i, j] *= (1 - t_cons_g_hc_df.iloc[i, j] / 100 * 0.25)

            old_p_cons_g_lc = p_cons_g_lc_df.iloc[i, j]
            p_cons_g_lc_df.iloc[i, j] *= (1 - t_cons_g_lc_df.iloc[i, j] / 100 * 0.25)

            old_p_agric_hc = p_agric_hc_df.iloc[i, j]
            p_agric_hc_df.iloc[i, j] *= (1 - t_agric_hc_df.iloc[i, j] / 100 * 0.25)

            old_p_agric_lc = p_agric_lc_df.iloc[i, j]
            p_agric_lc_df.iloc[i, j] *= (1 - t_agric_lc_df.iloc[i, j] / 100* 0.25)

            old_p_energy_hc = p_energy_hc_df.iloc[i, j]
            p_energy_hc_df.iloc[i, j] *= (1 - t_energy_hc_df.iloc[i, j] / 100 * 0.25)

            old_p_energy_lc = p_energy_lc_df.iloc[i, j]
            p_energy_lc_df.iloc[i, j] *= (1 - t_energy_lc_df.iloc[i, j] / 100 * 0.25)

            if(i != j): # Increasing domestic production if tariffs are enacted
                p_rsrc_ext_hc_df.iloc[i, i] += 0.25 * (old_p_rsrc_ext_hc - p_rsrc_ext_hc_df.iloc[i, j])
                p_rsrc_ext_lc_df.iloc[i, i] += 0.25 * (old_p_rsrc_ext_lc - p_rsrc_ext_lc_df.iloc[i, j])
                p_indust_hc_df.iloc[i, i] += 0.25 * (old_p_indust_hc - p_indust_hc_df.iloc[i, j])
                p_indust_lc_df.iloc[i, i] += 0.25 * (old_p_indust_lc - p_indust_lc_df.iloc[i, j])
                p_cons_g_hc_df.iloc[i, i] += 0.25 * (old_p_cons_g_hc - p_cons_g_hc_df.iloc[i, j])
                p_cons_g_lc_df.iloc[i, i] += 0.25 * (old_p_cons_g_lc - p_cons_g_lc_df.iloc[i, j])
                p_agric_hc_df.iloc[i, i] += 0.25 * (old_p_agric_hc - p_agric_hc_df.iloc[i, j])
                p_agric_lc_df.iloc[i, i] += 0.25 * (old_p_agric_lc - p_agric_lc_df.iloc[i, j])
                p_energy_hc_df.iloc[i, i] += 0.25 * (old_p_energy_hc - p_energy_hc_df.iloc[i, j])
                p_energy_lc_df.iloc[i, i] += 0.25 * (old_p_energy_lc - p_energy_lc_df.iloc[i, j])

    # Find max values in order to scale gdp growth
    rs_max = max([p_rsrc_ext_hc_df.values.max(), p_rsrc_ext_lc_df.values.max()])
    ind_max = max([p_indust_hc_df.values.max(), p_indust_lc_df.values.max()])
    cons_max = max([p_cons_g_hc_df.values.max(), p_cons_g_lc_df.values.max()])
    agric_max = max([p_agric_hc_df.values.max(), p_agric_lc_df.values.max()])
    energy_max = max([p_energy_hc_df.values.max(), p_energy_lc_df.values.max()])

    # Change if needed
    start_rate_neg = -0.02
    start_rate_pos = 0.01
    end_rate = 0.05

    ''' Makes sure that it doesn't return a 0
    '''
    def uniform_exclude_zero(low, high):
        val = 0
        while val == 0:
            val = random.uniform(low, high)
        return val

    # Increase each factor randomly to simulate natural growth
    for i, country in enumerate(countries): # rows
        for j in range(len(countries)):
            if (rs_max > p_rsrc_ext_hc_df.iloc[i, j]):
                p_rsrc_ext_hc_df.iloc[i, j] *= 1 + random.uniform(start_rate_pos, end_rate)
            if (rs_max > p_rsrc_ext_lc_df.iloc[i, j]):
                p_rsrc_ext_lc_df.iloc[i, j] *= 1 + random.uniform(start_rate_pos, end_rate)
                
            if (ind_max > p_indust_hc_df.iloc[i, j]):
                p_indust_hc_df.iloc[i, j] *= 1 + random.uniform(start_rate_pos, end_rate)
            if (ind_max > p_indust_lc_df.iloc[i, j]):
                p_indust_lc_df.iloc[i, j] *= 1 + random.uniform(start_rate_pos, end_rate)

            if (cons_max > p_cons_g_hc_df.iloc[i, j]):
                p_cons_g_hc_df.iloc[i, j] *= 1 + random.uniform(start_rate_pos, end_rate)
            if (cons_max > p_cons_g_lc_df.iloc[i, j]):
                p_cons_g_lc_df.iloc[i, j] *= 1 + random.uniform(start_rate_pos, end_rate)
                
            if (agric_max > p_agric_hc_df.iloc[i, j]):
                p_agric_hc_df.iloc[i, j] *= 1 + random.uniform(start_rate_pos, end_rate)
            if (agric_max > p_agric_lc_df.iloc[i, j]):
                p_agric_lc_df.iloc[i, j] *= 1 + random.uniform(start_rate_pos, end_rate)

            if (energy_max > p_energy_hc_df.iloc[i, j]):
                p_energy_hc_df.iloc[i, j] *= 1 + random.uniform(start_rate_pos, end_rate)
            if (energy_max > p_energy_lc_df.iloc[i, j]):
                p_energy_lc_df.iloc[i, j] *= 1 + random.uniform(start_rate_pos, end_rate)

            v = uniform_exclude_zero(start_rate_neg, end_rate)
            p_rsrc_ext_hc_df.iloc[i, j] *= 1 + v
            v = uniform_exclude_zero(start_rate_neg, end_rate)
            p_rsrc_ext_lc_df.iloc[i, j] *= 1 + v

            v = uniform_exclude_zero(start_rate_neg, end_rate)
            p_indust_hc_df.iloc[i, j] *= 1 + v
            v = uniform_exclude_zero(start_rate_neg, end_rate)
            p_indust_lc_df.iloc[i, j] *= 1 + v

            v = uniform_exclude_zero(start_rate_neg, end_rate)
            p_cons_g_hc_df.iloc[i, j] *= 1 + v
            v = uniform_exclude_zero(start_rate_neg, end_rate)
            p_cons_g_lc_df.iloc[i, j] *= 1 + v

            v = uniform_exclude_zero(start_rate_neg, end_rate)
            p_agric_hc_df.iloc[i, j] *= 1 + v
            v = uniform_exclude_zero(start_rate_neg, end_rate)
            p_agric_lc_df.iloc[i, j] *= 1 + v

            v = uniform_exclude_zero(start_rate_neg, end_rate)
            p_energy_hc_df.iloc[i, j] *= 1 + v
            v = uniform_exclude_zero(start_rate_neg, end_rate)
            p_energy_lc_df.iloc[i, j] *= 1 + v

    # Emisisons rates
    for i, country in enumerate(countries): # rows
        new_gdp = 0
        emissions = 0
        for j in range(len(countries)):
            if(i == j):
                new_gdp += p_rsrc_ext_hc_df.iloc[i, j] - p_rsrc_ext_hc_df.iloc[i].sum() + p_rsrc_ext_hc_df.iloc[:, j].sum()
                new_gdp += p_rsrc_ext_lc_df.iloc[i, j] - p_rsrc_ext_lc_df.iloc[i].sum() + p_rsrc_ext_hc_df.iloc[:, j].sum()
                new_gdp += p_indust_hc_df.iloc[i, j] - p_indust_hc_df.iloc[i].sum() + p_rsrc_ext_hc_df.iloc[:, j].sum()
                new_gdp += p_indust_lc_df.iloc[i, j] - p_indust_lc_df.iloc[i].sum() + p_rsrc_ext_hc_df.iloc[:, j].sum()
                new_gdp += p_cons_g_hc_df.iloc[i, j] - p_cons_g_hc_df.iloc[i].sum() + p_rsrc_ext_hc_df.iloc[:, j].sum()
                new_gdp += p_cons_g_lc_df.iloc[i, j] - p_cons_g_lc_df.iloc[i].sum() + p_rsrc_ext_hc_df.iloc[:, j].sum()
                new_gdp += p_agric_hc_df.iloc[i, j] - p_agric_hc_df.iloc[i].sum() + p_rsrc_ext_hc_df.iloc[:, j].sum()
                new_gdp += p_agric_lc_df.iloc[i, j] - p_agric_lc_df.iloc[i].sum() + p_rsrc_ext_hc_df.iloc[:, j].sum()
                new_gdp += p_energy_hc_df.iloc[i, j] - p_energy_hc_df.iloc[i].sum() + p_rsrc_ext_hc_df.iloc[:, j].sum()
                new_gdp += p_energy_lc_df.iloc[i, j] - p_energy_lc_df.iloc[i].sum() + p_rsrc_ext_hc_df.iloc[:, j].sum()

                emissions += p_rsrc_ext_hc_df.iloc[i, j] * 0.04 # Production
                emissions += p_indust_hc_df.iloc[i, j] * 0.03
                emissions += p_cons_g_hc_df.iloc[i, j] * 0.01
                emissions += p_agric_hc_df.iloc[i, j] * 0.02
                emissions += p_energy_hc_df.iloc[i, j] * 0.05

                emissions += p_rsrc_ext_lc_df.iloc[i, j] * 0.03
                emissions += p_indust_lc_df.iloc[i, j] * 0.04
                emissions += p_cons_g_lc_df.iloc[i, j] * 0.02
                emissions += p_agric_lc_df.iloc[i, j] * 0.05
                emissions += p_energy_lc_df.iloc[i, j] * 0.01

            emissions += p_rsrc_ext_hc_df.iloc[i, j] * 0.03 # Transportation
            emissions += p_indust_hc_df.iloc[i, j] * 0.03
            emissions += p_cons_g_hc_df.iloc[i, j] * 0.03
            emissions += p_agric_hc_df.iloc[i, j] * 0.03
            emissions += p_energy_hc_df.iloc[i, j] * 0.03
            emissions += p_energy_lc_df.iloc[i, j] * 0.03

            emissions += p_rsrc_ext_lc_df.iloc[i, j] * 0.03
            emissions += p_indust_lc_df.iloc[i, j] * 0.03
            emissions += p_cons_g_lc_df.iloc[i, j] * 0.03
            emissions += p_agric_lc_df.iloc[i, j] * 0.03
            emissions += p_energy_lc_df.iloc[i, j] * 0.03

        # Update resources
        resource_df.iloc[1, i+1] = new_gdp # GDP
        resource_df.iloc[2, i+1] += (new_gdp * 0.3) # Budget
        resource_df.iloc[3, i+1] = emissions # Emissions
        resource_df.iloc[1, i+1] = int(round(resource_df.iloc[1, i+1])) # Make it easier to read
        resource_df.iloc[2, i+1] = int(round(resource_df.iloc[2, i+1]))
        resource_df.iloc[3, i+1] = int(round(resource_df.iloc[3, i+1])) 


    # Load back into the buffer
    buffer_df.iloc[row_boundary + 3 + rsrc_ext_hc_loc:row_boundary + rsrc_ext_hc_loc + 3 + len(countries), column_boundary + 1:] = p_rsrc_ext_hc_df.values
    buffer_df.iloc[row_boundary + 3 + rsrc_ext_lc_loc:row_boundary + rsrc_ext_lc_loc + 3 + len(countries), column_boundary + 1:] = p_rsrc_ext_lc_df.values

    buffer_df.iloc[row_boundary + 3 + indust_hc_loc:row_boundary + indust_hc_loc + 3 + len(countries), column_boundary + 1:] = p_indust_hc_df.values
    buffer_df.iloc[row_boundary + 3 + indust_lc_loc:row_boundary + indust_lc_loc + 3 + len(countries), column_boundary + 1:] = p_indust_lc_df.values

    buffer_df.iloc[row_boundary + 3 + cons_g_hc_loc:row_boundary + cons_g_hc_loc + 3 + len(countries), column_boundary + 1:] = p_cons_g_hc_df.values
    buffer_df.iloc[row_boundary + 3 + cons_g_lc_loc:row_boundary + cons_g_lc_loc + 3 + len(countries), column_boundary + 1:] = p_cons_g_lc_df.values

    buffer_df.iloc[row_boundary + 3 + agric_hc_loc:row_boundary + agric_hc_loc + 3 + len(countries), column_boundary + 1:] = p_agric_hc_df.values
    buffer_df.iloc[row_boundary + 3 + agric_lc_loc:row_boundary + agric_lc_loc + 3 + len(countries), column_boundary + 1:] = p_agric_lc_df.values

    buffer_df.iloc[row_boundary + 3 + energy_hc_loc:row_boundary + energy_hc_loc + 3 + len(countries), column_boundary + 1:] = p_energy_hc_df.values
    buffer_df.iloc[row_boundary + 3 + energy_lc_loc:row_boundary + energy_lc_loc + 3 + len(countries), column_boundary + 1:] = p_energy_lc_df.values

    buffer_df.iloc[0:row_boundary-1, :column_boundary] = resource_df.values

    # Write to the file
    with pd.ExcelWriter('datasheet.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        buffer_df.to_excel(writer, sheet_name='buffer', index=False)