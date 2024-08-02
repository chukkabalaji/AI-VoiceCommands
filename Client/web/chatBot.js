import { TradeObject } from "./TradeObject.js";

var messages = [], 
  lastUserMessage = "", 
  botMessage = "",
  botName = 'Tradebot';

function chatbotResponse() {
  document.getElementById("TradeDataTable").style.display = "none"; 
  document.getElementById("TradeBookWindow").style.display = "none"; 
  botMessage = "I'm confused"; //the default message
  if (lastUserMessage.toLowerCase() === 'clear') {
    for (var i = 1; i < 15; i++) {
      if (messages[messages.length - i]){
        messages[messages.length - i] = ""
        document.getElementById("chatlog" + i).innerHTML = messages[messages.length - i];
      }
    }
    return;
  }
  if (lastUserMessage.toLowerCase() === 'name' || lastUserMessage.toLowerCase() === 'whoami') {
    botMessage = 'My name is ' + botName;
    messages.push("<b>" + botName + ":</b> " + botMessage);
      for (var i = 1; i < 15; i++) {
        if (messages[messages.length - i])
          document.getElementById("chatlog" + i).innerHTML = messages[messages.length - i];
      }
    return;
  }
  if (lastUserMessage.toLowerCase() === 'help' || lastUserMessage.toLowerCase() === 'info') {
    botMessage = ' <br> &nbsp; Trade Booking     &nbsp; &nbsp; book trade for [CUSTID]:[B/S]:[CCY/CTR]:[Amount]:[Rate]:[TYPE]:[Y/N ndfIndicator] <br>';
    // botMessage = botMessage + '&nbsp; Trade Amend     &nbsp; &nbsp; amend trade [TRADEID] with rate [RATE] <br>';
    botMessage = botMessage + '&nbsp; Trade info      &nbsp;  &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; [TRADEID] <br>';
    botMessage = botMessage + '&nbsp; Analyze       &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp; Analyze [What you wnat to analyze] <br>';
    botMessage = botMessage + '&nbsp; NDF Trades      &nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp; Show all the NDF trades <br>';
    botMessage = botMessage + '&nbsp; Todays NDF      &nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;Show only todays NDF trades <br>';
    botMessage = botMessage + '&nbsp; Fix NDF     &nbsp; &nbsp;&nbsp; &nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp; Fix todays NDF trades <br>';
    messages.push("<b>" + botName + ":</b> " + botMessage);
      for (var i = 1; i < 15; i++) {
        if (messages[messages.length - i])
          document.getElementById("chatlog" + i).innerHTML = messages[messages.length - i];
      }
    return;
  }
  eel.processCmdInput(lastUserMessage)(callback_result);
}

function callback_result(output){
  if(null != output){
    botMessage = output
    messages.push("<b>" + botName + ":</b> " + botMessage);
      for (var i = 1; i < 15; i++) {
        if (messages[messages.length - i])
          document.getElementById("chatlog" + i).innerHTML = messages[messages.length - i];
      }
  }
}

function newEntry() {
  //if the message from the user isn't empty then run 
  if (document.getElementById("chatbox").value != "") {
    //pulls the value from the chatbox ands sets it to lastUserMessage
    lastUserMessage = document.getElementById("chatbox").value;
    //sets the chat box to be clear
    document.getElementById("chatbox").value = "";
    //adds the value of the chatbox to the array messages
    messages.push("<b>" + "User" + ":</b> " + lastUserMessage);
    chatbotResponse();
    // messages.push("<b>" + botName + ":</b> " + botMessage);
    // for (var i = 1; i < 8; i++) {
    //   if (messages[messages.length - i])
    //     document.getElementById("chatlog" + i).innerHTML = messages[messages.length - i];
    // }
  }
}

//runs the keypress() function when a key is pressed
document.onkeypress = keyPress;
//if the key pressed is 'enter' runs the function newEntry()
function keyPress(e) {
  var x = e || window.event;
  var key = (x.keyCode || x.which);
  if (key == 13 || key == 3) {
    //runs this function when enter is pressed
    newEntry();
  }
  if (key == 38) {
    console.log('hi')
      //document.getElementById("chatbox").value = lastUserMessage;
  }
}
//clears the placeholder text ion the chatbox
//this function is set to run when the users brings focus to the chatbox, by clicking on it
function placeHolder() {
  document.getElementById("chatbox").placeholder = "";
}

function prepareTradeDataObj(query){
  console.log(query)
  const custName = query[0] == 1111 ? "Wells Fargo Ltd." : "Google India ltd."
  const buySellIndicator = query[1];    
  const curData = query[2].split("/");
  const ccy = curData[0];
  const ctr = curData[1];
  
  const isInverted = true;
  let valueDateStr = new Date();
  const valueDate = valueDateStr.toLocaleDateString('en-GB'); 
  const ccyAmount = query[3];
  const allInRate = query[4];
  const ctrAmount = (ccyAmount/allInRate).toFixed(2).toString();
  const notes = query[5] == "SPOT" ? "Spot Trade" : "Fwd Trade";
  const typeOfTrade =  query[5];  
  const isNDF = query[6] == "Y" ? true:false;  
  const fixingDate = query[6] == "Y" ? valueDate : "NA" ;
  const fixingStatus = 'N';
  const tobj = new TradeObject(custName , buySellIndicator, ccy, ctr, allInRate, isInverted, valueDate, ccyAmount,ctrAmount,notes,typeOfTrade, isNDF, fixingDate, fixingStatus);
  console.log("object created is "+isInverted)
  eel.submitTrade(JSON.stringify(tobj))(prepareTradeDataObjCallback)  
}

function prepareTradeDataObjCallback(output){
  botMessage = output
  messages.push("<b>" + botName + ":</b> " + botMessage);
    for (var i = 1; i < 15; i++) {
      if (messages[messages.length - i])
        document.getElementById("chatlog" + i).innerHTML = messages[messages.length - i];
    }
}

eel.expose(prepareTradeDataObj)