import gevent
import pyttsx3 # pip install pyttsx3 == text data into speech
import speech_recognition as sr # pip install SpeechRecognition 
import requests
from nltk.tokenize import word_tokenize
import eel
from jproperties import Properties
from fuzzywuzzy import fuzz
import json
import re

# <CUST_ID>:<B/S Indicator>:<CCY/CTR>:<Type i.e. SPOT,FWD>
# <TRADE_ID>
# custName=<Customer name>;ctr=<CTR> ctrAmount=<CTR amount>>

tradeBookKeywords = [];
tradeEnquiryKeywords = [];
analysisKeywords = ["analysis","data","analyze","analyse"];
ndfKeywords = ["ndf","n d f", "NDF"];
helpKeywords = ["help","Help", "INFO","info"];
fixKeywords = ["fix","FIX"];
tradeBookRegex = re.compile(r'\w* \w* \w* \d{4}:(B|S):(\w{3}/\w{3}):(\d*):\d*[.,]?\d*:(SPOT|FWD):(Y|N)')
tradeAmendRegex = re.compile(r'amend trade \d{7} with rate \d*[.,]?\d*')
tradeEnquiryRegex = re.compile(r'\b\d{7}\b')
# analysisRegex = re.compile(r'(analyze) \b(ctr|ccy|custName|valueDate|spnl)\b')
analysisRegex = re.compile(r'(analyze) \b\w*\b')
speechMode = True

def getNdfTrades(isTodays):
    URL = "http://127.0.0.1:5000/getNDFTradeData/"    
    try:
        payload = {'isTodays': isTodays}
        r = requests.get(URL,json=payload) 
        eel.displayNDFTableData(r.text)       
        print('SUCCESS')    
        speak('NDF trades fetched.')
        eel.displayResult('')    
        return "Success"      
    except Exception as e:
        print('FAILED')
        print(e)
        return 'error'
    
def fixNdfTrades():
    URL = "http://127.0.0.1:5000/fixNDFTradeData/"    
    try:        
        r = requests.get(URL) 
        speak('NDF trades Fixed.')
        getNdfTrades(True)            
        eel.displayResult('')    
        return "Success"      
    except Exception as e:
        print('FAILED')
        print(e)
        return 'error'
    
def showAnalysis(query):
    URL = "http://127.0.0.1:5000/showAnalysis/"    
    try:
        requests.get(URL+query)        
        eel.displayResult("Chart shown")        
    except Exception as e:
        print('FAILED')
        print(e)
        return 'error'

@eel.expose
def prepareAndSubmitTrade(query):
    eel.prepareTradeDataObj(re.split(':', query))(callback_prepareAndSubmitTrade)

def callback_prepareAndSubmitTrade(output):
    return output

# @eel.expose
# def setSpeechMode(val):
#     global speechMode
#     speechMode = val

@eel.expose
def submitTrade(data):
    print(data)
    URL = "http://127.0.0.1:5000/bookTrade/"    
    try:
        r = requests.post(URL,json=data)        
        eel.displayResult(r.text)
        if(speechMode):
            speak(r.text[:100])
        print('SUCCESS')    
        eel.displayResult('')    
        return r.text      
    except Exception as e:
        print('FAILED')
        print(e)
        return 'error'

@eel.expose
def getLiveRate(query):
    URL = "http://127.0.0.1:5000/getLiveRate/"
    try:
        r = requests.get(url = URL+query)
        eel.displayResult(r.text)
        print(r.text)
        speak(r.text[:100])  
        eel.displayResult('')
        print('SUCCESS')          
    except Exception as e:  
        print('FAILED')      
        print(e) 
        eel.displayResult('FAILED')

@eel.expose
def bookTrade():
    # api-endpoint
    configs = Properties()
    with open('tradeData.properties', 'rb') as read_prop:
        configs.load(read_prop)      
    prop_view = configs.items()
    print(type(prop_view))    
    data = {}
    for item in prop_view:
        print(item)
        data[item[0]]=item[1]
    jsonStr = json.dumps(data)
    print(jsonStr)
    eel.populateTradeDetails(jsonStr)
    if(speechMode):
        speak("Trade details are now populated.")    

@eel.expose
def populateCommands():
    # api-endpoint
    configs = Properties()
    with open('helpCommands.properties', 'rb') as read_prop:
        configs.load(read_prop)      
    prop_view = configs.items()
    print(type(prop_view))    
    data = {}
    tradeBookKeywords.clear
    tradeEnquiryKeywords.clear

    for item in prop_view:
        print(item)
        data[item[0]]=item[1]
        if(item[0].startswith('tradeBookingSpeech')):
            appendMoreStrings(tradeBookKeywords, item[1].data.lower())
        elif(item[0].startswith('tradeEnquirySpeech')):
            appendMoreStrings(tradeEnquiryKeywords, item[1].data.lower())          
    jsonStr = json.dumps(data)
    print(jsonStr)
    eel.populateHelpCommands(jsonStr)      

@eel.expose
def savePropertiesValues(data1):  
    data =  json.loads(data1);  
    # print("savePropertiesValues "+data)
    configs = Properties()
    configs["tradeBookingCmd"] = data['tradeBookingCmd']
    configs["tradeBookingSpeech"] = data['tradeBookingSpeech']
    configs["tradeEnquiryCmd"] = data['tradeEnquiryCmd']
    configs["tradeEnquirySpeech"] = data['tradeEnquirySpeech']  

    tradeBookKeywords.clear
    tradeEnquiryKeywords.clear

    appendMoreStrings(tradeBookKeywords, data['tradeBookingSpeech'].lower())
    appendMoreStrings(tradeEnquiryKeywords, data['tradeEnquirySpeech'].lower()) 

    print("tradeBookKeywords ",tradeBookKeywords)
    print("tradeEnquiryKeywords ",tradeEnquiryKeywords)

    with open("helpCommands.properties", "wb") as f:
        configs.store(f, encoding="utf-8")
    return "Properties saved !!"

@eel.expose
def getInfo(query):
    # api-endpoint
    URL = "http://127.0.0.1:5000/getInfo/"
    try:
        r = requests.get(url = URL+query)
        eel.displayResult(r.text)
        print(r.text)
        if(speechMode):
            speak(r.text[:200])  
        eel.displayResult('')
        print('SUCCESS')  
        return r.text
    except Exception as e:  
        print('FAILED')      
        print(e) 
        eel.displayResult('FAILED')   
        return "Error"

@eel.expose
def tradeEnquiry(query):
    print("Inside tradeEnquiry" + query)
    # api-endpoint    
    URL = "http://127.0.0.1:5000/getTradeDetails/"
    try:
        r = requests.get(url = URL+query)
        # eel.displayResult(r.text)
        print(r.text)
        # if(speechMode):
        #     speak(r.text[:100])          
        print('SUCCESS')  
        return r.text;     
    except Exception as e:  
        print('FAILED')      
        print(e) 
        eel.displayResult('FAILED')    
        return "Something went wrong"  

@eel.expose
def tradeAmend(query):
    print("Inside tradeAmend" + query)
    # api-endpoint    
    URL = "http://127.0.0.1:5000/amendTrade/"
    try:
        r = requests.get(url = URL+query)
        # eel.displayResult(r.text)
        print(r.text)
        # if(speechMode):
        #     speak(r.text[:100])          
        print('SUCCESS')  
        return r.text;     
    except Exception as e:  
        print('FAILED')      
        print(e) 
        eel.displayResult('FAILED')    
        return "Something went wrong"         


@eel.expose
def getNDFTradeData():
    print("Inside getNDFTradeData")
    # api-endpoint    
    URL = "http://127.0.0.1:5000/getNDFTradeData/"
    try:
        r = requests.get(url = URL)
        # eel.displayResult(r.text)
        print(r.text)
        # if(speechMode):
        #     speak(r.text[:100])          
        print('SUCCESS')  
        return r.text;     
    except Exception as e:  
        print('FAILED')      
        print(e) 
        eel.displayResult('FAILED')    
        return "Something went wrong"  


@eel.expose
def processCommand(query):
    queryList = word_tokenize(query)
    print(queryList)
    print("tradeBookKeywords ",tradeBookKeywords)
    print("tradeEnquiryKeywords ",tradeEnquiryKeywords)
    for q in queryList:
        if q in tradeBookKeywords:        
            return bookTrade() 
        elif q in analysisKeywords:
            return showAnalysis("ctr")
        elif q in tradeEnquiryKeywords:  
            print("Inside enquiry")
            res = ''.join(filter(lambda i: i.isdigit(), query))
            res = res.strip()
            print("query :"+res)
            if(res.isnumeric()):
                return tradeEnquiry(res)
            else:
                if(speechMode):
                    speak("Only numberic values are allowed")
                return "Only numberic values are allowed"  
        elif q in fixKeywords:
            ratioFixTodaysNDF = fuzz.ratio(query, 'Fix todays NDF trades')
            ratioFixNDF = fuzz.ratio(query, 'Fix NDF trades')            
            ratioFix = fuzz.ratio(query, 'Fix trades')            
            if(ratioFixTodaysNDF > 50 or ratioFixNDF > 50 or ratioFix > 50):
                return fixNdfTrades()                   
        elif q in ndfKeywords:
            ratioTodays = fuzz.ratio(query, 'Show only todays NDF trades')
            ratioAll = fuzz.ratio(query, 'Show all NDF trades')            
            return getNdfTrades(True if (ratioTodays > ratioAll) else False)
    return getInfo(query)

@eel.expose
def processCmdInput(query):
    queryList = word_tokenize(query)    
    for q in queryList:        
        if(tradeBookRegex.match(query)):
            return prepareAndSubmitTrade(query)
        elif(tradeEnquiryRegex.match(query)):
            return tradeEnquiry(query)
        # elif(tradeAmendRegex.match(query)):
        #     return tradeAmend(query)
        elif(analysisRegex.match(query)):
            query = query.replace("analyze","")
            query = query.strip()
            showAnalysis(query)
            return "Showing chart"
        elif q in ndfKeywords:
            ratioTodays = fuzz.ratio(query, 'Show only todays NDF trades')
            ratioAll = fuzz.ratio(query, 'Show all NDF trades')            
            return getNdfTrades(True if (ratioTodays > ratioAll) else False)
        elif q in fixKeywords:
            ratioFixTodaysNDF = fuzz.ratio(query, 'Fix todays NDF trades')
            ratioFixNDF = fuzz.ratio(query, 'Fix NDF trades')            
            ratioFix = fuzz.ratio(query, 'Fix trades')            
            if(ratioFixTodaysNDF > 50 or ratioFixNDF > 50 or ratioFix > 50):
                return fixNdfTrades()   
    return getInfo(query)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommandCMD():
    query = input("please tell me how can I help you\n")
    return query

@eel.expose
def takeCommandMic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        eel.displayMessage("Listening...")
        eel.displayListeningIcon()
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing..")
        eel.displayMessage("Recognizing..")
        query = r.recognize_google(audio, language="en-IN")
        print(query)
        eel.displayMessage(query)
    except Exception as e:
        print(e)
        speak("Say that again Please...") 
        query = "Error"       
    return query

def openUI():    
    eel.start("home.html", size =(1000,800),port=9000)    

@eel.expose
def giveCommand():
    speak("Hi How can I help you?")  
    return takeCommandMic().lower()  

def appendMoreStrings(list, strToBeAdded):
    newWords = word_tokenize(strToBeAdded)
    for nw in newWords:
        list.append(nw)

# from speech_recognition import Microphone as source
engine = pyttsx3.init()

if __name__== "__main__":    
    eel.init("D:\HackathonProject\AI_Assistance\Client\web")    
    openUI()