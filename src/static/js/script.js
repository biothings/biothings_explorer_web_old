// define concentric option
var concentricOptions = {
    name: 'concentric',
    concentric: function(node) {
        return 10 - node.data('level');
    },
    levelWidth: function() {
        return 1;
    },
    padding: 40
};

// 
$(function(){
    //set the height of the cytoscape display div relative to the window size
    $("#cy").css("height", $(window).height()-$("#navbar").height());

    var cy = cytoscape({
    container: document.getElementById('cy'), // container to render in

    style: [
        {
            'selector': "node",
            'style': {
                'text-valign': 'top',
                'text-halign': 'center',
                'background-color': '#555',
                'color': 'black',
                'z-index': '10'
            }
        },
        {
            'selector': "node[type = 'field_name']",
            'style': {
                'shape': 'circle',
                'background-color': 'red',
                'label': 'data(symbol)',
                'width': '100'
            }
        },
        {
            'selector': 'node:selected',
            'style': {
              'border-width': '10px',
              'border-color': '#AAD8FF',
              'border-opacity': '0.5',
              'background-color': '#77828C',
              'text-outline-color': '#77828C'
            }
        },
        {
            'selector': "node[type = 'id']",
            'style': {
                'shape': 'circle',
                'font-size': '80px',
                'background-color': 'green',
                'label': 'data(id)',
                'width': '200',
                'height': '200'
            }
        },
        {
            'selector': "node[type = 'path']",
            'style': {
                'shape': 'circle',
                'background-color': 'mapData(level, 0, 2, green, red)',
                'label': 'data(id)'
            }
        },
        {
            'selector': "node[type = 'api']",
            'style': {
                'background-color': 'blue',
                'label': 'data(id)',
                'shape': 'star',
                'width': '100',
                'height': '100',
                'font-size': '50px'
            }
        },
        {
            'selector': "node[type = 'endpoint']",
            'style': {
                'background-color': 'red',
                'label': 'data(id)',
                'shape': 'triangle',
                'width': '150',
                'height': '150',
                'font-size': '80px'
            }
        },
        {
            'selector': "node[type = 'input']",
            'style': {
                'background-color': 'green',
                'label': 'data(id)',
                'width': '150',
                'height': '150',
                'font-size': '80px'
            }
        },
        {
            'selector': "node[type = 'output']",
            'style': {
                'background-color': 'green',
                'label': 'data(id)',
                'width': '150',
                'height': '150',
                'font-size': '80px'
            }
        },
        {
            'selector': "node[type = 'start']",
            'style': {
                'background-color': 'blue',
                'label': 'data(symbol)',
                'shape': 'diamond',
                'width': '150',
                'height': '150',
                'font-size': '80px'
            }
        },
        {
            'selector': "node[type = 'end']",
            'style': {
                'background-color': 'blue',
                'label': 'data(symbol)',
                'shape': 'diamond',
                'width': '150',
                'height': '150',
                'font-size': '80px'
            }
        },
        {
            'selector': "edge",
            'style': {
              'label': 'data(label)',
              'font-size': '10px',
              'target-arrow-shape': 'triangle',
              'curve-style': 'haystack',
              'haystack-radius': '0.5',
              'opacity': '0.4',
              'line-color': '#bbb',
              'overlay-padding': '3px',
              'width': 4,
              'target-arrow-color': '#ddd'
            }
        },
        {
            'selector': "edge.bezier",
            'style': {
                'curve-style': 'bezier',
                'control-point-step-size': 120
            }
        },
        {
            'selector': '.highlighted',
            'style': {
                'background-color': 'red',
                'line-color': 'red',
                'target-arrow-color': 'red',
                'transition-property': 'background-color, line-color, target-arrow-color',
                'transition-duration': '0.5s'
            }
        }]
      });
        // when user click 'API MAP', display the API connectivity map
    /*
    When user click the 'map', display a connecting map for APIs and bio-entities.
    */
    $("#map").click(function(){
        cy.elements().remove();
        $.ajax(
        {
            url: "./relation/",
            type: "POST",
            success: function(jsonResponse){
                var objresponse = JSON.parse(jsonResponse);
                var api_info = objresponse;
                //First need to empty all options in select
                $("#Select1, #Select2").find('option').remove();
                $(".explore-input").hide();
                $(".cy-path:not(h1)").show();
                var triples;
                cy, triples = addApiInfoToGraph(cy, objresponse);
                cy.layout(concentricOptions);
                console.log(cy.edges());
                cy.nodes().forEach(function(ele) {
                    ele.qtip({
                        content: {
                            text: qtipTextMap(ele),
                            title: ele.data('id')
                        },
                        style: {
                            classes: 'qtip-bootstrap'
                        },
                        position: {
                            my: 'bottom center',
                            at: 'top center',
                            target: ele
                        }
                    });
                });
                $('select').material_select();
                $('#updatePath').click(function(){
                    cy.elements().remove();
                    var start = $('#Select1').find(':selected').text();
                    var end = $('#Select2').find(':selected').text();
                    var results;
                    var routes;
                    routes = findPath(start, end, triples);
                    if (routes.length == 0) {
                        $("#cy h1").show();
                    }
                    else {
                        $("#cy h1").hide();
                        cy.add({'data': {'id': end, 'symbol': "End Point: " + end, 'type': 'end'}, 'position': {'x': -100000, 'y': -100000}});
                        cy.add({'data': {'id': start, 'symbol': "Start Point: " + start, 'type': 'start'}, 'position': {'x': -100000, 'y': -100000}});
                        cy = addRouteToCy(cy, routes, api_info);
                        cy.layout({name: 'breadthfirst'});
                        cy.nodes().forEach(function(ele) {
                            ele.qtip({
                                content: {
                                    text: qtipTextPath(ele),
                                    title: ele.data('id')
                                },
                                style: {
                                    classes: 'qtip-bootstrap',
                                    width: 1000,
                                    height: 500
                                },
                                position: {
                                    my: 'bottom center',
                                    at: 'top center',
                                    target: ele
                                }
                            });
                        });
                        cy.edges().on("click", function(){
                            cy.$().removeClass('highlighted');
                            cy.edges("[route=" + this.data()['route'] + "]").addClass('highlighted');
                            var target_path = routes[this.data()['route']];
                            $("#path_start_input").show();
                            $("#userInput").click(function(){
                            var input_value = $('#textarea1').val();
                            console.log(input_value, target_path);
                            $.ajax(
                            {
                                url: "./path/",
                                type: "POST",
                                data: JSON.stringify({'path': target_path, 'input': input_value}),
                                success: function (jsonResponse){
                                    var objresponse = JSON.parse(jsonResponse);
                                    cy.elements().remove();
                                    cy.batch(function(){
                                        var edge = 0
                                        objresponse.forEach(function(pair){
                                            if (cy.getElementById(pair[0]).empty()) {
                                                cy.add({'data': {'id': pair[0], 'type': 'path', 'level': pair[2]},'position': {'x': -100000, 'y': -100000}});
                                            };
                                            if (cy.getElementById(pair[1]).empty()) {
                                                cy.add({'data': {'id': pair[1], 'type': 'path', 'level': pair[2] + 1},'position': {'x': -100000, 'y': -100000}});
                                            };
                                            cy.add({'data': {'id': 'edge' + edge, 'source': pair[0], 'target': pair[1]}});
                                            edge += 1
                                        })
                                    });
                                    cy.layout(concentricOptions);
                                    
                                }
                            })  
                            })
                        })
                    };
                $("#resetMap").click(function(){
                    $("#cy h1").hide();
                    cy.elements().remove();
                    cy, triples = addApiInfoToGraph(cy, objresponse);
                    cy.layout(concentricOptions);
                })
            })
        }
    });
});
})


// add api and bio-entities to the graph
function addApiInfoToGraph(cy, api_info){
    var triples = []
    var arrays = []
    // add bioentity info onto the graph
    for (var key in api_info['bioentity']) {
        if (api_info['bioentity'].hasOwnProperty(key)){
            cy.add({'data': {'id': api_info['bioentity'][key]['preferred_name'], 'alternative_name': api_info['bioentity'][key]['alternative_name'], 'uri': api_info['bioentity'][key]['uri'], 'description': api_info['bioentity'][key]['description'], 'registry_identifier': api_info['bioentity'][key]['registry_identifier'], 'identifier_pattern': api_info['bioentity'][key]['identifier_pattern'], 'type': 'id', 'level': 2}});
            var opt1 = document.createElement('option');
            var opt2 = document.createElement('option');
            opt1.value = opt1.innerHTML = opt2.innerHTML = api_info['bioentity'][key]['preferred_name'];
            opt2.value = api_info['bioentity'][key]['preferred_name'] + '_2';
            $("#Select1").append(opt1);
            $("#Select2").append(opt2);
        }
    };
    // add endpoints info onto the graph
    for (var key in api_info['endpoint']) {
        if (api_info['endpoint'].hasOwnProperty(key)){
            console.log(key);
            cy.add({'data': {'id': key, 'description': api_info['endpoint'][key]['get']['summary'], 'type': 'endpoint', 'level': 1}});
            api_info['endpoint'][key]['input'].forEach(function(_input){
                if (cy.getElementById(key + 'to' + _input['preferred_name']).empty()) {
                    cy.add({'data': {'id': key + 'to' + _input['preferred_name'], 'source': key, 'target': _input['preferred_name'], 'label': 'has_input'}})
                };
                api_info['endpoint'][key]['output'].forEach(function(_output){
                    _array = _input['preferred_name'] + _output['preferred_name'] + key;
                    _triple = {input: _input['preferred_name'], output: _output['preferred_name'], endpoint: key};
                    if ($.inArray(_array, arrays) === -1){
                        triples.push(_triple);
                        arrays.push(_array);
                    }
                })
            });
            api_info['endpoint'][key]['output'].forEach(function(_output){
                if (cy.getElementById(key + 'to' + _output['preferred_name']).empty()) {
                    cy.add({'data': {'id': key + 'to' + _output['preferred_name'], 'source': key, 'target': _output['preferred_name'], 'label': 'has_output'}})
                }
            });
        };
    }
    // add api info onto the graph
    for (var key in api_info['api']) {
        console.log(key);
        if (api_info['api'].hasOwnProperty(key)){
            cy.add({'data': {'id': key, 'description': api_info['api'][key]['info']['description'], 'type': 'api', 'level': 0}});
            api_info['api'][key]['endpoints'].forEach(function(_endpoint){
                console.log(_endpoint);
                cy.add({'data': {'id': 'edge' + _endpoint, 'source': key, 'target': _endpoint, 'label': 'has_endpoint'}});
            })
        }
    }
    return (cy, triples)
}
/**
    api_info.forEach(function(_api){
        cy.add({'data': {'id': _api['api'], 'description': _api['description'], 'type': 'api', 'level': 0}});
        _api['paths'].forEach(function(_endpoint){
            var endpoint_name = _endpoint['name'];
            cy.add({'data': {'id': endpoint_name, 'description': _endpoint['description'], 'type': 'endpoint', 'level': 1}})
            cy.add({'data': {'id': 'edge' + endpoint_name, 'source': _api['api'], 'target': endpoint_name, 'label': 'has_endpoint'}})
            cy.batch(function(){
                _endpoint['input'].forEach(function(_input){
                    if (cy.getElementById(_input['preferred_name']).empty()) {
                        cy.add({'data': {'id': _input['preferred_name'], 'alternative_name': _input['alternative_name'], 'uri': _input['uri'], 'description': _input['description'], 'registry_identifier': _input['registry_identifier'], 'identifier_pattern': _input['identifier_pattern'], 'type': 'id', 'level': 2}})
                        var opt1 = document.createElement('option');
                        var opt2 = document.createElement('option');
                        opt1.value = opt1.innerHTML = opt2.innerHTML = _input['preferred_name'];
                        opt2.value = _input + '_2';
                        $("#Select1").append(opt1);
                        $("#Select2").append(opt2);
                    }
                    if (cy.getElementById(endpoint_name + 'to' + _input['preferred_name']).empty()) {
                        cy.add({'data': {'id': endpoint_name + 'to' + _input['preferred_name'], 'source': endpoint_name, 'target': _input['preferred_name'], 'label': 'has_input'}})
                    }
                    _endpoint['output'].forEach(function(_output){
                        //This code is to make sure there is no duplicate _triple in triples
                        _array = _input['preferred_name'] + _output['preferred_name'] + endpoint_name;
                        _triple = {input: _input['preferred_name'], output: _output['preferred_name'], endpoint: endpoint_name};
                        if ($.inArray(_array, arrays) === -1){
                            triples.push(_triple);
                            arrays.push(_array);
                        }
                    })
                })
                _endpoint['output'].forEach(function(_output){
                    if (cy.getElementById(_output['preferred_name']).empty()) {
                        cy.add({'data': {'id': _output['preferred_name'], 'alternative_name': _output['alternative_name'], 'uri': _output['uri'], 'description': _output['description'], 'registry_identifier': _output['registry_identifier'], 'identifier_pattern': _output['identifier_pattern'], 'type': 'id', 'level': 2}})
                        var opt1 = document.createElement('option');
                        var opt2 = document.createElement('option');
                        opt1.value = opt1.innerHTML = opt2.innerHTML = _output['preferred_name'];
                        opt2.value = _output['preferred_name'] + '_2';
                        $("#Select1").append(opt1);
                        $("#Select2").append(opt2);
                    }
                    if (cy.getElementById(endpoint_name + 'to' + _output['preferred_name']).empty()) {
                        cy.add({'data': {'id': endpoint_name + 'to' + _output['preferred_name'], 'source': endpoint_name, 'target': _output['preferred_name'], 'label': 'has_output'}})
                    }
                    
                })
            })

        })
    })
    return (cy, triples)
}
*/

/* This function takes input (path start/path end), 
and return paths which connect from start to end */
function findPath(start, end, triples) {
    var routes = [];
    // case 1: path start and path end share the same endpoint
    triples.forEach(function(_triple){
        if (start == _triple['input'] && end == _triple['output']) {
            routes.push([_triple]);
        }
    })
    // case 2: path start and path end need an intermediate endpoint to connect
    if (routes.length == 0) {
        triples.forEach(function(_triple1){
            if (start == _triple1['input']) {
                triples.forEach(function(_triple2){
                    if (_triple1['output'] == _triple2['input'] && end == _triple2['output']) {
                        routes.push([_triple1, _triple2]);
                    }
                })
            }
        })
    }
    return routes
}

/* This function adds connecting paths between start and end
onto the cytoscape graph */
function addPathToCy(cy, paths) {
    cy.batch(function(){
        var edge = 0;
        paths.forEach(function(_path){
            for (var key in _path) {
                if (cy.getElementById(_path[key]).empty()) {
                    cy.add({'data': {'id': _path[key], 'type': key}, 'position': {'x': -100000, 'y': -100000}});
                } else {
                    cy.add({'data': {'id': _path[key], 'type': key, 'description': api_info['endpoint'][key]['get']['summary']}})
                }
            }
            cy.add({'data': {'id': 'edge' + edge, 'name': _path['input'] + 'to' + _path['endpoint'], 'source': _path['input'], 'target': _path['endpoint'], 'label': 'has_input'}, 'classes': 'bezier'});
            edge += 1
            cy.add({'data': {'id': 'edge' + edge, 'name': _path['output'] + 'to' + _path['endpoint'], 'source': _path['endpoint'], 'target': _path['output'], 'label': 'has_output'}, 'classes': 'bezier'});
            edge += 1
            })
        })
    return cy
}

function addRouteToCy(cy, routes, api_info) {
    cy.batch(function(){
        var edge = 0;
        routes.forEach(function(paths, i){
            paths.forEach(function(_path, k){
                for (var key in _path) {
                    if (cy.getElementById(_path[key]).empty()) {
                        if (key != 'endpoint'){
                            cy.add({'data': {'id': _path[key], 'type': key}, 'position': {'x': -100000, 'y': -100000}});
                        } else {
                            cy.add({'data': {'id': _path[key], 'type': key, 'description': api_info['endpoint'][_path[key]]['get']['summary'], 'parameters': api_info['endpoint'][_path[key]]['get']['parameters']}, 'position': {'x': -100000, 'y': -100000}});
                        }
                        
                    }
                }
                cy.add({'data': {'id': 'edge' + edge, 'name': _path['input'] + 'to' + _path['endpoint'], 'source': _path['input'], 'target': _path['endpoint'], 'label': 'has_input', 'route': i}, 'classes': 'bezier'});
                edge += 1
                cy.add({'data': {'id': 'edge' + edge, 'name': _path['output'] + 'to' + _path['endpoint'], 'source': _path['endpoint'], 'target': _path['output'], 'label': 'has_output', 'route': i}, 'classes': 'bezier'});
                edge += 1
                })                   
            })
        })
    return cy
}

function qtipTextMap(node) {
    if (node.data('type') != 'id') {
        return 'Description: ' + node.data('description') + '<br>'
    } else {
        return '<b>Description: </b>' + node.data('description') + '<br>' + '<b>Preferred_name: </b>' + node.data('id') + '<br>' + '<b>URI: </b>' + node.data('uri') + '<br>' + '<b>Registry Identifier: </b>' + node.data('registry_identifier') + '<br>' + '<b>Alternative name: </b>' + node.data('alternative_name') + '<br>' + '<b>Identifier Pattern: </b>' + node.data('identifier_pattern')
    }
}

function qtipTextPath(node) {
    if (node.data('type') == 'api') {
        return 'Description: ' + node.data('description') + '<br>'
    } else if (node.data('type') == 'endpoint') {
        console.log(node.data('description'));
        return 'Description: ' + node.data('description') + '<br> <form action = "#">' + composeForm(node.data('parameters')) + '<br><br><input type="submit" value="Submit"></form>'
    }
    else {
        return '<b>Description: </b>' + node.data('description') + '<br>' + '<b>Preferred_name: </b>' + node.data('id') + '<br>' + '<b>URI: </b>' + node.data('uri') + '<br>' + '<b>Registry Identifier: </b>' + node.data('registry_identifier') + '<br>' + '<b>Alternative name: </b>' + node.data('alternative_name') + '<br>' + '<b>Identifier Pattern: </b>' + node.data('identifier_pattern')
    }
}

function composeForm(parameters){
    input = ''
    parameters.forEach(function(_para){
        if ('schema' in _para && 'enum' in _para['schema']) {
            console.log(_para['schema']);
            _input = '<select id=' + _para['name'] + '>'
            _para['schema']['enum'].forEach(function(_value){
                _option = '<option value=' + _value + '>' + _value + '</option>'
                _input += _option
            })
            input += _input
            input += '</select>'
            label = '<label>' + _para['name'] + '</label>'
            input += label
            console.log(input);
        } else {
            _input = '<b>' + _para['name'] + ':</b> <br> <input type="text" name=' + _para['name'] + ' value="inputvalue"><br>'
            //input += _input
        }
    })
    return input
}