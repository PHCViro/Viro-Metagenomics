import pandas as pd
import re 

pd.set_option("display.max_columns", None)

def multibase_codon_detection(snpsift_df, hbv_df):

    # Create an empty list to store the new dataframes
    result_df = pd.DataFrame(columns=['Gene', 'codon', 'bases'])
    # Iterate over each row in the hbv_codeonbases.csv
    for idx, row in hbv_df.iterrows():
        # Check if at least two of the values for base1, base2, or base3 appear in the POS column of the snpsift.txt
        bases = [row['base1'], row['base2'], row['base3']]
        count = len(set(snpsift_df['POS']).intersection(bases))
        detected_bases = re.sub('\{|\}', '', str(set(snpsift_df['POS']).intersection(bases))) 
        detected_bases = detected_bases.replace(',', ';')
        if count >= 2:
            # Create a new dataframe for each row that meets this condition
            new_row = pd.DataFrame({'Gene': [row['Gene']], 'codon': [row['codon']], 'bases': detected_bases})
            # append new row to the result_df
            result_df = pd.concat([result_df, new_row], ignore_index=True)

    return result_df

# Load the data
snpsift_df = pd.read_csv('/home/azureuser/ph-metagenomics/bin/snpsift.txt', sep='\t')  # assuming tab-separated values
hbv_df = pd.read_csv('/home/azureuser/ph-metagenomics/bin/hbv_codeonbases.csv')

# Create an empty list to store the new dataframes
new_rows = []
result_df = pd.DataFrame(columns=['Gene', 'codon', 'bases'])

result_df = multibase_codon_detection(snpsift_df, hbv_df)

result_df.to_csv( path, index=False)  # Save the result to a new CSV file
result_df.to_csv(path.replace('csv', 'txt'), sep='\t', index=False, encoding="utf-8-sig")
