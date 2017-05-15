// If dialog box is disabled.
function confirm_download_csv(arrData, ReportTitle) {
    var open_time = new Date();
    var result = confirm("there are " + arrData.length + " data to be converted to .csv\nexpect processing time");
    var close_time = new Date();

    if (close_time - open_time < 10) {
        JSONToCSVConverterProcess(arrData, ReportTitle);
    } else {
        if (result) { JSONToCSVConverterProcess(arrData, ReportTitle); }
    }
}
function isInArray(value, array) {
  return array.indexOf(value) > -1;
}
function JSONPrint(JSONData, ReportTitle) {
    //Generate a file name
    var fileName = "pedge_";
    //this will remove the blank-spaces from the title and replace it with an underscore
    fileName += ReportTitle.replace(/ /g,"_");

    //Initialize file format you want csv or xls
    var uri = 'data:text/json;charset=utf-8,' + escape(JSONData);

    // Now the little tricky part.
    // you can use either>> window.open(uri);
    // but this will not work in some browsers
    // or you will not get the correct file extension

    //this trick will generate a temp <a /> tag
    var link = document.createElement("a");
    link.href = uri;

    //set the visibility hidden so it will not effect on your web-layout
    link.style = "visibility:hidden";
    link.download = fileName + ".json";

    //this part will append the anchor tag and remove it after automatic click
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
function JSONToCSVConverter(JSONData, ReportTitle) {
    //If JSONData is not an object then JSON.parse will parse the JSON string in an Object
    var arrData = typeof JSONData != 'object' ? JSON.parse(JSONData) : JSONData;

    if (arrData.length >= 500) { confirm_download_csv(arrData, ReportTitle); }
    else { JSONToCSVConverterProcess(arrData, ReportTitle); }
}
function JSONToCSVConverterProcess(arrData, ReportTitle){
    var CSV = '';
    //Set Report title in first row or line

    CSV += ReportTitle + '\r\n\n';

    var array_header = [];
    var row = "";
    for (var i = 0; i < arrData.length; i ++) {
        for (var j in arrData[i]){
            if (!isInArray(j, array_header)) {
                array_header.push(j);
                row += j + ',';
            }
        }
    }
    row = row.slice(0, -1);
    CSV += row + '\r\n';
    for (var i = 0; i < arrData.length; i ++) {
        var row = "";
        for (var j = 0; j < array_header.length; j ++) {
            if (arrData[i].hasOwnProperty(array_header[j])) {
                row += '"' + arrData[i][array_header[j]] + '",';
            }
            else {
                row += '"None",';
            }
        }
        row.slice(0, row.length - 1);
        CSV += row + '\r\n';
    }

    if (CSV == '') {
        alert("invalid data");
        return;
    }

    //Generate a file name
    var fileName = "pedge_";
    //this will remove the blank-spaces from the title and replace it with an underscore
    fileName += ReportTitle.replace(/ /g,"_");

    //Initialize file format you want csv or xls
    var uri = 'data:text/csv;charset=utf-8,' + escape(CSV);

    // Now the little tricky part.
    // you can use either>> window.open(uri);
    // but this will not work in some browsers
    // or you will not get the correct file extension

    //this trick will generate a temp <a /> tag
    var link = document.createElement("a");
    link.href = uri;

    //set the visibility hidden so it will not effect on your web-layout
    link.style = "visibility:hidden";
    link.download = fileName + ".csv";

    //this part will append the anchor tag and remove it after automatic click
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}