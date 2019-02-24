var link = null;

function clickSet() {
  link = document.getElementById("youtube").value;
  link = link.substr(link.indexOf("v="), link.length - link.indexOf("v="));
  next = link.indexOf("&") < 0 ? link.length : link.indexOf("&");
  link = link.substr(0, next);
  link = link.substr(2, link.length - 2);
  var http = new XMLHttpRequest();
  var server = "/upload_video/" + link;
  http.open("POST", server, true);

  //Send the proper header information along with the request
  http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

  http.onreadystatechange = function() {
    //Call a function when the state changes.
    if (http.readyState == XMLHttpRequest.DONE && http.status == 200) {
    }
  };
  http.send(null);

  // generate and set new link
  var newLink = "https://www.youtube.com/embed/" + link + "?start=0";
  document.getElementById("video").src = newLink;
}

function clickSubmit() {
  document.getElementById("loader").hidden = false;
  document.getElementById("status").hidden = true;
  var http = new XMLHttpRequest();
  var caption = document.getElementById("caption").value;
  var server = "/get_time/" + link + "/" + caption;
  http.open("GET", server, true);

  http.onreadystatechange = function() {
    if (http.readyState == XMLHttpRequest.DONE && http.status == 200) {
      // move cursor right to that timestamp
      var jsonObj = JSON.parse(http.responseText);
      var newLink =
        "https://www.youtube.com/embed/" + link + "?start=" + jsonObj.timestamp;
      document.getElementById("video").src = newLink;
      document.getElementById("status").innerHTML = "Success";
      document.getElementById("status").style.color = "green";
    } else {
      document.getElementById("status").innerHTML = "Failed";
      document.getElementById("status").style.color = "red";
    }
    document.getElementById("loader").hidden = true;
    document.getElementById("status").hidden = false;
  };

  http.send(null);
}
