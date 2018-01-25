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
var COMMENT_LINE = "<br>################################################<br>"
var IMPORT_LINE = COMMENT_LINE + "<p>#Import biothings_explorer python package</p>" + COMMENT_LINE + "<p style='color:blue;'>from biothings_explorer import BioThingsExplorer</p>"
var INITIATE_LINE = COMMENT_LINE + "#Start biothings_explorer instance" + COMMENT_LINE + "<p style='color:blue;'>t = BioThingsExplorer()</p>"
var DEFINE_PATH_LINE = COMMENT_LINE + "#Your exploration starts from input_id to output_id" + COMMENT_LINE 
var FIND_PATH_LINE = "<p style='color:blue;'>paths = t.find_path(start=input_id, end=output_id)</p>"
var DEFINE_INPUT_LINE = COMMENT_LINE + "#Here is the input you give<br><br>" + COMMENT_LINE + "INPUT = input_value<br><br>"
var EXPLORE_PATH_LINE = COMMENT_LINE + "#Here is the function to extract the output<br><br>" + COMMENT_LINE + "output = t.find_output(t.path_conversion(PATH), INPUT, display_graph=False<br><br>"
var FINAL_COMMENT = "#If you are using jupyter notebook, set display_graph to True<br>#This will display the graph on the jupyter notebook cell<br><br>#You can do further data analysis using output.edges(), output.nodes()<br></p>"

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