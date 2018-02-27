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
    var template = '<p class="filter-item"><label><input type="checkbox" class="filled-in"/><span>{input}</span></label></p>';
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
CURRENT_DATA_INDEX = 0;
function initialize_data_display(data) {
    $(".data-display-list").empty();
    CURRENT_DATA_INDEX = 0;
    var i = 0;
    if (data.length > 20) {
        for (i = 0; i < 20; i++) {
            $(".data-display-list").append(create_single_collection(data[i]['api'], data[i]['endpoint'], data[i]['curie'], data[i]['predicate']));
            $("#show-more").show();
        };
        CURRENT_DATA_INDEX = 20;
    } else {
        for (i = 0; i < data.length; i++) {
            $(".data-display-list").append(create_single_collection(data[i]['api'], data[i]['endpoint'], data[i]['curie'], data[i]['predicate']));
            $("#show-more").hide();
        }
    };
    show_more_results();
};

/**
 * function to yield 20 more results
*/
function extend_data_display(data) {
    if (data.length > (20 + CURRENT_DATA_INDEX)) {
        for (var i=CURRENT_DATA_INDEX; i < CURRENT_DATA_INDEX + 20; i++) {
            $(".data-display-list").append(create_single_collection(data[i]['api'], data[i]['endpoint'], data[i]['curie'], data[i]['predicate']));
            $("#show-more").show();
        };
        CURRENT_DATA_INDEX += 20;
    } else {
        for (var i=CURRENT_DATA_INDEX; i < data.length; i++) {
            $(".data-display-list").append(create_single_collection(data[i]['api'], data[i]['endpoint'], data[i]['curie'], data[i]['predicate']));
            $("#show-more").hide();
        }
    }
}

/**
 * function to yield more results when user clicks on 'show more results'
*/
function show_more_results() {
    $("#show-more").click(function() {
        extend_data_display(CURRENT_DISPLAY_CONTENT);
    })
}

/**
 * Add more data to th
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
/**
 * Group a list of dicts by its key
*/
function groupBy(xs, key) {
  return xs.reduce(function(rv, x) {
    (rv[x[key]] = rv[x[key]] || []).push(x);
    return rv;
  }, {});
};
/**
 * change data display based on filter checkbox change
*/
NON_PREFIX_DATA_TYPE = ['api', 'endpoint', 'predicate'];
CURRENT_DISPLAY_CONTENT = [];
function update_data_display_by_filter_results(){
    CURRENT_FILTER_STATUS = {'prefix': [], 'api': [], 'endpoint': [], 'predicate': []};
    $("input[type=checkbox]").change(function(){
        $(".overlay-group").show();
        CURRENT_DISPLAY_CONTENT = []
        var filter_criteria = $(this).siblings('span').text();
        var data_type = $(this).parents('.filter-item').siblings('h5').text();
        if (this.checked) {     
            if (NON_PREFIX_DATA_TYPE.includes(data_type)) {
                CURRENT_FILTER_STATUS[data_type].push(filter_criteria);
            } else {
                CURRENT_FILTER_STATUS['prefix'].push(filter_criteria);
            }
        }
        else {
            if (NON_PREFIX_DATA_TYPE.includes(data_type)) {
                var index = CURRENT_FILTER_STATUS[data_type].indexOf(filter_criteria);
                if (index > -1) {
                    CURRENT_FILTER_STATUS[data_type].splice(index, 1);
                }
            } else {
                var index = CURRENT_FILTER_STATUS['prefix'].indexOf(filter_criteria);
                if (index > -1) {
                    CURRENT_FILTER_STATUS['prefix'].splice(index, 1);
                } 
            }
        };
        if (CURRENT_FILTER_STATUS['prefix'].length > 0) {
            var results_groupby_prefix = groupBy(CURRENT_CRAWLING_RESULTS, 'prefix');
            CURRENT_FILTER_STATUS['prefix'].forEach(function(_prefix) {
                CURRENT_DISPLAY_CONTENT = CURRENT_DISPLAY_CONTENT.concat(results_groupby_prefix[_prefix]);
            });
        } else {
            CURRENT_DISPLAY_CONTENT = CURRENT_CRAWLING_RESULTS;
        };
        NON_PREFIX_DATA_TYPE.forEach(function(key) {
            if (CURRENT_FILTER_STATUS[key].length > 0) {
                var results_groupby_criteria = groupBy(CURRENT_DISPLAY_CONTENT, key);
                CURRENT_DISPLAY_CONTENT = []
                CURRENT_FILTER_STATUS[key].forEach(function(_criteria) {
                    CURRENT_DISPLAY_CONTENT = CURRENT_DISPLAY_CONTENT.concat(results_groupby_criteria[_criteria]);
                })
            }
        });
        initialize_data_display(CURRENT_DISPLAY_CONTENT);
        $(".overlay-group").hide();
        update_data_display_by_user_search();
        show_more_results();
    })
};

/**
 * change data display when user click on one of the item in the display collection
*/
function update_data_display_by_user_search(){
    $(".collection-search").click(function(){
        $(".overlay-group").show();
        var prefix = $(this).attr('id').split(":")[0];
        var input_value = $(this).attr('id').split(":")[1];
        update_data_display(prefix, input_value);
    });
};

/**
 * change data display when user click on one of the item in the search history
*/
function update_data_display_by_search_history(){
    $(".chip").click(function(){
        $(".overlay-group").show();
        var prefix = $(this).text().split(":")[0];
        var input_value = $(this).text().split(":")[1];
        update_data_display(prefix, input_value);
    });
};

/**
 * Given prefix and input_value, display the results
*/
function update_data_display(prefix, input_value) {
    fetch_crawler_results(prefix, input_value).done(function(jsonResponse) {
        add_chip(prefix + ':' + input_value);
        $(".overlay-group").hide();
        shuffle_results(jsonResponse);
        populate_filter(jsonResponse);
        initialize_data_display(CURRENT_CRAWLING_RESULTS);
        CURRENT_DISPLAY_CONTENT = CURRENT_CRAWLING_RESULTS;
        $(".main").show();
        update_data_display_by_filter_results();
        update_data_display_by_user_search();
        update_data_display_by_search_history();
    });
};

/**
 * Add a chip recording search history
*/
function add_chip(search_item) {
    $(".search-history").append('<div class="chip" style="cursor:pointer;">' + search_item + '</div>');
};

$(document).ready(function(){
    populateBioEntity('#select-input');
    $('#start-crawl-button').click(function() {
        $("#navbar").css({'position': 'relative'});
        $(".crawler-header").hide();
        $(".overlay-group").show();
        $(".search-bar-center").removeClass("search-bar-center");
        $(".search-history").show();
        var prefix = $("#select-input").find("option:selected").attr('value');
        var input_value = $("#crawler-input-value").val();
        update_data_display(prefix, input_value);
    });
});