import pandas as pd
import requests

pd.set_option('display.max_columns', None) #This is so we can see all the columns in a wide dataframe
import time
import numpy as np

test_url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2022-23&SeasonType=Regular%20Season&StatCategory=PTS'
r = requests.get(url=test_url).json()
tableHeaders=r['resultSet']['headers']

df_cols = ['Year', 'Season_type']+ tableHeaders
df = pd.DataFrame(columns=df_cols)
season_types = ['Regular%20Season' , 'Playoffs']
years = ['2012-13','2013-14','2014-15','2015-16','2016-17','2017-18','2018-19','2019-20','2020-21','2021-22','2022-23']

begin_loop = time.time()

for y  in years:
    for s in season_types:
        api_url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season='+y+'&SeasonType='+s+'&StatCategory=PTS'
        r = requests.get(url = api_url).json()
        temp_df1 = pd.DataFrame(r['resultSet']['rowSet'], columns=tableHeaders)
        temp_df2 = pd.DataFrame({'Year':[y for i in range(len(temp_df1))], 
                                 'Season_type':[s for i in range(len(temp_df1))]})
        temp_df3 = pd.concat([temp_df2, temp_df1], axis = 1)
        temp_df3
        df  = pd.concat([df, temp_df3], axis = 0)
        print(f'Finished scrapping data for the {y} {s}.')
        lag = np.random.uniform(low = 5,high = 15)
        print(f'....waiting {round(lag,1)} seconds')
        time.sleep(lag)

print(f'Process completed! Total runtime: {round((time.time()-begin_loop)/60,2)}')

df.to_excel('nba_player_data.xlsx', index=False)