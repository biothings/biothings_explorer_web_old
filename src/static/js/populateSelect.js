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
    url: "/explorer/metadata/" + metadata_type,
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
    getMetaData('endpoint').done(function(jsonResponse){
        var parsedJson = $.parseJSON(jsonResponse);
        addOptionFromMetaData(parsedJson['endpoint'], 'endpoint', dropdown_id);
        $(dropdown_id).material_select();
    });
};

/**
 * Automatically add bioentity info to the options of select
 * @param {String} dropdown_id
*/
function populateBioEntity(dropdown_id){
    getMetaData('bioentity').done(function(jsonResponse){
        var parsedJson = $.parseJSON(jsonResponse);
        addOptionFromMetaData(parsedJson['bioentity'], 'bioentity', dropdown_id);
        $(dropdown_id).material_select();
    });
};

function populatePath(dropdown_id, data){
    $(dropdown_id).empty();
    $.each(data, function(index, value) {
        $(dropdown_id).append('<option value =' + index + '>' + 'Path: ' + index + '</option>');
    });
    $(dropdown_id).material_select();
}

/**
 * Automatically populate all selects in the side bar
*/
function populateSelectInSideBar() {
    populateEndpoints("#select-endpoint");
    populateBioEntity("#select-input");
    populateBioEntity("#select-output");
    populateBioEntity("#select-input1");
    populateBioEntity("#select-output1");
    populateInput("#customize1");
    $("#select-max-api").material_select();
    $("#customize2").material_select();
    $("#customize3").material_select();
}

/**
 * Automatically add available bio-entities as input of endpoint
*/
function populateInput(dropdown_id) {
    getMetaData('bioentity_input').done(function(jsonResponse) {
        var parsedJson = $.parseJSON(jsonResponse);
        addOptionFromMetaData(parsedJson['input'], 'input', dropdown_id);
        $(dropdown_id).material_select();
    });
}
/**
 * Automatically add available bio-entities as input of endpoint
*/
function poplulateEndpointFromInput(dropdown_id, _input) {
    getEndpointsBasedOnInput(_input).done(function(jsonResponse) {
        var parsedJson = $.parseJSON(jsonResponse);
        addOptionFromMetaData(parsedJson['endpoints'], 'endpoint', dropdown_id);
        $(dropdown_id).material_select();
    });
}
/**
 * Automatically add available bio-entities as input of endpoint
*/
function populateOutputFromEndpoint(dropdown_id, _endpoint) {
    getOutputBasedOnEndpoint(_endpoint).done(function(jsonResponse) {
        var parsedJson = $.parseJSON(jsonResponse);
        addOptionFromMetaData(parsedJson['output'], 'output', dropdown_id);
        $(dropdown_id).material_select();
    });
}
