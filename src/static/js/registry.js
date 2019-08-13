function fetch_registry(){
  var promise = $.ajax({
      type:"GET",
      url: "/explorer_beta/api/v2/registry",
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
}


$(document).ready(function(){
  fetch_registry().done(function(jsonResponse) {
    $('#registry').DataTable( {
        data: jsonResponse,
        "bLengthChange": false,
        "bFilter": true,
        "bInfo": false,
        columns: [
            { title: "Prefix" },
            { title: "Recommended Name"},
            { title: "URI" },
            { title: "Pattern" },
            { title: "Example" },
            { title: "Semantic Type" },
            { title: "Attribute Type" },
            { title: "Description" }
        ]
    });
  });
  $(".dropdown-trigger").dropdown();
});
