import pandas as pd

detats = pd.read_csv('CSVs\Detachments.csv')
detats = detats[detats['type'] == 'Boarding Actions']
print(detats)