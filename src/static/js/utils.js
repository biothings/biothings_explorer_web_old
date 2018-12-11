function download(cy) {
	$("#DownloadPNGButton").click(function(){
        var a = document.createElement('a');
        a.href = cy.png();
        a.download = 'api_map.png';
        a.click();
    });
    $("#DownloadJSONButton").click(function() {
    	var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(cy.json()));
		var dlAnchorElem = document.getElementById('downloadAnchorElem');
		dlAnchorElem.setAttribute("href",     dataStr     );
		dlAnchorElem.setAttribute("download", "biothings_explorer_data.json");
		dlAnchorElem.click();
	$("#DownloadCodeButton").click(function() {
		var path = ['ncbigene', 'http://mygene.info/v3/gene/{geneid}', 'hgnc.symbol']
		download_file('my_file.py', dynamic_text(path, '1017'), 'text/plain');
	})
    })
}
var COMMENT_LINE = "################################################################\n"
var REQUEST_LINE = "from __future__ import print_function\nimport requests\n"
var COMMENT_CALL_BIOTHINGS = "#Make API calls to BioThings Explorer\n"
var EXTRACT_JSON_LINE = "data = doc.json()\nprint(data)\n"
var COMMENT_EXTRACT_JSON = "#Extract JSON output\n"
var IMPORT_LINE = COMMENT_LINE + "<p>#Import biothings_explorer python package</p><p> You can download the python package using pip install biothings_explorer</p>" + COMMENT_LINE + "<p style='color:blue;'>from biothings_explorer import BioThingsExplorer</p>"
var INITIATE_LINE = COMMENT_LINE + "#Start biothings_explorer instance" + COMMENT_LINE + "<p style='color:blue;'>t = BioThingsExplorer()</p>"
var DEFINE_PATH_LINE = COMMENT_LINE + "#Your exploration starts from input_id to output_id" + COMMENT_LINE 
var FIND_PATH_LINE = "<p style='color:blue;'>paths = t.find_path(start=input_id, end=output_id)</p>"
var DEFINE_INPUT_LINE = COMMENT_LINE + "#Here is the input you give<br><br>" + COMMENT_LINE + "INPUT = input_value<br><br>"
var EXPLORE_PATH_LINE = COMMENT_LINE + "#Here is the function to extract the output<br><br>" + COMMENT_LINE + "output = t.find_output(t.path_conversion(PATH), INPUT, display_graph=False<br><br>"
var FINAL_COMMENT = "#If you are using jupyter notebook, set display_graph to True<br>#This will display the graph on the jupyter notebook cell<br><br>#You can do further data analysis using output.edges(), output.nodes()<br></p>"

function construct_input_text(_input) {
    var final_string = COMMENT_LINE + '#This code is for finding endpoints which take input "{input}"\n'.replace('{input}', _input) + COMMENT_LINE + REQUEST_LINE + COMMENT_CALL_BIOTHINGS
    var query = "doc = requests.get('http://biothings.io/explorer/api/v2/input', params={'input': '{input}'})\n"
    final_string += query.replace('{input}', _input)
    final_string += COMMENT_EXTRACT_JSON
    final_string += EXTRACT_JSON_LINE
    return final_string
};

function construct_output_text(_output) {
    var final_string = COMMENT_LINE + '#This code is for finding endpoints which have output "{output}"\n'.replace('{output}', _output) + COMMENT_LINE + REQUEST_LINE + COMMENT_CALL_BIOTHINGS
    var query = "doc = requests.get('http://biothings.io/explorer/api/v2/output', params={'output': '{output}'})\n"
    final_string += query.replace('{output}', _output)
    final_string += COMMENT_EXTRACT_JSON
    final_string += EXTRACT_JSON_LINE
    return final_string
};

function construct_endpoint_text(_endpoint) {
    var final_string = COMMENT_LINE + '#This code is for finding the inputs and outputs of endpoint "{endpoint}"\n'.replace('{endpoint}', _endpoint) + COMMENT_LINE + REQUEST_LINE + COMMENT_CALL_BIOTHINGS
    var query = "doc = requests.get('http://biothings.io/explorer/api/v2/endpoint', params={'endpoint': '{endpoint}'})\n"
    final_string += query.replace('{endpoint}', _endpoint)
    final_string += COMMENT_EXTRACT_JSON
    final_string += EXTRACT_JSON_LINE
    return final_string
};

function construct_semantic_connect_text(_input, _output) {
    var final_string = COMMENT_LINE + '#This code is for finding the endpoints which can connect from input "{input}" to output "{output}"\n'.replace('{input}', _input).replace('{output}', _output) + COMMENT_LINE + REQUEST_LINE + COMMENT_CALL_BIOTHINGS
    var query = "doc = requests.get('http://biothings.io/explorer/api/v2/connectsemantictype', params={'input': '{input}', 'output': '{output}'})\n"
    final_string += query.replace('{input}', _input).replace('{output}', _output)
    final_string += COMMENT_EXTRACT_JSON
    final_string += EXTRACT_JSON_LINE
    return final_string
};

function construct_id_connect_text(_input, _output, max_api) {
    var final_string = COMMENT_LINE + '#This code is for finding the endpoints which can connect from input "{input}" to output "{output}"\n'.replace('{input}', _input).replace('{output}', _output) + COMMENT_LINE + REQUEST_LINE + COMMENT_CALL_BIOTHINGS
    var query = "doc = requests.get('http://biothings.io/explorer/api/v2/findpath', params={'input': '{input}', 'output': '{output}', 'max_api': '{max_api}''})\n"
    final_string += query.replace('{input}', _input).replace('{output}', _output).replace('{max_api}', max_api)
    final_string += COMMENT_EXTRACT_JSON
    final_string += EXTRACT_JSON_LINE
    return final_string
};

function construct_directinput2output_text(_input, _value, _output) {
    var final_string = COMMENT_LINE + '#This code is for finding the output "{output}" which can be connected from {input}:{input_value}\n'.replace('{input}', _input).replace('{output}', _output).replace('{input_value', _value) + COMMENT_LINE + REQUEST_LINE + COMMENT_CALL_BIOTHINGS
    var query = "doc = requests.get('http://biothings.io/explorer/api/v2/directinput2output', params={'input_prefix': '{input}', 'output_prefix': '{output}', 'input_value': '{input_value}'})\n"
    final_string += query.replace('{input}', _input).replace('{input}', _input).replace('{output}', _output).replace('{input_value}', _value)
    final_string += COMMENT_EXTRACT_JSON
    final_string += EXTRACT_JSON_LINE
    return final_string
};

function construct_semanticinput2output_text(_input, _value, _output) {
    var final_string = COMMENT_LINE + '#This code is for finding the output "{output}" which can be connected from {input}:{input_value} through semantic aligning results from multiple APIs\n'.replace('{input}', _input).replace('{output}', _output).replace('{input_value', _value) + COMMENT_LINE + REQUEST_LINE + COMMENT_CALL_BIOTHINGS
    var query = "doc = requests.get('http://biothings.io/explorer/api/v2/semanticquery', params={'input_prefix': '{input}', 'output_prefix': '{output}', 'input_value': '{input_value}'})\n"
    final_string += query.replace('{input}', _input).replace('{input}', _input).replace('{output}', _output).replace('{input_value}', _value)
    final_string += COMMENT_EXTRACT_JSON
    final_string += EXTRACT_JSON_LINE
    return final_string
};

    function dynamic_text(_input, _output) {
	    var final_string = IMPORT_LINE + INITIATE_LINE + DEFINE_PATH_LINE.replace('input_id', _input).replace('output_id', _output) + FIND_PATH_LINE.replace('input_id', _input).replace('output_id', _output);
	    console.log(final_string);
        return final_string;
    }

    function download_file(name, contents, mime_type) {
        mime_type = mime_type || "text/plain";

        var blob = new Blob([contents], {type: mime_type});

        var dlink = document.createElement('a');
        dlink.download = name;
        dlink.href = window.URL.createObjectURL(blob);
        dlink.onclick = function(e) {
            // revokeObjectURL needs a delay to work properly
            var that = this;
            setTimeout(function() {
                window.URL.revokeObjectURL(that.href);
            }, 1500);
        };

        dlink.click();
        dlink.remove();
    }