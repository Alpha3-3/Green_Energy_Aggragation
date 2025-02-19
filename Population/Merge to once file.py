import pandas as pd

# List your CSV files here
csv_files = ['Processed_Education2023.csv', 'Processed_Poverty2023.csv', 'Processed_Unemployment2023.csv', 'Processed_PopulationEstimates.csv']

# Initialize the merged DataFrame with the first CSV file
merged_df = pd.read_csv(csv_files[0])

# Loop through the remaining CSV files and merge them on 'fips_code'
for file in csv_files[1:]:
    df = pd.read_csv(file)
    merged_df = pd.merge(merged_df, df, on='fips_code', how='outer')

# Save the merged DataFrame to a new CSV file
merged_df.to_csv('DemographicsData.csv', index=False)
print("Merged CSV file saved as 'merged_data.csv'")
