import pandas as pd
import numpy as np
from sodapy import Socrata

# Consider only the 10 most common overall complaint types.  For the 10 most populous zip codes, how many of each of those 10 types were there in 2017?

pd.options.display.max_rows = 5000

token = '9EDniwZuIo69m780HXzBZ7oxK'
client = Socrata('data.cityofnewyork.us', token)
results1 = client.get('fhrw-4uyv',  where="created_date between '2017-01-01T00:00:00.000' and '2017-12-31T00:00:00.00'", select="complaint_type, incident_zip, borough", limit=500000, order='created_date ASC')
results2 = client.get('fhrw-4uyv',  where="created_date between '2017-01-01T00:00:00.000' and '2017-12-31T00:00:00.00'", select="complaint_type, incident_zip, borough", limit=500000, order='created_date ASC', offset=500000)
results3 = client.get('fhrw-4uyv',  where="created_date between '2017-01-01T00:00:00.000' and '2017-12-31T00:00:00.00'", select="complaint_type, incident_zip, borough", limit=500000, order='created_date ASC', offset=1000000)
results4 = client.get('fhrw-4uyv',  where="created_date between '2017-01-01T00:00:00.000' and '2017-12-31T00:00:00.00'", select="complaint_type, incident_zip, borough", limit=500000, order='created_date ASC', offset=1500000)
results5 = client.get('fhrw-4uyv',  where="created_date between '2017-01-01T00:00:00.000' and '2017-12-31T00:00:00.00'", select="complaint_type, incident_zip, borough", limit=500000, order='created_date ASC', offset=2000000)

results_df1 = pd.DataFrame.from_records(results1)
results_df2 = pd.DataFrame.from_records(results2)
results_df3 = pd.DataFrame.from_records(results3)
results_df4 = pd.DataFrame.from_records(results4)
results_df5 = pd.DataFrame.from_records(results5)

combined_df = pd.concat([results_df1, results_df2, results_df3, results_df4, results_df5])
#: Get the top 10 complaints
all_complaints = combined_df[['complaint_type']]
top_tens = all_complaints.complaint_type.value_counts()[:10]
top_ten_complaints = top_tens.to_dict().keys()

#: Clean the zip codes - Remove short zips and all zero zips
all_zips = combined_df.incident_zip.str.slice(0, 5)
short_zips = all_zips.str.len() < 5
zero_zips = all_zips == '00000'
combined_df[short_zips] = np.nan
combined_df[zero_zips] = np.nan
#remaining zips should all be clean
good_zips = combined_df.incident_zip.str.replace(r'[A-Z /.?]','')
good_zips = good_zips.str.slice(0, 5)

#: Sourced from Zipcode-ZCTA-Population-Density-And-Area-Unsorted
#: Filtered out non-NY zips and sorted by descending population count
top_ten_pop_zips = ['11368', '11226', '11373', '11220', '11385', '10467', '10025', '11208', '11236', '11207']

complaints_boroughs = combined_df[['complaint_type', 'incident_zip', 'borough']]
#: Get top 10 complaints
top_complaints_zip = complaints_boroughs[complaints_boroughs.complaint_type.isin(top_ten_complaints)]
#: Get complaints in top 10 zips
top_ten_complaints_and_zips = top_complaints_zip[top_complaints_zip.incident_zip.isin(top_ten_pop_zips)]
complaints_count = top_ten_complaints_and_zips.groupby('incident_zip').complaint_type.value_counts()
print(complaints_count)

