$(function(){
	//by default, when user opens the biothings explorer, 
	//the overview of api road map will be displayed
	drawSemanticMap();
	drawIdLevelMap();
	drawApiLevelMap();
	drawColorSchema()
	//var cy = drawCytoscape("#cy", concentric_style, concentricOptions, [{"group": "nodes", "data": {'id': "NCBIGENE", "type": "value", "level": 0}}]);
	//temparorily hide explore_path section, this section will only be shown
	//after the user has specified the path
	$("#explore-path").hide();
	$("#explore-customize-path").hide();
	//Display api_road_map when 'roadmapbutton' is clicked
	$("#roadMapButton").click(function() {
		$("#path-plotly-div").hide();
		$("#path-plotly-div").hide();
		$("#explore-plotly-div").hide();
		$("#cy").hide();
		$(".overview_map").show();
	});
	//populate the sidebar, fill in endpoint and bioentity names to 'select'
	populateSelectInSideBar();
	//when user select a bioentity/endpoint, display the sankey plot 
	//related to the user request
	displaySankeyBasedOnUserSelect();
	//when user select the path connecting input/output, and provide the input value
	//display the cytoscape graph linking input and output
	$("#explorePathButton").click(function() {
		if ($("#select-path").find("option:selected").attr("value") == 'all') {
			displayOutputFromAllPaths();
		} else {
			var path = getPath();
			displayOutputToCytoscape(path[0], path[1]);
		}
	});
	//detect changes in the customize path options
	changeCustomizeOption();
	displayCustomizedOutput();
});


