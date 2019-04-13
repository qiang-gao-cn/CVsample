function load_json(url_of_json,callback=null,obj){
  var url = url_of_json;
  var xmlhttp;
  if(window.XMLHttpRequest){
    xmlhttp=new XMLHttpRequest();
  }else {
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
  xmlhttp.onreadystatechange=function(){
    if(xmlhttp.readyState==4&&xmlhttp.status==200){
      try {
          var obj = JSON.parse(this.responseText);
          if (obj && callback) {
              callback(url,obj);
          }
      } catch(e) {}
    }
  }
  xmlhttp.open("GET",url,true);
  xmlhttp.send();
}
function put_json(url_of_json, jobNew){
  var xmlhttp = new XMLHttpRequest();
  var obj = {};
  for(var key in jobNew) obj[key] = jobNew[key];
  xmlhttp.open("PUT",url_of_json, true);
  xmlhttp.send(JSON.stringify(obj));
  xmlhttp.onreadystatechange = function(){
      if(xmlhttp.readyState == 4 && xmlhttp.status == 200){
          console.log(xmlhttp.responseText);
      }
  }
}
function save_json(url_of_json, obj_to_save) {
  var url="b.JSON";
  var jobNew = {};
  var ths = document.getElementsByTagName("th");
  var ipt = document.getElementsByTagName("input");
  for(var i=0;i<ths.length;i++){
    jobNew[ths[i].innerText] = ipt[i].value;
  }
  put_json(url, jobNew);
}
function div1(){
  var url_of_json = "a.json";
  load_json(url_of_json,createtables);
  var urls = "test.json";
  load_json(urls,createtables);
}
function createtables(url,obj){
  var len=0;
  for(var datas in obj){
    len++;
  }
  var divs = document.getElementById("divval");
  var tables = document.createElement("table");
  divs.appendChild(tables);
  for(var i=0;i<len;i++){
    var trs = document.createElement("tr");
    var ths = document.createElement("th");
    var tds = document.createElement("td");
    var ipts = document.createElement("input");
    tables.appendChild(trs);
    trs.appendChild(ths);
    trs.appendChild(tds);
    tds.appendChild(ipts);
  }
  var timer = setInterval(function(){ showvalue(obj); }, 1000);
}
function showvalue(obj){
  var lens = 0;
  for(var key in obj){
    lens++;
    var tabes = document.getElementsByTagName("table");
    tabes[0].childNodes[lens-1].childNodes[0].innerText = key;
    tabes[0].childNodes[lens-1].childNodes[1].childNodes[0].value = obj[key];
  }
}
