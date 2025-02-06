import pandas as pd
import subprocess
import time
from datetime import datetime

# Read the original sample sheet
df = pd.read_csv('/home/azureuser/ph-metagenomics/sample_sheet.csv')

# DataFrame to store outcomes
outcomes_df = pd.DataFrame(columns=['Sample', 'Status', 'Duration', 'ErrorMessage'])
rows_list = []

# each row in the sample sheet belongs to a sample_id. I want to group the rows by sample_id and then run the pipeline for each sample_id

# Group the rows by sample_id
grouped_df = df.groupby('sample_id')

# Iterate over the groups
for sample_id, group_df in grouped_df:

    # Create a new sample sheet for the current group
    new_sample_sheet_name = f"sample_sheet_{sample_id}.csv"
    group_df.to_csv(new_sample_sheet_name, index=False)

    # Prepare the Nextflow command
    nextflow_command = f"sudo nextflow -C /home/azureuser/ph-metagenomics/nextflow-dev.config run /home/azureuser/ph-metagenomics/main.nf \
        --samples_file '/home/azureuser/ph-metagenomics/{new_sample_sheet_name}' \
        --with-timeline \
        --outdir 'az://samples-results/debug' \
        -w 'az://work'"

    # Run the Nextflow command and measure duration
    start_time = datetime.now()
    try:
        process = subprocess.Popen(nextflow_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, bufsize=1)
        for line in iter(process.stdout.readline, b''):
            print(line.decode('utf-8').strip())

        # subprocess.check_call(nextflow_command, shell=True)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        rows_list.append({'Sample': sample_id, 'Status': 'Success', 'Duration': duration, 'ErrorMessage': None})
        outcomes_df = pd.DataFrame(rows_list)               
        # Save the outcomes to a CSV file
        outcomes_df.to_csv('pipeline_outcomes.csv', index=False)
    except subprocess.CalledProcessError as e:
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        rows_list.append({'Sample': sample_id, 'Status': 'Success', 'Duration': duration, 'ErrorMessage': e.output.decode()})

    # Remove the new sample sheet
    subprocess.run(f"rm {new_sample_sheet_name}", shell=True)




