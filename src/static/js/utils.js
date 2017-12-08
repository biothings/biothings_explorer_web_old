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
var COMMENT_LINE = "###############\n"
var IMPORT_LINE = COMMENT_LINE + "#Import biothings_explorer python package\n" + COMMENT_LINE + "from biothings_explorer import BioThingsExplorer\n"
var INITIATE_LINE = COMMENT_LINE + "#Start biothings_explorer instance\n" + COMMENT_LINE + "t = BioThingsExplorer()\n"
var DEFINE_PATH_LINE = COMMENT_LINE + "#Here is the exploration path you select\n" + COMMENT_LINE + "PATH = path_list\n"
var DEFINE_INPUT_LINE = COMMENT_LINE + "#Here is the input you give\n" + COMMENT_LINE + "INPUT = input_value\n"
var EXPLORE_PATH_LINE = COMMENT_LINE + "#Here is the function to extract the output\n" + COMMENT_LINE + "output = t.find_output(t.path_conversion(PATH), INPUT, display_graph=False\n"
var FINAL_COMMENT = "#If you are using jupyter notebook, set display_graph to True\n#This will display the graph on the jupyter notebook cell\n#You can do further data analysis using output.edges(), output.nodes()\n"

    function dynamic_text(path, _input) {
	    var final_string = IMPORT_LINE + INITIATE_LINE + DEFINE_PATH_LINE.replace('path_list', JSON.stringify(path)) + DEFINE_INPUT_LINE.replace('input_value', _input) + EXPLORE_PATH_LINE + FINAL_COMMENT;
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