import pandas as pd
from datetime import datetime
import json
import numpy as np

etf_type="VOOG_2024"
# Read the CSV file
df = pd.read_csv(etf_type+'.csv')


# Converts mapping to date wise in a dict
df_dict = df.set_index('Date').to_dict(orient='index')

# Loop through the dates.
sorted_dict = dict(sorted(df_dict.items(), key=lambda item: datetime.strptime(item[0], "%m/%d/%Y")))

# print(sorted_dict['11/11/2024'])


# {'Price': 598.76, 'Open': 599.81, 'High': 600.11, 'Low': 597.03, 'Vol.': '31.33M', 'Change %': '0.10%'}
def caluclate_gain(data,threshold=None,Increment=100,investment=10000):
    intial_investment=investment
    increment_investment=0
    for date in data:
        percentage_change=data[date]['Change %']
        percentage_change=float(percentage_change[:-1])/100
        if percentage_change < threshold:
            investment=investment+(investment*percentage_change)+Increment
            increment_investment=increment_investment+Increment
        else:
            investment=investment+(investment*percentage_change)
        print("Date: "+str(date)+" investment: "+str(investment))
    percent_gain=(investment/(intial_investment+increment_investment))-1
    percent_gain=percent_gain*100
    return {"threshold":threshold,"investment":investment,"percent_gain":percent_gain}

# print(caluclate_gain(sorted_dict,-2.0,100,10000))


dataset={}
increment=100
investment=10000
for i in np.arange(-2, 2, 0.01):
    threshold=float(i/100)
    dataset[i]=caluclate_gain(sorted_dict,threshold,increment,investment)


data_df = pd.DataFrame.from_dict(dataset, orient='index')

file_name=etf_type+"_transfomred_data_set_incremtn_"+str(increment)+"_investetment_"+str(investment)+".csv"

data_df.to_csv(file_name, index=False)











