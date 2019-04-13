/*
* volo.js: Simple javascript to demonstrate volo api.
* Author: harry.ma@dao-lab.com
*/

if (!(document.body || document.getElementsByTagName("body")[0])) {
    document.body = document.createElement("body");
}

if (!(document.head || document.getElementsByTagName("head")[0])) {
    document.head = document.createElement("head");
}

if (!(document.title || document.getElementsByTagName("title")[0])) {
    document.title = "Volo Video Optimizer";
}

var css  = document.createElement('link');
css.rel  = "stylesheet";
css.type = "text/css";
css.href = "volo.css";
css.media = 'all';
document.head.appendChild(css);

var volo = document.createElement("div");
volo.id = "Volo";
document.body.appendChild(volo);

var formdiv = document.createElement("div");
formdiv.id = "formdiv"
document.body.appendChild(formdiv);

var JobsList = document.createElement("table");
JobsList.innerHTML = "<caption>Volo Cube Job Summary</caption>"
    + "<tr><th>Job Name</th><th>Last Update</th><th>Status</th>"
    + "<th>Speed</th><th>Bitrate</th><th>Run Time</th><th>Priview</th></tr>"
    + "<tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>"
    + "<tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>"
    + "<tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>"
    + "<tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>"
volo.appendChild(JobsList);

var formdivobj = document.getElementById("formdiv");

function loadJson(filename, callback=null, row=null) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            try {
                var obj = JSON.parse(this.responseText);
                if (obj && callback) {
                    callback(obj, row);
                }
            } catch(e) {}
        }
    };
    xhttp.open("GET", "api/"+filename, true);
    xhttp.send();
}

function showJobStatus(job, r) {
    JobsList.rows[r].cells[2].textContent = job.Status;
    JobsList.rows[r].cells[3].textContent = job.Info[0].ifps;
    JobsList.rows[r].cells[4].textContent = job.Info[0].ibitrate;
    JobsList.rows[r].cells[5].textContent = job.Info[0].out_time.split(".")[0];
    if (job.Thumbnail) {
    JobsList.rows[r].cells[6].innerHTML = "<img src=\"data:image/png;base64," + job.Thumbnail + "\"/>";
    }
    JobsList.rows[r].onclick=function(){
      console.log(JobsList.rows[r].cells[0].textContent);
      var filename = JobsList.rows[r].cells[0].textContent;
      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
          if (xhttp.readyState == 4 && xhttp.status == 200) {
              var dataobj = JSON.parse(xhttp.responseText);
              str = "";
              str +="<form style=\"clear:both;padding-top:30px;\">";
              str +="Service :" + "<input style=\"margin-left:85px;\" type=\"text\" id=\"Service\" value=\"" + dataobj["Service"] +"\">" + "</br>";
              str +="</br>";
              str +="Device :" + "<input style=\"margin-left:87px;\" type=\"text\" id=\"Device\" value=\"" + dataobj["Device"] +"\">" + "</br>";
              str +="</br>";
              str +="VideoSize :" + "<input style=\"margin-left:63px;\" type=\"text\" id=\"VideoSize\" value=\"" + dataobj["VideoSize"] +"\">" + "</br>";
              str +="</br>";
              str +="Source :" + "<input style=\"margin-left:85px;\" type=\"text\" id=\"Source\" value=\"" + dataobj["Source"] +"\">" + "</br>";
              str +="</br>";
              str +="Output :" + "<input style=\"margin-left:83px;\" type=\"text\" id=\"Output\" value=\"" + dataobj["Output"] +"\">" + "</br>";
              str +="</br>";
              str +="Loop :" + "<input style=\"margin-left:99px;\" type=\"text\" id=\"Loop\" value=\"" + dataobj["Loop"] +"\">" + "</br>";
              str +="</br>";
              str +="NbInfo :" + "<input style=\"margin-left:85px;\" type=\"text\" id=\"NbInfo\" value=\"" + dataobj["NbInfo"] +"\">" + "</br>";
              str +="</br>";
              str +="NbLog :" + "<input style=\"margin-left:85px;\" type=\"text\" id=\"NbLog\" value=\"" + dataobj["NbLog"] +"\">" + "</br>";
              str +="</br>";
              str +="MediaInfo :" + "<input style=\"margin-left:58px;\" type=\"text\" id=\"MediaInfo\" value=\"" + dataobj["MediaInfo"] +"\">" + "</br>";
              str +="</br>";
              str +="Thumbnail :" + "<input style=\"margin-left:55px;\" type=\"text\" id=\"Thumbnail\" value=\"" + dataobj["Thumbnail"] +"\">" + "</br>";
              str +="</br>";
              str +="UpdateTime :" + "<input style=\"margin-left:43px;\" type=\"text\" id=\"UpdateTime\" value=\"" + dataobj["UpdateTime"] +"\">" + "</br>";
              str +="</br>";
              str +="Version :" + "<input style=\"margin-left:78px;\" type=\"text\" id=\"Version\" value=\"" + dataobj["Version"] +"\">" + "</br>";
              str +="</br>";
              str +="<input style=\"margin-left:50px;\" type=\"submit\" id=\"send\" value=\"SEND\" onclick=\"putajax()\" />";
              str +="<input style=\"margin-left:50px;\" type=\"reset\" id=\"reset\" value=\"RESET\" />";
              str +="</br>";
              str +="</form>";
              formdivobj.innerHTML = str;
          }
      };
      xhttp.open("GET", "/"+filename, true);
      xhttp.send();
    }
}

function putajax(){
  var xmlhttp = new XMLHttpRequest();
  var url="form.json";
  // var obj = new Array();
  var obj = {push:Array.prototype.push};
  var inputs = document.getElementsByTagName("input");
  for(var i=0;i<inputs.length-2;i++){
    obj.push(inputs[i].id+":"+inputs[i].value);
  }
  xmlhttp.open("PUT",url, true);
  xmlhttp.setRequestHeader("Content-Type","text/plain;charset=UTF-8");
  xmlhttp.send(JSON.stringify(obj));
  // readyState == 4 为请求完成，status == 200为请求陈宫返回的状态
  xmlhttp.onreadystatechange = function(){
      if(xmlhttp.readyState == 4 && xmlhttp.status == 200){
          console.log(xmlhttp.responseText);
      }
  }
}
function showJobsList(job, r) {
    JobsList.rows[r].cells[0].textContent = job.Job;
    JobsList.rows[r].cells[1].textContent = job.Timestamp;

    loadJson(job.Job+"/index.json", showJobStatus, r);
}

function update(job) {
    for(var i=0; i<job.length; i++) {
        loadJson(job[i].dir+"/idx.json", showJobsList, i+1);
    }
}

loadJson("", update);
setInterval(function(){ loadJson("", update); }, 3000);
