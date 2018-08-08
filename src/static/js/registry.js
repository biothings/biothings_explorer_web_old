function fetch_registry(){
  var promise = $.ajax({
      type:"GET",
      url: "/explorer/api/v2/registry",
      datatype: "json"
  });
  return promise;
};


$(document).ready(function(){
  fetch_registry().done(function(jsonResponse) {
    $('#registry').DataTable( {
        data: jsonResponse,
        "bLengthChange": false,
        "bFilter": true,
        "bInfo": false,
        columns: [
            { title: "Prefix" },
            { title: "URI" },
            { title: "Description" },
            { title: "Semantic Type" }
        ]
    });
  });
  $(".dropdown-trigger").dropdown();
});
