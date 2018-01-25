/**
 * Display Sankey Plot for the selected Input
 * @return {Sankey Plot}
*/
function displayInput() {
	$("#select-input").change(function(){
		_input = $(this).find("option:selected").attr('value');
		findOutputTypeBasedOnInputType(_input).done(function(jsonResponse){
	    	drawSankeyPlot(jsonResponse);
		});
	});
};

/**
 * Display Sankey Plot for the selected Output
 * @return {Sankey Plot}
*/
function displayOutput() {
    $("#select-output").change(function(){
        _output = $(this).find("option:selected").attr('value');
        findInputTypeBasedOnOutputType(_output).done(function(jsonResponse){
            drawSankeyPlot(jsonResponse);
        });
    });
};

/**
 * Display Sankey Plot for the selected Endpoint
 * @return {Sankey Plot}
*/
function displayEndpoint() {
    $("#select-endpoint").change(function(){
        _endpoint = $(this).find("option:selected").attr('value');
        console.log(_endpoint);
        findInputOutputBasedOnEndpoint(_endpoint).done(function(jsonResponse){
            drawSankeyPlot(jsonResponse);
        });
    });
};


/**
 * Display Sankey Plot for the Paths Connecting Input and Output
 * @return {Sankey Plot}
*/
function displayPathsBetweenInputOutput() {
    $("#inputOutputPathButton").click(function(){
        var _input = $("#select-input1").find("option:selected").attr('value');
        var _output = $("#select-output1").find("option:selected").attr('value');
        var max_api = $("#select-max-api").find("option:selected").attr('value');
        findStartEndConnection(_input, _output, max_api).done(function(jsonResponse){
            var parsedJson = $.parseJSON(jsonResponse);
            drawSankeyPlot(parsedJson);
            var paths = parsedJson['paths'];
            populatePath("#select-path", paths);
            $("#explore-path").show();
            $("#paths").show();
            $("#paths-list").append('<li class="collection-header"><h4>' + 'Path(s) Connecting from ' + _input + ' to ' + _output + '</h4></li>')
            $.each(paths, function(index, value) {
                $("#paths-list").append('<li class="collection-item">' + 'Path' + index + ': ' + value.join(' -> ') + '</li>')
            });
        });
    });
};


function displaySankeyBasedOnUserSelect(){
    displayInput();
    displayOutput();
    displayEndpoint();
    displayPathsBetweenInputOutput();
}
