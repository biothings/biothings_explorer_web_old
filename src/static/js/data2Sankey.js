/**
 * Display Sankey Plot for the selected Input
 * @return {Sankey Plot}
*/
function displayInput() {
	$("#input-search-button").click(function(){
		_input = $("#select-input").find("option:selected").attr('value');
		findOutputTypeBasedOnInputType(_input).done(function(jsonResponse){
	    	drawSankeyPlot(jsonResponse, type='path');
            $("#DownloadCodeButton").show();
            $("#DownloadCodeButton").click(function() {
                download_file('bt_explorer_code_input.py', construct_input_text(_input), 'text/plain');
            });
		}).catch(function (err) {
            $("#DownloadCodeButton").hide();
            Plotly.purge('path-plotly');
            $("#path-plotly-div").show();
            $("#error-message").html('<h2 class="center">' + err.responseJSON['error message'].replace('\n', '<br />') + '</h2>')
        });
	});
};

/**
 * Display Sankey Plot for the selected Output
 * @return {Sankey Plot}
*/
function displayOutput() {
    $("#output-search-button").click(function(){
        _output = $("#select-output").find("option:selected").attr('value');
        findInputTypeBasedOnOutputType(_output).done(function(jsonResponse){
            $("#DownloadCodeButton").show();
            $("#DownloadCodeButton").click(function() {
                download_file('bt_explorer_code_output.py', construct_output_text(_output), 'text/plain');
            });
            drawSankeyPlot(jsonResponse, type='path');
        }).catch(function (err) {
            $("#DownloadCodeButton").hide();
            Plotly.purge('path-plotly');
            $("#path-plotly-div").show();
            $("#error-message").html('<h2 class="center">' + err.responseJSON['error message'].replace('\n', '<br />') + '</h2>')
        });
    });
};

/**
 * Display Sankey Plot for the selected Endpoint
 * @return {Sankey Plot}
*/
function displayEndpoint() {
    $("#endpoint-search-button").click(function(){
        _endpoint = $("#select-endpoint").find("option:selected").attr('value');
        findInputOutputBasedOnEndpoint(_endpoint).done(function(jsonResponse){
            $("#DownloadCodeButton").show();
            $("#DownloadCodeButton").click(function() {
                download_file('bt_explorer_code_endpoint.py', construct_endpoint_text(_endpoint), 'text/plain');
            });
            drawSankeyPlot(jsonResponse, type='path');
        }).catch(function (err) {
            $("#DownloadCodeButton").hide();
            Plotly.purge('path-plotly');
            $("#path-plotly-div").show();
            $("#error-message").html('<h2 class="center">' + err.responseJSON['error message'].replace('\n', '<br />') + '</h2>')
        });
    });
};

/**
 * Display Sankey Plot for the selected input semantic types and output semantic types
 * @return {Sankey Plot}
*/
function displaySemanticType() {
    $("#semantic-search-button").click(function(){
        _input = $("#select-semantic-input").find("option:selected").attr('value');
        _output = $("#select-semantic-output").find("option:selected").attr('value');
        findPathBetweenTwoSemanticTypes(_input, _output).done(function(jsonResponse){
            drawSankeyPlot(jsonResponse, type='path');
            $("#DownloadCodeButton").show();
            $("#DownloadCodeButton").click(function() {
                download_file('bt_explorer_code_semantic_connect.py', construct_semantic_connect_text(_input, _output), 'text/plain');
            });
        }).catch(function (err) {
            $("#DownloadCodeButton").hide();
            Plotly.purge('path-plotly');
            $("#path-plotly-div").show();
            $("#error-message").html('<h2 class="center">' + err.responseJSON['error message'].replace('\n', '<br />') + '</h2>')
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
            drawSankeyPlot(jsonResponse, type="explore");
            CURRENT_PATHS = jsonResponse['paths'];
            $("#export-python").append(dynamic_text(_input, _output));
            draw_hierarchical_path(CURRENT_PATHS);
            populatePath("#select-path", CURRENT_PATHS);
        });
    });
};


function displaySankeyBasedOnUserSelect(){
    displayInput();
    displayOutput();
    displayEndpoint();
    displayPathsBetweenInputOutput();
    displaySemanticType();
}
