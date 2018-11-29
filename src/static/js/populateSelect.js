/**
 * Automatically add metadata info to the options of select
 * @param {Array} data
 * @param {String} metadata_type
 * @param {String} dropdown_id
*/
function addOptionFromMetaData(metadata, metadata_type, dropdown_id){    
    $(dropdown_id).empty();
    $(dropdown_id).append('<option value="" disabled selected>Choose the ' + metadata_type + ' you want to explore</option>')
    for (var idx in metadata) {
        $(dropdown_id).append('<option value =' + metadata[idx] + '>' + metadata[idx] + '</option>');
    };
};



/**
 * Get metadata information based on type
 * @param {String} metadata_type
 * @return {Promise} getMetaData
*/

function getMetaData(metadata_type){
  var promise = $.ajax({
    type:"GET",
    url: "/explorer/api/v2/metadata/" + metadata_type,
    datatype: "json"
  });
  return promise;
}

/**
 * Get available endpoint info based on input
*/
function getEndpointsBasedOnInput(_input) {
    var promise = $.ajax({
        type: "POST",
        url: "/explorer/input2endpoint",
        data: {input: _input},
        datatype: "json"
    });
    return promise;
}

/**
 * Get available output info based on endpoint
*/
function getOutputBasedOnEndpoint(_endpoint) {
    var promise = $.ajax({
        type: "POST",
        url: "/explorer/endpoint2output",
        data: {endpoint: _endpoint},
        datatype: "json"
    });
    return promise;
}

/**
 * Automatically add endpoint info to the options of select
 * @param {String} dropdown_id
*/
function populateEndpoints(dropdown_id){
    getMetaData('endpoints').done(function(jsonResponse){
        var endpoint_select2_data = $.map(jsonResponse.endpoint, function(n) {
            return {"id": n, "text": n};
        });
        $(dropdown_id).select2({data: endpoint_select2_data});
    });
};

/**
 * Automatically add semantic type info to the options of select
 * @param {String} dropdown_id
*/
function populateSemanticType(dropdown_id, default_value=null, include_all=false){
    getMetaData('semantic_types').done(function(jsonResponse){
        var semantic_type_select2_data = $.map(jsonResponse.semantic_types, function(n) {
            if (default_value == n) {
                return {"id": n, "text": n, "selected": true}
            } else {
                return {"id": n, "text": n};
            }
        });
        if (include_all) {
            semantic_type_select2_data.unshift({"id": "all", "text": "All Semantic Types"})
        }
        $(dropdown_id).select2({data: semantic_type_select2_data});
    });
};


/**
 * Automatically add semantic type info to the options of select
 * @param {String} dropdown_id
*/
function populateNumAPI(dropdown_id, default_value=null){
    $(dropdown_id).select2({data: [{"id": 1, "text": 1}, {"id": 2, "text": 2}, {"id": 3, "text": 3}]});
    //set the default value of the select
    if (default_value) {
        $(dropdown_id).val(default_value);
        $(dropdown_id).trigger('change'); 
    }
};
/** Automatically add crawler input to the options of select
* @param {String} dropdown_id
*/
function populateCrawlerInput(dropdown_id){
    getMetaData('crawler_input').done(function(jsonResponse){
        var bioentity_select2_data = []
        for (var semantic_type in jsonResponse.bioentity) {
            var group = {'id': semantic_type, 'text': semantic_type, 'children': []};
            var bioentity_id_list = jsonResponse.bioentity[semantic_type];
            for (var bioentity_id in bioentity_id_list) {
                group['children'].push({id: bioentity_id_list[bioentity_id], text: bioentity_id_list[bioentity_id]})
            };
            bioentity_select2_data.push(group);
        };
        $(dropdown_id).select2({data: bioentity_select2_data});
    });
};

/**
 * Automatically add bioentity info to the options of select
 * @param {String} dropdown_id
*/
function populateBioEntity(dropdown_id, default_value=null, semantic_type1=null){
    // empty  all current options in select
    $(dropdown_id).empty();
    getMetaData('bioentities').done(function(jsonResponse){
        var bioentity_select2_data = []
        if (semantic_type1 == null) {
            for (var semantic_type in jsonResponse.bioentity) {
                var group = {'id': semantic_type, 'text': semantic_type, 'children': []};
                var bioentity_id_list = jsonResponse.bioentity[semantic_type];
                for (var bioentity_id in bioentity_id_list) {
                    if (bioentity_id_list[bioentity_id] == default_value) {
                        group['children'].push({id: bioentity_id_list[bioentity_id], text: bioentity_id_list[bioentity_id], selected: true})
                    } else {
                        group['children'].push({id: bioentity_id_list[bioentity_id], text: bioentity_id_list[bioentity_id]})
                    }
                };
                bioentity_select2_data.push(group);
            };
        } else {
            var bioentity_id_list = jsonResponse.bioentity[semantic_type1];
            for (var bioentity_id in bioentity_id_list) {
                if (bioentity_id_list[bioentity_id] == default_value) {
                    bioentity_select2_data.push({id: bioentity_id_list[bioentity_id], text: bioentity_id_list[bioentity_id], selected: true})
                } else {
                    bioentity_select2_data.push({id: bioentity_id_list[bioentity_id], text: bioentity_id_list[bioentity_id]})
                }
            };
            bioentity_select2_data.unshift({id: 'all', text: 'All ' + semantic_type1.toUpperCase() + ' IDs', selected: true});
        };
        
        $(dropdown_id).select2({data: bioentity_select2_data});
        //set the default value of the select
        /*
        if (default_value) {
            $(dropdown_id).val(default_value); 
            $(dropdown_id).trigger('change'); 
        }
        */
    });
};

function populatePath(dropdown_id, data){
    $("#explore-path").show();
    $(dropdown_id).empty();
    //add select all paths option first
    /*
    $.each(data, function(index, value) {
        $(dropdown_id).append('<option value =' + index + '>' + 'Path: ' + index + '</option>');
    });
    $(dropdown_id).material_select();
    */
    var path_data = []
    for (var i=0; i < data.length; i+=1) {
        path_data.push({id: i+1, text: 'Path: ' + (i+1), value: data[i]})
    };
    $(dropdown_id).select2({data:path_data})
};

/**
 * Automatically populate all selects in the side bar
*/
function populateSelectInSideBar() {
    populateEndpoints("#select-endpoint");
    populateBioEntity("#select-input");
    populateBioEntity("#select-output");
    populateBioEntity("#direct-input");
    populateBioEntity("#direct-output");
    populateBioEntity("#semantic-input");
    populateBioEntity("#semantic-output");
    populateBioEntity("#select-input1");
    populateBioEntity("#select-output1");
    populateInput("#customize1");
    populateSemanticType("#select-semantic-input");
    populateSemanticType("#select-semantic-output");
    $("#select-max-api").select2();
    //$("#customize2").material_select();
    //$("#customize3").material_select();
    
}

/**
 * Automatically add available bio-entities as input of endpoint
*/
function populateInput(dropdown_id) {
    getMetaData('bioentity_input').done(function(jsonResponse) {
        addOptionFromMetaData(jsonResponse['input'], 'input', dropdown_id);
        //$(dropdown_id).material_select();
    });
}
/**
 * Automatically add available bio-entities as input of endpoint
*/
function poplulateEndpointFromInput(dropdown_id, _input) {
    getEndpointsBasedOnInput(_input).done(function(jsonResponse) {
        addOptionFromMetaData(jsonResponse['endpoints'], 'endpoint', dropdown_id);
        $(dropdown_id).material_select();
    });
}
/**
 * Automatically add available bio-entities as input of endpoint
*/
function populateOutputFromEndpoint(dropdown_id, _endpoint) {
    getOutputBasedOnEndpoint(_endpoint).done(function(jsonResponse) {
        addOptionFromMetaData(jsonResponse['output'], 'output', dropdown_id);
        $(dropdown_id).material_select();
    });
}
