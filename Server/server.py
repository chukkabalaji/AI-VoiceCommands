from flask import Flask, jsonify, request
import os
import openai
from jproperties import Properties
import json
import random
from pymongo import MongoClient
app = Flask(__name__)
import constants
import os
import sys
from bson.json_util import dumps, loads
from bson import json_util
import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
import matplotlib.pyplot as plt
import pandas as pd
import pymongo
import datetime

os.environ["OPENAI_API_KEY"] = constants.APIKEY

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = False
chat_history = []

@app.route('/showAnalysis/<query>')
def showAnalysis(query):
    if query =='spnl':
        all_data = list(collection.find(filter={}, projection={"custName": 1, 'spnl': 1}))
        df = pd.DataFrame(all_data)
        group_sizes = df.groupby('custName').size()
        # to plot the size of group using Matplotlib
        group_sizes.plot(kind='bar')
        plt.xlabel('Customer')
        plt.ylabel('Profit and Loss')
        plt.title('Graph Showing Group Sizes')
        plt.show()
    else:
        lst_power_production = list(collection.find(filter={}, projection={"_id": 0, "ccy": 1, query: 1}))
        df_mongo = pd.DataFrame(lst_power_production)
        # Create DataFrame
        #df = pd.DataFrame(data)
        # Count the occurrences of each trade status
        status_counts = df_mongo[query].value_counts()
        print(status_counts)
        # Create bar chart
        plt.bar(status_counts.index, status_counts.values)
        # Add labels and title
        plt.xlabel(query)
        plt.ylabel('Count')
        plt.title('Distribution of '+ query)
        # Display the chart
        plt.show()

@app.route('/getTradeDetails/<query>')
def getTradeDetails(query):          
    myquery = {'tradeId': int(query)}    
    print(myquery)
    mydoc = collection.find(myquery)
    for trade in mydoc:
        print(trade)
        # list_cur = list(trade)
        # Converting to the JSON
        json_data = parse_json(trade) 
        print(json_data)
        return json_data
    return "Trade id "+query+" not found"
@app.route('/fixNDFTradeData/')
def fixNDFTradeData():
    now = datetime.datetime.now()
    todaysDate = now.strftime("%d/%m/%Y")
    myquery = {
            'isNDF': True, 
            'fixingStatus': 'N', 
            'fixingDate': {
                '$eq': todaysDate
            }
    }
    newvalues = { "$set": { "fixingStatus": "Y" } }
    x = collection.update_many(myquery, newvalues)
    print(x.modified_count, "documents updated.")
    return str(x.modified_count) + "documents updated."

@app.route('/getNDFTradeData/')
def getNDFTradeData():  
    isTodays = request.get_json()["isTodays"]
    now = datetime.datetime.now()
    todaysDate = now.strftime("%d/%m/%Y")
    if isTodays:
        myquery = {
            'isNDF': True, 
            'fixingStatus': 'N', 
            'fixingDate': {
                '$eq': todaysDate
            }
        }
    else:
        myquery = {
            'isNDF': True, 
            'fixingStatus': 'N'
        }
    print(myquery)
    mydoc = collection.find(myquery)
    result_list = []
    for trade in mydoc:
        print(trade)
        # list_cur = list(trade)
        # Converting to the JSON
        json_data = parse_json(trade) 
        print(json_data)
        result_list.append(json_data)
    return result_list

def parse_json(data):
    return json.loads(json_util.dumps(data))

@app.route('/bookTrade/', methods=['POST'])
def bookTrade():
    print(request.get_json())
    data = json.loads(request.get_json())
    # custName = data['custName']
    # buySellIndicator = data['buySellIndicator']
    ccy = data['ccy']
    ctr = data['ctr']      
    allInRate = data['allInRate']
    # isInverted = data['isInverted']
    # valueDate = data['valueDate']    
    ccyAmount = data['ccyAmount']
    # ctrAmount = data['ctrAmount']
    # notes = data['notes']
    # typeOfTrade = data['typeOfTrade']
    # isNDF = data['isNDF']
    # fixingDate = data['fixingDate'] 
    # fixingStatus = data['fixingStatus']
    tradeId = random.randint(6193279, 7977864)
    data['tradeId'] = tradeId
    data['spnl'] = round(int(ccyAmount)/float(81.0987),2)
    updatePropertiesValues(data)
    return 'TradeId : '+ str(tradeId) +' is booked for currency pair '+ccy+"/"+ctr

def updatePropertiesValues(data):    
    configs = Properties()
    configs["custName"] = data['custName']
    configs["buySellIndicator"] = data['buySellIndicator']
    configs["ccy"] = data['ccy']
    configs["ctr"] = data['ctr']
    configs["allInRate"] = data['allInRate']
    configs["isInverted"] = 'Y' if data['isInverted'] else 'N'
    configs["valueDate"] = data['valueDate']
     
    configs["ccyAmount"] = data['ccyAmount']
    configs["ctrAmount"] = data['ctrAmount']
    configs["notes"] = data['notes']
    configs["typeOfTrade"] = data['typeOfTrade']
    configs["isNDF"] = 'Y' if data['isNDF'] else 'N'
    configs["fixingDate"] = data['fixingDate']
    configs["fixingStatus"] = data['fixingStatus']
    with open("D:\HackathonProject\AI_Assistance\Client\\tradeData.properties", "wb") as f:
        configs.store(f, encoding="utf-8")
    collection.insert_one(data)


@app.route('/getLiveRate/<query>')
def getLiveRate(query):
    result = chain({"question": query, "chat_history": chat_history})
    return result['answer']

@app.route('/getInfo/<query>')
def getInfo(query):
    response = openai.Completion.create(
        engine='text-davinci-003',  # Specify the GPT-3 model variant
        prompt=query,
        max_tokens=20  # Set the desired length of the generated text
    )
    generated_text = response.choices[0].text.strip()
    return generated_text

if __name__ == "__main__":
    
    if PERSIST and os.path.exists("persist"):
        print("Reusing index...\n")
        vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
        global index
        index = VectorStoreIndexWrapper(vectorstore=vectorstore)
    else:
        loader = TextLoader("./data/data4.txt")  #Use this line if you only need data.txt
        # loader = DirectoryLoader("data/")
        if PERSIST:
            index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"}).from_loaders([loader])
        else:
            index = VectorstoreIndexCreator().from_loaders([loader])

    chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3),
    retriever = index.vectorstore.as_retriever(search_kwargs={"k": 1}),
    )
    
    try:
        client = MongoClient('localhost', 27017)
        print("Connected successfully!!!")
    except:  
        print("Could not connect to MongoDB")
    
    # database
    my_db = client['mydb']

    print("List of databases after creating new one")
    print(client.list_database_names())

    # Created or Switched to collection names: my_gfg_collection
    global collection
    collection = my_db.TradeDetails
    app.run(debug=True)
    
