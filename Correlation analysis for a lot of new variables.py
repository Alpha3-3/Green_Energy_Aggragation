import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the datasets
outage_df = pd.read_csv('Outage/Aggregated_Outage_Events.csv')
grouped_df = pd.read_csv('DS/Grouped_By_FIPS_List.csv')
demographics_df = pd.read_csv('Population/Processed_PopulationEstimates.csv')

print("outage_df",len(outage_df))
print("grouped_df",len(grouped_df))
print("demographics_df",len(demographics_df))

# Convert necessary fields to lists of floats where applicable
def safe_convert_to_list(x):
    try:
        return [float(i) for i in x.strip('[]').split(',')] if isinstance(x, str) else ([x] if isinstance(x, (int, float)) else [])
    except Exception:
        return []

outage_df['durations_hrs'] = outage_df['durations_hrs'].apply(safe_convert_to_list)
outage_df['sums'] = outage_df['sums'].apply(safe_convert_to_list)

grouped_df['total_power_usage_kwh'] = grouped_df['total_power_usage_kwh'].apply(safe_convert_to_list)
grouped_df['total_carbon_emission_2023_tons'] = grouped_df['total_carbon_emission_2023_tons'].apply(safe_convert_to_list)

grouped_df['number_of_data_centers'] = grouped_df['data_centers'].apply(lambda x: len(eval(x)) if pd.notnull(x) else 0)

# Convert demographic fields to numeric where applicable
demographics_cols = demographics_df.columns.difference(['fips_code'])
demographics_df[demographics_cols] = demographics_df[demographics_cols].apply(pd.to_numeric, errors='coerce')

# Merge all datasets on 'fips_code'
merged_df = pd.merge(outage_df, grouped_df, on='fips_code', how='outer')
merged_df = pd.merge(merged_df, demographics_df, on='fips_code', how='outer')

# Flatten list columns by taking the mean
merged_df['avg_durations_hrs'] = merged_df['durations_hrs'].apply(lambda x: sum(x) / len(x) if isinstance(x, list) and len(x) > 0 else 0)
merged_df['sum_duration_hrs'] = merged_df['durations_hrs'].apply(lambda x: sum(x) if isinstance(x, list) and len(x) > 0 else 0)
merged_df['sums_sum'] = merged_df['sums'].apply(lambda x: sum(x) if isinstance(x, list) and len(x) > 0 else 0)
merged_df['avg_power_usage'] = merged_df['total_power_usage_kwh'].apply(lambda x: sum(x) / len(x) if isinstance(x, list) and len(x) > 0 else 0)
merged_df['avg_carbon_emission'] = merged_df['total_carbon_emission_2023_tons'].apply(lambda x: sum(x) / len(x) if isinstance(x, list) and len(x) > 0 else 0)

# Reorder columns for correlation analysis
outage_columns = list(outage_df.columns.difference(['fips_code']))
grouped_columns = list(grouped_df.columns.difference(['fips_code']))
correlation_columns = outage_columns + grouped_columns + list(demographics_cols)

# Ensure only numeric columns are used for correlation
numeric_columns = merged_df.select_dtypes(include=['number', 'float']).columns

# First correlation (with data centers)


merged_df_with_centers = merged_df[merged_df['number_of_data_centers'] > 0]
correlation_matrix_with_centers = merged_df_with_centers[numeric_columns].corr()


# Second correlation (without data centers)
correlation_matrix_all_counties = merged_df[numeric_columns].corr()

print(merged_df.info())


# Visualization function with adjusted size and font
def plot_correlation(corr_matrix, title):
    plt.figure(figsize=(14, 12))  # Increased figure size
    sns.heatmap(
        corr_matrix,  cmap="coolwarm", annot=True, fmt=".2f", center=0
    )
    plt.title(title)
    plt.show()

# Plot the correlations
plot_correlation(
    correlation_matrix_with_centers,
    f"Pearson Correlation (Only With Counties With Data Centers) | Size: {len(merged_df_with_centers)}"
)

plot_correlation(
    correlation_matrix_all_counties,
    f"Pearson Correlation (All Counties) | Size: {len(merged_df)}"
)


# Save the correlation matrices to CSV
correlation_matrix_with_centers.to_csv('Correlation_Matrix_Only_Counties_With_Data_Centers.csv')
correlation_matrix_all_counties.to_csv('Correlation_Matrix_All_Counties.csv')


correlation_difference = correlation_matrix_with_centers - correlation_matrix_all_counties
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_difference, cmap="coolwarm", annot=True, fmt=".2f", center=0)
plt.title("Difference in Pearson Correlation (With vs. Without Data Centers)")
plt.show()