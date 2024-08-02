import { TradeObject } from "./TradeObject.js";
import { HelpObject } from "./HelpObject.js";

const colExclude = ['_id', 'allInRate','isInverted','notes', 'typeOfTrade'];

window.onload = function () {
	// document.getElementById("micbutton").style.display = "none";
    document.getElementById("TradeBookWindow").style.display = "none";    
    document.getElementById("TradeDataTable").style.display = "none";    
    eel.populateCommands()
}

document.getElementById("isNDF").onclick = function savePropertiesValues(){  
    if(document.getElementById("isNDF").checked == true){
        document.getElementById("fixingDate").disabled = false;
    }else{
        document.getElementById("fixingDate").disabled = true;
    }
}

function clearTableData(){
    var tableHeaderRowCount = 1;
    var table = document.getElementById('TradeDataTable');
    var rowCount = table.rows.length;
    for (var i = tableHeaderRowCount; i < rowCount; i++) {
        table.deleteRow(tableHeaderRowCount);
}
}

function displayNDFTableData(ndfTradesList){
    let tData = JSON.parse(ndfTradesList);
    if(tData.length != 0){
        document.getElementById("TradeDataTable").style.display = "block";
        clearTableData();
        const tableId = document.getElementById('TradeDataTable');
        let tData = JSON.parse(ndfTradesList);
        tData.forEach((dataRow, trIndex) => {
            let newRow = tableId.insertRow(-1);
            newRow.insertCell(-1).innerHTML = trIndex+1;        
            Object.keys(dataRow).forEach((dataCell, cellIndex) => { 
                if(!colExclude.includes(dataCell)){
                    let newCell = newRow.insertCell(-1);             
                    newCell.innerHTML =  tData[trIndex][dataCell];          
                }
            })
        }) 
    }else {
        displayMessage('There are no NDF trades for the given query');
        clearTableData();
    }
}

// document.getElementById("saveCmds").onclick = function savePropertiesValues(){  
//     document.getElementById("TradeBookWindow").style.display = "none";

//     const tradeBookingCmd = document.getElementById("tradeBookingCmd").value;
//     const tradeBookingSpeech = document.getElementById("tradeBookingSpeech").value;
//     const tradeEnquiryCmd = document.getElementById("tradeEnquiryCmd").value;
//     const tradeEnquirySpeech = document.getElementById("tradeEnquirySpeech").value;
//     const tobj = new HelpObject(tradeBookingCmd,tradeBookingSpeech,tradeEnquiryCmd,tradeEnquirySpeech);
//     console.log("object created is "+isInverted)
//     eel.savePropertiesValues(JSON.stringify(tobj)) (savePropCallback)  
// } 


// document.getElementById("speechCmdMode").onclick = function hideWindow(){
//     if(document.getElementById("speechCmdMode").checked == true) {
//         document.getElementById("TraderBotWindow").style.display = "none";
//         document.getElementById("micbutton").style.display = "inline-block";        
//         document.getElementById("TradeBookWindow").style.display = "none";
//         eel.setSpeechMode(true);
//     }else {
//         document.getElementById("TradeBookWindow").style.display = "none";
//         document.getElementById("TraderBotWindow").style.display = "block";
//         document.getElementById("micbutton").style.display = "none";
//         eel.setSpeechMode(false);
//     }
//     displayMessage("");
// }

document.getElementById("micbutton").onclick = function giveCommand(){    
    document.getElementById("TradeBookWindow").style.display = "none";     
    displayMessage("");  
    eel.giveCommand()(call_Back)  
}  

document.getElementById("getLiveRate").onclick = function getLiveRate(){
    const ccy = document.getElementById("ccy").value;
    const ctr = document.getElementById("ctr").value;
    eel.getLiveRate(ccy +" "+ ctr)(call_Back_rate)  
}  

const submitElement = document.getElementById("submitTrade");
submitElement.addEventListener("click", submitTrade);

function submitTrade(){  
    const custName = document.getElementById("custName").value;
    const buySellIndicator = document.getElementById("buySellIndicator").value == 1 ? "B" : "S";  
    const ccy = document.getElementById("ccy").value;
    const ctr = document.getElementById("ctr").value;
    const allInRate = document.getElementById("allInRate").value;
    const isInverted = document.getElementById("isInverted").checked;
    let valueDateStr = document.getElementById("valueDate").valueAsDate; 
    const valueDate = valueDateStr.toLocaleDateString('en-GB'); 
    const ccyAmount = document.getElementById("ccyAmount").value;
    const ctrAmount = document.getElementById("ctrAmount").value;
    const notes = document.getElementById("notes").value;
    const typeOfTrade = document.getElementById("typeOfTrade").value == 1 ?  "Spot" : "Fwd";
    const isNDF = document.getElementById("isNDF").checked;
    let fixingDate = "NA"
    if(isNDF){
        let fixingDateStr = document.getElementById("fixingDate").valueAsDate; 
        fixingDate = fixingDateStr.toLocaleDateString('en-GB'); 
    }
    const fixingStatus = 'N';
    const tobj = new TradeObject(custName , buySellIndicator, ccy, ctr, allInRate, isInverted, valueDate, ccyAmount,ctrAmount,notes,typeOfTrade,isNDF, fixingDate, fixingStatus);
    eel.submitTrade(JSON.stringify(tobj))(submitTradeCallback)  
}  

// function submitValues(){
//     custName = document.getElementById("custName").value;
//     buySellIndicator = document.getElementById("buySellIndicator").value;    
//     ccy = document.getElementById("ccy").value;
//     ctr = document.getElementById("ctr").value;
//     allInRate = document.getElementById("allInRate").value;
//     isInverted = document.getElementById("isInverted").checked;
//     valueDate = document.getElementById("valueDate").valueAsDate;
//     tobj = new TradeObject(custName , buySellIndicator, ccy, ctr, allInRate, isInverted, valueDate);
//     console.log("object created is "+tobj)
//     eel.submitTrade(JSON.stringify(tobj))(submitTradeCallback) 
// }

function populateTradeDetails(tradeData){
    console.log("Inside populate")
    const jsonObj = JSON.parse(tradeData)    
    document.getElementById("custName").value = jsonObj.custName[0] 
    document.getElementById("buySellIndicator").value = jsonObj.buySellIndicator[0]
    
    document.getElementById("ccy").value = jsonObj.ccy[0]
    document.getElementById("ctr").value = jsonObj.ctr[0]
    document.getElementById("allInRate").value = jsonObj.allInRate[0]

    document.getElementById("ccyAmount").value = jsonObj.ccyAmount[0]
    document.getElementById("ctrAmount").value = jsonObj.ctrAmount[0]

    document.getElementById("typeOfTrade").value = "Spot"//jsonObj.typeOfTrade[0]

    document.getElementById("notes").value = jsonObj.notes[0]

    document.getElementById("isInverted").checked = jsonObj.isInverted[0] 
    document.getElementById("valueDate").valueAsDate = new Date();

    document.getElementById("TradeBookWindow").style.display = "block";
}

function populateHelpCommands(tradeData){
    console.log("Inside populateHelpCommands")
    const jsonObj = JSON.parse(tradeData)    
    document.getElementById("tradeBookingCmd").value = jsonObj.tradeBookingCmd[0] 
    // document.getElementById("tradeBookingSpeech").value = jsonObj.tradeBookingSpeech[0]    
    // document.getElementById("tradeEnquiryCmd").value = jsonObj.tradeEnquiryCmd[0]
    // document.getElementById("tradeEnquirySpeech").value = jsonObj.tradeEnquirySpeech[0]   
}

function call_Back(output){  
    document.getElementById("result").value = output
    if(output != "error" && output != "FAILED"){
        eel.processCommand(output)    
    }else{
        displayMessage("Something went wrong!!"); 
    }
    displayClickIcon()   
}

function submitTradeCallback(output){  
    displayResult(output)
    displayClickIcon()   
}

function getNDFTradeDataCallback(tradeDataList){  
    const tableId = document.getElementById('TradeDataTable');
    tradeDataList.forEach((dataRow, trIndex) => {
        let newRow = tableId.insertRow(-1);
        newRow.insertCell(-1).innerHTML = trIndex+1;
        Object.keys(dataRow).forEach((dataCell, cellIndex) => {
          let newCell = newRow.insertCell(-1);             
          newCell.innerHTML =  tData[trIndex][dataCell];
        })
      })   
    displayClickIcon()   
}

function call_Back_rate(output){  
    displayResult(output)
    displayClickIcon()
}

function savePropCallback(output){
    displayResult(output)
}

eel.expose(displayMessage);
eel.expose(displayListeningIcon);
eel.expose(displayClickIcon);
eel.expose(displayResult);
eel.expose(populateTradeDetails);
eel.expose(displayAllInRate);
eel.expose(populateHelpCommands);
eel.expose(getLiveRate);
eel.expose(submitTrade);
eel.expose(displayNDFTableData);

function displayListeningIcon(){
    document.getElementById("micbutton").style.color="red"
}

function displayClickIcon(){
    document.getElementById("micbutton").style.color="white"    
}

function displayMessage(message){
    console.log("Inside display message !!! ")
    document.getElementById("result").innerHTML = message
}

function displayResult(message){
    document.getElementById("result").innerHTML = message
}

function getLiveRate(){
    const ccy = document.getElementById("ccy").value
    const ctr = document.getElementById("ctr").value
    eel.getLiveRate(ccy+" "+ctr)
}

function displayAllInRate(message){
    document.getElementById("rateResult").innerHTML = message
}
