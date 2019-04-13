function load_json(url_of_json,div_to_be_display){
  var url = url_of_json;
  var xmlhttp;
  if(window.XMLHttpRequest){
    xmlhttp=new XMLHttpRequest();
  }else {
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
  xmlhttp.onreadystatechange=function(){
    if(xmlhttp.readyState==4&&xmlhttp.status==200){
      var data=xmlhttp.responseText;
      dataObj=JSON.parse(data);
      for (var objs in dataObj) {
        var trs = document.createElement("tr");
        document.getElementById("tabs").appendChild(trs);
        trs.innerHTML = "<tr><th>"+ objs +"</th>"+"<td>"+ dataObj[objs] +"</td></tr>";
      }
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
  var tds = document.getElementsByTagName("td");
  for(var i=0;i<ths.length;i++){
    jobNew[ths[i].innerText] = tds[i].innerText;
  }
  put_json(url, jobNew);
}
function div1(){
  var url_of_json = "a.json";
  load_json(url_of_json);
}
