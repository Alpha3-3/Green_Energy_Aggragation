import pandas as pd
from datetime import timedelta

# Load the outages data
outages = pd.read_csv('eaglei_outages_2023.csv')

# Ensure 'run_start_time' is datetime
outages['run_start_time'] = pd.to_datetime(outages['run_start_time'])

# Filter for outages with 'sum' >= 10
outages = outages[outages['sum'] >= 10]

# Sort by fips_code and run_start_time
outages = outages.sort_values(by=['fips_code', 'run_start_time']).reset_index(drop=True)

def aggregate_outages(group):
    """Aggregate outages into events for a single fips_code."""
    start_times, end_times, durations, sums = [], [], [], []
    current_start, current_end, current_sums = None, None, []

    for _, row in group.iterrows():
        start_time = row['run_start_time']
        end_time = start_time + timedelta(minutes=15)  # Fixed duration of 15 minutes
        outage_sum = row['sum']

        if current_start is None:
            # Start a new event
            current_start, current_end = start_time, end_time
            current_sums = [outage_sum]
        elif start_time - current_end <= timedelta(hours=2):
            # Extend the current event
            current_end = max(current_end, end_time)
            current_sums.append(outage_sum)
        else:
            # Save the current event and start a new one
            start_times.append(current_start)
            end_times.append(current_end)
            durations.append((current_end - current_start).total_seconds() / 3600)
            sums.append(sum(current_sums))
            current_start, current_end = start_time, end_time
            current_sums = [outage_sum]

    # Add the last event
    if current_start is not None:
        start_times.append(current_start)
        end_times.append(current_end)
        durations.append((current_end - current_start).total_seconds() / 3600)
        sums.append(sum(current_sums))

    # Aggregate information
    return pd.Series({
        'start_times': start_times,
        'end_times': end_times,
        'durations_hrs': durations,
        'sums': sums,
        'counts_of_outage': len(start_times),
        'average_sums': sum(sums) / len(sums) if sums else 0
    })

# Apply the aggregation function to each group
aggregated_outages = outages.groupby(['fips_code', 'county', 'state']).apply(aggregate_outages).reset_index()

# Save the aggregated data to a new CSV
aggregated_outages.to_csv('Aggregated_Outage_Events.csv', index=False)

# Print the first few rows
print(aggregated_outages.head())
