class TradeObject {
    constructor(custName , buySellIndicator, ccy, ctr, allInRate, isInverted, valueDate, ccyAmount,ctrAmount,notes,typeOfTrade, isNDF,fixingDate, fixingStatus ) {
        this.custName = custName;
        this.buySellIndicator = buySellIndicator;
        this.isInverted = isInverted;
        this.ccy = ccy;
        this.ctr = ctr;
        this.allInRate = allInRate;
        this.valueDate = valueDate;
        this.ccyAmount = ccyAmount;
        this.ctrAmount = ctrAmount;
        this.notes = notes;
        this.typeOfTrade = typeOfTrade;
        this.isNDF = isNDF;
        this.fixingDate = fixingDate;
        this.fixingStatus = fixingStatus;
    }
}

export {TradeObject}
