function drawCytoscape(target_div, _style, _layout, data){
	$("#cy").empty();
	Plotly.purge('plotly-div');
	$("#paths-list").empty();
    $("#cy").show();
    $("#plotly-div").hide();
	var cy = cytoscape({
		boxSelectionEnabled: false,
        autounselectify: true,
		container: $(target_div),
		layout: _layout,
		style: _style,
		elements: data
	});
	return cy;
}
