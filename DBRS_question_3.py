from __future__ import division
import pandas as pd
from sodapy import Socrata

#  Considering all complaint types. Which boroughs are the biggest "complainers" relative to the size of the population in 2017? Meaning, calculate a complaint-index that adjusts for population of the borough.

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

#: 2017 census population data sourced from https://www1.nyc.gov/site/planning/data-maps/nyc-population/current-future-populations.page
population_by_borough = {'bronx': 1471160, 'brooklyn': 2648771, 'manhattan': 1664727, 'queens': 2358582, 'staten_island': 479458}

complaints_boroughs = combined_df[['complaint_type', 'incident_zip', 'borough']]
#complaints_count = complaints_boroughs.groupby('borough').complaint_type.count()
bx_count = complaints_boroughs[complaints_boroughs['borough'] == 'BRONX'].complaint_type.count()
bx_index = bx_count / population_by_borough['bronx']
bk_count = complaints_boroughs[complaints_boroughs['borough'] == 'BROOKLYN'].complaint_type.count()
bk_index = bk_count / population_by_borough['brooklyn']
man_count = complaints_boroughs[complaints_boroughs['borough'] == 'MANHATTAN'].complaint_type.count()
man_index = man_count / population_by_borough['manhattan']
qns_count = complaints_boroughs[complaints_boroughs['borough'] == 'QUEENS'].complaint_type.count()
qns_index = qns_count / population_by_borough['queens']
si_count = complaints_boroughs[complaints_boroughs['borough'] == 'STATEN ISLAND'].complaint_type.count()
si_index = si_count / population_by_borough['staten_island']

data = {
    'Borough': ['BRONX', 'BROOKLYN', 'MANHATTAN', 'QUEENS', 'STATEN ISLAND'],
    'Uncorrected Count': [bx_count, bk_count, man_count, qns_count, si_count],
    'Complaint Index': [bx_index, bk_index, man_index, qns_index, si_index],
    'Corrected Count': [(bx_count * bx_index), (bk_count * bk_index), (man_count * man_index), (qns_count * qns_index), (si_count * si_index)]
}
df = pd.DataFrame(data)
print(df)

