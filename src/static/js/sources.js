function fetch_apistatus(){
  var promise = $.ajax({
      type:"GET",
      url: "/explorer/api/v2/apistatus",
      data: {"format": "1"},
      datatype: "json"
  });
  return promise;
};

function fetch_databasestatus(){
  var promise = $.ajax({
      type:"GET",
      url: "/explorer/api/v2/databasestatus",
      data: {"format": "1"},
      datatype: "json"
  });
  return promise;
};

function responsiveNav() {
    var x = document.getElementById("myTopnav");
    if (x.className === "topnav") {
        x.className += " responsive";
    } else {
        x.className = "topnav";
    }
};

$(document).ready(function(){
  fetch_apistatus().done(function(jsonResponse) {
    $('#apitable').DataTable( {
        data: jsonResponse,
        "bLengthChange": false,
        "bFilter": true,
        "bInfo": false,
        columns: [
            { title: "API" },
            { title: "Status" }
        ]
    });
  });
  fetch_databasestatus().done(function(jsonResponse) {
    $('#databasetable').DataTable( {
        data: jsonResponse,
        "bLengthChange": false,
        "bFilter": true,
        "bInfo": false,
        columns: [
            { title: "database name" },
            { title: "database version" },
            { title: "API" }
        ]
    });
  });
  $('.scrollspy').scrollSpy();
  $(".dropdown-trigger").dropdown();

});
