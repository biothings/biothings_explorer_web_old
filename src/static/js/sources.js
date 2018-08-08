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

$(document).ready(function(){
  fetch_apistatus().done(function(jsonResponse) {
    $('#example').DataTable( {
        data: jsonResponse,
        columns: [
            { title: "API" },
            { title: "Status" }
        ]
    });
  });
  fetch_databasestatus().done(function(jsonResponse) {
    $('#example1').DataTable( {
        data: jsonResponse,
        columns: [
            { title: "database name" },
            { title: "database version" },
            { title: "API" }
        ]
    });
  });
});