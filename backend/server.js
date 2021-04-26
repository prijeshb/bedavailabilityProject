const express = require("express");
const cors = require("cors");
const app = express();
const fs = require('fs');
const path = require('path');

process.env.TZ = 'Asia/Calcutta';
(new Date().toString())
app.use(cors())

app.get("/",(req,res) => {
    res.json({jsodn:"Hey there !!🥱"})
})
const convertToFormattedDigit  = (value) => {
    let tempValue = null;
    let prefix = "0";
    if(!value)
        throw Error("Passed value for formatting is undefined ");
    
    if(value.toString().length < 2 ){
        tempValue = value
        tempValue = prefix + value;
        value = tempValue;
    }
    return value;
}
const getFormattedDateTimeValue = (currDateTime) => {
    let formattedHr = currDateTime.getHours().toString().length < 2 ? convertToFormattedDigit(currDateTime.getHours()) : currDateTime.getHours();
    let formattedDate = currDateTime.getDate().toString().length < 2 ? convertToFormattedDigit(currDateTime.getDate()) : currDateTime.getDate();
    let formattedMont = currDateTime.getMonth().toString().length < 2 ? convertToFormattedDigit(currDateTime.getMonth()+1) : currDateTime.getMonth()+1;
    return {formattedDate,formattedMont,formattedHr}
}
const getFileStringForCurrTime = () => {
    let currDateTime = new Date();
    let fileString = '';
    let filePath = '';
    let osPath = path.sep;
    let dataPath = '';
    let { formattedDate, formattedMont, formattedHr } = getFormattedDateTimeValue(currDateTime)
    let currMin = currDateTime.getMinutes();
    // if( 0 <= currMin  < 15)
    //     fileString = `${formattedDate}${formattedMont}${currDateTime.getFullYear()}${formattedHr}00.json`
    // else if( 15 <= currMin < 30)
    //     fileString = `${formattedDate}${formattedMont}${currDateTime.getFullYear()}${formattedHr}15.json`
    // else if( 30 <= currMin < 45)
    //     fileString = `${formattedDate}${formattedMont}${currDateTime.getFullYear()}${formattedHr}30.json`   
    // else if (45 <= currMin < 59)
    //     fileString = `${formattedDate}${formattedMont}${currDateTime.getFullYear()}${formattedHr}45.json`
        
    fileString = `${formattedDate}${formattedMont}${currDateTime.getFullYear()}${formattedHr}.json`
    filePath = `${currDateTime.getFullYear()}${osPath}${formattedMont}${osPath}${formattedDate}${osPath}`;
    dataPath = `${osPath}data${osPath}` + filePath + fileString
    return dataPath;
}
app.get("/availableBeds",(req,res) => {
    let path = getFileStringForCurrTime();
    if(!path)
        path = `${osPath}data${osPath}`+  `default${path.sep}` + "default.json"
    fs.readFile(`.${path}`,(err,data) => {
        if(err) throw err
        res.json(JSON.parse(data));
    })
})


app.listen(process.env.PORT || 8090,()=>{
    console.log('Listening on port 8090')
})