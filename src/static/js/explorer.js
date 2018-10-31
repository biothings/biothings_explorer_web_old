$(document).ready(function() {
    $(".dropdown-trigger").dropdown();
    //this section deals with the side nav
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems);
    var instance = M.Sidenav.getInstance($("#slide-out"));
    $("#menu").click(function(){
        instance.open();
    });
    //initialize, make the main graph section invisible
    $("#main").hide();
    $(".search-bar").hide();
    $("#DownloadCodeButton").hide();
    $('.tooltipped').tooltip();
    populateSelectInSideBar();
    DirectOutput2Graph();
    SemanticOutput2Graph();
    $(".try-explore-single-edge").click(function() {
        $("#DownloadCodeButton").hide();
        $(".intermediate-switch").hide();
        $(".search-bar-header").show();
        $("#main").hide();
        $(".search-bar").hide();
        $("#intro").hide();
        $(".landing-page").hide();
        $(".page-footer").hide();
        $(".single-edge-search-bar").show();
        $(".single-edge-search-bar").addClass("search-bar-center");
        $(".single-edge-search-bar").removeClass("search-bar-top");
        $(".crawler-header").show();
        $("#path-plotly-div").hide();
    });
    $(".try-explore-semantic").click(function() {
        $("#DownloadCodeButton").hide();
        $(".search-bar-header").show();
        $("#main").hide();
        $(".search-bar").hide();
        $("#intro").hide();
        $(".landing-page").hide();
        $(".page-footer").hide();
        //recenter the search bar and show header
        $(".semantic-search-bar").show();
        $(".semantic-search-bar").addClass("search-bar-center");
        $(".semantic-search-bar").removeClass("search-bar-top");
        $(".crawler-header").show();
        // hide the ploty graph display
        $("#path-plotly-div").hide();
    });

    //the following section of code provides examples
    // of how to connect from hgnc.symbol:CXCR4 to chembl.compound
    $("#g2c_nav_example").click(function() {
        $("#direct-input").val('hgnc.symbol'); // Select the option with a value of 'gene'
        $('#direct-input').trigger('change'); 
        $("#direct-output").val('chembl.compound'); // Select the option with a value of 'gene'
        $('#direct-output').trigger('change');
        $("#direct_input_value").val('CXCR4');
    });

    //the following section of code provides examples
    // of how to connect from chembl.compound:CHEMBL744 to hgnc.symbol
    $("#c2g_nav_example").click(function() {
        $("#direct-input").val('chembl.compound'); // Select the option with a value of 'gene'
        $('#direct-input').trigger('change'); 
        $("#direct-output").val('hgnc.symbol'); // Select the option with a value of 'gene'
        $('#direct-output').trigger('change');
        $("#direct_input_value").val('CHEMBL744');
    });

    //the following section of code provides examples
    // of how to connect from MONDO:0013632 to HP
    $("#d2p_nav_example").click(function() {
        $("#direct-input").val('mondo'); // Select the option with a value of 'gene'
        $('#direct-input').trigger('change'); 
        $("#direct-output").val('hp'); // Select the option with a value of 'gene'
        $('#direct-output').trigger('change');
        $("#direct_input_value").val('0013632');
    });

    $(".search-button").click(function() {
        $(".query_example").hide();
        $(".crawler-header").hide();
        $(".search-bar-center").addClass("search-bar-top");
        $(".search-bar-center").removeClass("search-bar-center");
        
    });
    //when user select a bioentity/endpoint, display the sankey plot 
    //related to the user request
    displaySankeyBasedOnUserSelect();
    $("#metadata-header").click(function() {
        $(".landing-page").show();
        $("#main-menu").show();
        $(".page-footer").show();
        $(".search-bar-top").addClass("search-bar-center");
        $(".search-bar-center").removeClass("search-bar-top");
        $(".search-bar-center").hide();
        $("#path-plotly-div").hide();
    })
});