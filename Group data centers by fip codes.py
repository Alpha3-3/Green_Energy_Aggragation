import pandas as pd

# Load the merged data
merge_ba_carbon_with_fips = pd.read_csv('Merge_BA_Carbon_with_FIPS.csv')

# Group by FIPS code and aggregate into lists
grouped_by_fips = merge_ba_carbon_with_fips.groupby('fips_code').agg(
    data_centers=('Data_center', list),  # Collect data center names into a list
    total_power_usage_kwh=('power_usage_2023_kwh', list),  # Collect power usage into a list
    avg_power_usage_per_hour=('power_usage_per_hour_2023_kwh', list)  # Collect avg power usage into a list
).reset_index()

# Save the grouped data to a new CSV file
grouped_by_fips.to_csv('Grouped_By_FIPS_List.csv', index=False)

# Print the first few rows of the grouped data
print(grouped_by_fips.head(10).to_string())
print(grouped_by_fips.info())