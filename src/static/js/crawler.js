/**
 * Get crawling results based on user input
 * @param {String} input_type
 * @param {String} input_value
 * @return {Promise} crawling results
*/
function fetch_crawler_results(prefix, input_value){
    var promise = $.ajax({
        type:"GET",
        url: "/explorer/api/v1/crawler",
        data: {input_type: prefix, input_value: input_value},
        datatype: "json"
    });
    return promise;
};

/**
 * Create a new checkbox by name for the refine side bar
 * @param {String} name
 * @return {String} html for new checkbox
*/
function create_single_checkbox(name) {
    var template = '<p><label><input type="checkbox" class="filled-in" checked="checked" /><span>{input}</span></label></p>';
    return template.replace('{input}', name);
};

/**
 * Create a new filter group 
 * @param {String} semantic_type
 * @param {Object} summary
 * @return {String} html for new filter group
*/
function create_single_filter_group(semantic_type, summary) {
	var header_template = '<h5 class="green-text">{input}</h5>';
	var filter_group_html = '<div class="row filter-box">' + header_template.replace('{input}', semantic_type);
	summary['id'].forEach(function(prefix) {
		var new_checkbox = create_single_checkbox(prefix);
		filter_group_html += new_checkbox;
	});
	filter_group_html += '</div>'
	return filter_group_html;
};

/**
 * Create new collection based on API, Endpoint, CURIE, Predicate
 * @param {String} api
 * @param {String} endpoint
  * @param {String} curie
 * @param {String} predicate
 * @return {String} html for new collection
*/
function create_single_collection(api, endpoint, curie, predicate) {
    var template = '<li class="collection-item avatar"><span class="title">ID:   {curie}</span><p>Predicate:   {predicate}</p><p>API:   {API}</p><p>Endpoint:   {Endpoint}</p><a href="#!" class="secondary-content"><i class="material-icons collection-search" id="{curie}">search</i></a></li>'
    template = template.replace('{API}', api).replace('{Endpoint}', endpoint).replace('{curie}', curie).replace('{predicate}', predicate).replace('{curie}', curie);
    return template
};

/**
 * Update the refine side bar
*/
function populate_filter(jsonResponse) {
    $(".filter").empty();
    var predicate_summary = {'id': []};
    var api_summary = {'id': []};
    var endpoint_summary = {'id': []};
    for (var semantic_type in jsonResponse['summary']) {
        $.each(jsonResponse['summary'][semantic_type]['predicate'], function(i, predicate) {
            if($.inArray(predicate, predicate_summary['id']) === -1) predicate_summary['id'].push(predicate);
        });
        $.each(jsonResponse['summary'][semantic_type]['api'], function(i, api) {
            if($.inArray(api, api_summary['id']) === -1) api_summary['id'].push(api);
        });
        $.each(jsonResponse['summary'][semantic_type]['endpoint'], function(i, endpoint) {
            if($.inArray(endpoint, endpoint_summary['id']) === -1) endpoint_summary['id'].push(endpoint);
        });
        $(".filter").append(create_single_filter_group(semantic_type, jsonResponse['summary'][semantic_type]));
    };
    $(".filter").append(create_single_filter_group('predicate', predicate_summary));
    $(".filter").append(create_single_filter_group('api', api_summary));
    $(".filter").append(create_single_filter_group('endpoint', endpoint_summary));
};

/**
 * Update the data content
*/
function populate_data_display(jsonResponse) {
    $(".data-display-list").empty();
    var i = 0;
    for (i = 0; i < 20; i++) {
        $(".data-display-list").append(create_single_collection(CURRENT_CRAWLING_RESULTS[i]['api'], CURRENT_CRAWLING_RESULTS[i]['endpoint'], CURRENT_CRAWLING_RESULTS[i]['curie'], CURRENT_CRAWLING_RESULTS[i]['predicate']));
    };
};

/**
 * Shuffles array in place.
 * @param {Array} a items An array containing the items.
 */
function shuffle(a) {
    var j, x, i;
    for (i = a.length - 1; i > 0; i--) {
        j = Math.floor(Math.random() * (i + 1));
        x = a[i];
        a[i] = a[j];
        a[j] = x;
    }
}

/**
 * shuffle the crawling results
*/
CURRENT_CRAWLING_RESULTS = []
function shuffle_results(jsonResponse) {
    CURRENT_CRAWLING_RESULTS = []
    for (var semantic_type in jsonResponse['linkedData']) {
        $.merge(CURRENT_CRAWLING_RESULTS, jsonResponse['linkedData'][semantic_type]);
    };
    shuffle(CURRENT_CRAWLING_RESULTS);
};

$(document).ready(function(){
    var prefix = 'ncbigene';
    var input_value = '1017';
    fetch_crawler_results(prefix, input_value).done(function(jsonResponse) {
        shuffle_results(jsonResponse);
    	populate_filter(jsonResponse);
        populate_data_display(jsonResponse);
    });
});