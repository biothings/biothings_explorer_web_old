/**
 * Get crawling results based on user input
 * @param {String} input_type
 * @param {String} input_value
 * @return {Promise} crawling results
*/
function fetch_crawler_results(prefix, input_value){
    var promise = $.ajax({
        type:"GET",
        url: "/explorer/api/v2/crawler",
        data: {input_type: prefix, input_value: input_value},
        datatype: "json"
    });
    return promise;
};

/**
 * Organize data to be compatible with dataTable
*/
function organize_api_output_to_fit_datatable(dataset) {
	var organized_dataset = [];
	dataset.forEach(function(element) {
		organized_element = [element.object.id, element.prefix, element.predicate, element.api];
		organized_dataset.push(organized_element);
	});
	return organized_dataset;
}

/**
 * calculate number of entries per semantic type
 * used in radar chart
*/
SEMANTIC_TYPE_LIST = ["gene", "transcript", "chemical", "pathway", "bioassay", 'disease', 'ontology'];
function count_entry_for_each_semantic_type(data) {
	counter = [];
	SEMANTIC_TYPE_LIST.forEach(function(semantic_type) {
		if (semantic_type in data) {
			counter.push(data[semantic_type].length);
		} else {
			counter.push(0);
		}
	});
	return counter;
}
/**
 * Given prefix and input_value, display the results
*/
function update_data_display(prefix, input_value) {
    fetch_crawler_results(prefix, input_value).done(function(jsonResponse) {
    	var counter = count_entry_for_each_semantic_type(jsonResponse['linkedData']);
        // remove loading status
        console.log(counter);
        var myConfig = {
		    "type": "radar",
		    "series": [{
		        "values": counter
		    }],
		    "scale-k": {
    			"labels": SEMANTIC_TYPE_LIST}
		};
		 
		zingchart.render({ 
			id : 'radar_chart', 
			data : myConfig, 
			height: '100%', 
			width: '100%' 
		});
        $(".overlay-group").hide();
        // show div for data display
        $(".main").show();
        for (var semantic_type in jsonResponse['linkedData']) {
    		fill_data_for_single_semantic_type(semantic_type.toUpperCase(), organize_api_output_to_fit_datatable(jsonResponse['linkedData'][semantic_type]), ['id', 'prefix', 'predicate', 'api']);
    	};
	});
};


/**
 * Create a datatable by utilizing the div id, data, column name
 * specified by the user
*/
function create_data_table(div_id, dataset, column_names) {
	var columns_dict = column_names.map(x => {return {'title': x}});
	$("#" + div_id).DataTable( {
		data: dataset,
		columns: columns_dict
	});
};

/**
 * Create a collapsible element for each semantic type
*/
function create_collapsible_for_single_semantic_type(semantic_type) {
    var collapsible_header_template = '<li><div class="collapsible-header">{semantic_type}</div>';
    var collapsible_body = '<div class="collapsible-body"><table id=' + semantic_type + ' class="display" width="100%"></table>';
    return collapsible_header_template.replace('{semantic_type}', semantic_type) + collapsible_body + '</div></li>'
};

/**
 * Create a data block for semantic type info
*/
function fill_data_for_single_semantic_type(semantic_type, dataset, column_names) {
    $(".data-display-list").append(create_collapsible_for_single_semantic_type(semantic_type));
    $(".collapsible").collapsible();
    create_data_table(semantic_type, dataset, column_names);
};

$(document).ready(function(){
    $(".dropdown-trigger").dropdown();
    populateCrawlerInput('#select-input');
    $('#start-crawl-button').click(function() {
        $("#navbar").css({'position': 'relative'});
        $(".crawler_header").hide();
        $(".overlay-group").show();
        $(".search-bar-center").removeClass("search-bar-center");
        $(".search-history").show();
        var prefix = $("#select-input").find("option:selected").attr('value');
        var input_value = $("#crawler-input-value").val();
        update_data_display(prefix, input_value);
        $(".collapsible").collapsible();
    });
});