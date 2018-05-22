$(document).ready(function() {
    $("#path-plotly-div").hide();
	$(".search-bar-center").hide();
    $(".search-bar-top").hide();
    var elems = document.querySelectorAll('.sidenav');
	var instances = M.Sidenav.init(elems);
    var instance = M.Sidenav.getInstance($("#slide-out"));
	$("#menu").click(function(){
		instance.open();
	});
    populateSelectInSideBar()
    $(".try-explore-endpoint").click(function() {
        $(".main-menu").hide();
        $(".endpoint-search-bar").show();
        $(".endpoint-search-bar").addClass("search-bar-center");
        $(".endpoint-search-bar").removeClass("search-bar-top");
        $(".crawler-header").show();
        $("#path-plotly-div").hide();
    });
    $(".try-explore-input").click(function() {
        $(".main-menu").hide();
        //recenter the search bar and show header
        $(".input-search-bar").show();
        $(".input-search-bar").addClass("search-bar-center");
        $(".input-search-bar").removeClass("search-bar-top");
        $(".crawler-header").show();
        // hide the ploty graph display
        $("#path-plotly-div").hide();
    });
    $(".try-explore-output").click(function() {
        $(".main-menu").hide();
        //recenter the search bar and show header
        $(".output-search-bar").show();
        $(".output-search-bar").addClass("search-bar-center");
        $(".output-search-bar").removeClass("search-bar-top");
        $(".crawler-header").show();
        // hide the ploty graph display
        $("#path-plotly-div").hide();
    });
    $(".search-button").click(function() {
        $(".crawler-header").hide();
        $(".search-bar-center").addClass("search-bar-top");
        $(".search-bar-center").removeClass("search-bar-center");
        
    });
    //when user select a bioentity/endpoint, display the sankey plot 
    //related to the user request
    displaySankeyBasedOnUserSelect();
});