import matplotlib.pyplot as plt
import pandas as pd
import pymongo


client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')

mydb=client['mydb']
tradeinfo = mydb.TradeDetails


# all_data = list(tradeinfo.find(filter={} , projection={"_id": 0, "custName": 1, 'spnl': 2}))
all_data = list(tradeinfo.find(filter={}, projection={"custName": 1, 'spnl': 1}))
df = pd.DataFrame(all_data)
group_sizes = df.groupby('custName').size()
# to plot the size of group using Matplotlib
group_sizes.plot(kind='bar')
plt.xlabel('Cust')
plt.ylabel('Spnls')
plt.title('Graph Showing Group Sizes')
plt.show()

print(df)

# agg_result= tradeinfo.aggregate( 
#     [{ 
#     "$group" :  
#         {"_id" : "$custName",  
#          "num_tutorial" : {"$sum" : 1} 
#          }} 
#     ]) 
# for i in agg_result: 
#     print(i)

# all_data = list(tradeinfo.find(filter={} , projection={"_id": 0, "custName": 1, 'spnl': 2}))
# df = pd.DataFrame(all_data)
# status_counts = df['spnl'].value_counts()
# print(status_counts)
# plt.bar(status_counts.index, status_counts.values)
# plt.show()

# query='spnl'

# lst_power_production = list(tradeinfo.find(filter={}, projection={"_id": 3, "custName": 1, query: 1}))

# df_mongo = pd.DataFrame(lst_power_production)


# # Create DataFrame
# #df = pd.DataFrame(data)

# # Count the occurrences of each trade status
# status_counts = df_mongo['spnl'].value_counts()

# print(status_counts)

# # df_mongo.groupby(['ctr','ccy'], as_index=True)['spnl'].mean().unstack().iplot(kind='bar', mode='group', title='Average Customer Satisfaction by Store')
# # Create bar chart
# plt.bar(status_counts.index, status_counts.values)

# # Add labels and title
# plt.xlabel(query)
# plt.ylabel('Count')
# plt.title('Distribution of '+query)

# # Display the chart
# plt.show()