import pandas as pd

outages = pd.read_csv('Aggregated_Outage_Events.csv')

print(outages.head(10).to_string())
print(outages.info())