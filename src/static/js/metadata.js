$(document).ready(function() {
    $(".dropdown-trigger").dropdown();
    $("#path-plotly-div").hide();
	$(".search-bar-center").hide();
    $(".search-bar-top").hide();
    $('.tooltipped').tooltip();
    $("#DownloadCodeButton").hide();
    var elems = document.querySelectorAll('.sidenav');
	var instances = M.Sidenav.init(elems);
    var instance = M.Sidenav.getInstance($("#slide-out"));
	$("#menu").click(function(){
		instance.open();
	});
    populateSelectInSideBar();
    $(".try-explore-endpoint").click(function() {
        $(".search-bar").hide();
        $("#main-menu").hide();
        $(".landing-page").hide();
        $(".page-footer").hide();
        $(".endpoint-search-bar").show();
        $(".endpoint-search-bar").addClass("search-bar-center");
        $(".endpoint-search-bar").removeClass("search-bar-top");
        $(".crawler-header").show();
        $("#path-plotly-div").hide();
    });
    $(".try-explore-input").click(function() {
        $(".search-bar").hide();
        $("#main-menu").hide();
        $(".landing-page").hide();
        $(".page-footer").hide();
        //recenter the search bar and show header
        $(".input-search-bar").show();
        $(".input-search-bar").addClass("search-bar-center");
        $(".input-search-bar").removeClass("search-bar-top");
        $(".crawler-header").show();
        // hide the ploty graph display
        $("#path-plotly-div").hide();
    });
    $(".try-explore-output").click(function() {
        $(".search-bar").hide();
        $("#main-menu").hide();
        $(".landing-page").hide();
        $(".page-footer").hide();
        //recenter the search bar and show header
        $(".output-search-bar").show();
        $(".output-search-bar").addClass("search-bar-center");
        $(".output-search-bar").removeClass("search-bar-top");
        $(".crawler-header").show();
        // hide the ploty graph display
        $("#path-plotly-div").hide();
    });
    $(".try-explore-semantic").click(function() {
        $(".search-bar").hide();
        $("#main-menu").hide();
        $(".landing-page").hide();
        $(".page-footer").hide();
        $(".query_example").hide();
        //recenter the search bar and show header
        $(".semantic-search-bar").show();
        $(".semantic-search-bar").addClass("search-bar-center");
        $(".semantic-search-bar").removeClass("search-bar-top");
        $(".crawler-header").show();
        // hide the ploty graph display
        $("#path-plotly-div").hide();
    });

    //the following section of code provides examples
    // of how to connect from gene to chemical
    $("#g2c_example").click(function() {
        $("#select-semantic-input").val('gene'); // Select the option with a value of 'gene'
        $('#select-semantic-input').trigger('change'); 
        $("#select-semantic-output").val('chemical'); // Select the option with a value of 'gene'
        $('#select-semantic-output').trigger('change');
    });

    //the following section of code provides examples
    // of how to connect from disease to gene
    $("#d2g_example").click(function() {
        $("#select-semantic-input").val('disease'); // Select the option with a value of 'gene'
        $('#select-semantic-input').trigger('change'); 
        $("#select-semantic-output").val('gene'); // Select the option with a value of 'gene'
        $('#select-semantic-output').trigger('change');
    });

    $(".search-button").click(function() {
        $(".crawler-header").hide();
        $(".search-bar-center").addClass("search-bar-top");
        $(".search-bar-center").removeClass("search-bar-center");
        
    });

    //when user select a bioentity/endpoint, display the sankey plot 
    //related to the user request
    displaySankeyBasedOnUserSelect();
    $("#metadata-header").click(function() {
        $("#DownloadCodeButton").hide();
        $(".landing-page").show();
        $("#main-menu").show();
        $(".page-footer").show();
        $(".search-bar-top").addClass("search-bar-center");
        $(".search-bar-center").removeClass("search-bar-top");
        $(".search-bar-center").hide();
        $("#path-plotly-div").hide();
    })
});