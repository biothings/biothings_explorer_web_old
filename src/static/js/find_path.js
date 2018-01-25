/**
 * Find the connection between start and end biological entity
 * @param {String} _start
 * @param {String} _end
 * @return {Promise} findStartEndConnection
*/

function findStartEndConnection(_start, _end, _max_api=3){
  var promise = $.ajax({
    type:"GET",
    url: "/explorer/path",
    data: {start: _start, end: _end, "max_api": _max_api},
    datatype: "json"
  });
  return promise;
};

/**
 * Find the output given an input bioentity_type
 * @param {String} _input
 * @return {Promise} findOutputTypeBasedOnInputType
*/
function findOutputTypeBasedOnInputType(_input){
	var promise = $.ajax({
		type: "GET",
		url: "/explorer/input",
		data: {input: _input},
		datatype: "json"
	});
	return promise;
};

/**
 * Find the input given an output bioentity_type
 * @param {String} _output
 * @return {Promise} findInputTypeBasedOnOutputType
**/
function findInputTypeBasedOnOutputType(_output){
	var promise = $.ajax({
		type: "GET",
		url: "/explorer/output",
		data: {output: _output},
		datatype: "json"
	});
	return promise;
}

/**
 * Find the input and output given an endpoint name
 * @param {String} endpoint_name
 * @return {Promise} findInputTypeBasedOnOutputType
**/
function findInputOutputBasedOnEndpoint(endpoint_name) {
	var promise = $.ajax({
		type: "GET",
		url: "/explorer/endpoint",
		data: {endpoint: endpoint_name},
		datatype: "json"
	});
	return promise;
}

/**
 * Find output based on path and input_value
 * @param {String} input_value
 * @param {Array} path
 * @return {Promise} findInputTypeBasedOnOutputType
**/
function findOutputBasedOnInputAndPath(input_value, _path, _level) {
	var promise = $.ajax({
		type: "GET",
		url: "/explorer/findoutput",
		data: {path: JSON.stringify(_path), input: JSON.stringify(input_value), level: _level},
		datatype: "json"
	});
	return promise;
}

