$(function(){
    //initialize the floating action button
    $('.tooltipped').tooltip();
    $(".tabs").tabs();
    var elems = document.querySelectorAll('.fixed-action-btn');
    var instances = M.FloatingActionButton.init(elems, {
        direction: 'left'
    });
    $('.dropdown-trigger').dropdown();
    hide_all_graph_div();
	$('.sidenav').sidenav();
    $('.collapsible').collapsible();
    //by default, when user opens the biothings explorer, 
    //the overview of api road map will be displayed
    //drawSemanticMap();
    //drawIdLevelMap();
    //drawApiLevelMap();
    //drawColorSchema();
    
    //populate the sidebar, fill in endpoint and bioentity names to 'select'
    populateSelectInSideBar();
    //when user select a bioentity/endpoint, display the sankey plot 
    //related to the user request
    displaySankeyBasedOnUserSelect();
    DirectOutput2Graph();
    SemanticOutput2Graph();
});