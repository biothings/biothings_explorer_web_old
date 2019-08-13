/**
 * Get the 
 * @return {Promise} knowledgemap
*/

function retrieveSemanticOutput(input_prefix, input_value, output_prefix){
  var promise = $.ajax({
    type:"GET",
    url: "/explorer_beta/api/v2/semanticquery",
    data: {'input_prefix': input_prefix, 'output_prefix': output_prefix, 'input_value': input_value},
    datatype: "json"
  });
  return promise;
};

var NODES = []
var EDGES = []
var NODES_NO_INTERMEDIATE = []
var EDGES_NO_INTERMEDIATE = []
var EDGE_COLOR_DICT = {1: 'green', 2: 'blue', 3: 'red', 4: 'pink', 5: 'yellow'}
CURRENT_SELECTION = 'intermediate'
function SemanticOutput2Graph(){
    $("#SemanticInput2OutputButton").click(function(){
        $(".intermediate-switch").hide();
        $(".search-bar-header").hide();
        $("#intro").hide();
        $(".landing-page").hide();
        hide_all_graph_div();
        $("#main").show();
        $(".progress").show();
        $(".direct_output_display").show();
        $(".mainview").hide();
        $(".tabs").tabs();
        var instance = M.Tabs.getInstance($(".tabs"));
        var helper_text = '<div id="graph-details-info"><p class="help-text">Click on one of the nodes or edges in the network to view more details...</p><img src="./static/img/help-left-arrow.png" width="75"></div>'
        $("#node_info").empty();
        $("#edge_info").empty();
        $("#context_info").empty();
        $("#node_info").html(helper_text);
        $("#edge_info").html(helper_text);
        $("#context_info").html(helper_text);
        $("#error-message").empty();
        instance.select('node_info');
        var _input = $("#direct-input").find("option:selected").attr('value');
        var _output = $("#direct-output").find("option:selected").attr('value');
        var _value = $("#direct_input_value").val();
        $("#cy").empty();
        var _input = $("#semantic-input").find("option:selected").attr('value');
        var _output = $("#semantic-output").find("option:selected").attr('value');
        var _value = $("#semantic_input_value").val();
    	retrieveSemanticOutput(_input, _value, _output).done(function(jsonResonse){
            $(".intermediate-switch").show();
            $(".progress").hide();
            $(".mainview").show();
            var results = jsonResonse.data;
            var node_title = 'prefix: ' + _input;
            var input_prefix = _input.toUpperCase();
            var input_curie = input_prefix + ":" + _value;
            var node_dict = {}
            var nodes_no_intermediate_dict = {}
            nodes_no_intermediate_dict[input_curie] = 1;
            node_dict[input_curie] = 1;
            NODES = [{'id': 1, 'label': _value, 'title': node_title, 'size': 15, 'font': {'color': 'red'}, 'group': 1}];
            var nodes_id = 2;
            NODES_NO_INTERMEDIATE = [{'id': 1, 'label': _value, 'title': node_title, 'size': 15, 'font': {'color': 'red'}, 'group': 1}];
            var nodes_no_intermediate_id = 2;
            EDGES = [];
            EDGES_NO_INTERMEDIATE = []
            var endpoint_dict = {}
            var endpoint_id = 1
            results.forEach(function(_item) {
                _item.forEach(function(_result){
                    var endpoint_name =  _result['endpoint']
                    if (!(endpoint_name in endpoint_dict)){
                        endpoint_dict[endpoint_name] = endpoint_id;
                        endpoint_id += 1
                    };
                    var edge_color = EDGE_COLOR_DICT[endpoint_dict[endpoint_name]];
                    console.log(edge_color);
                    node_label = _result['output']['object']['id'];
                    node_prefix = node_label.split(':')[0].toLowerCase();
                    if (node_prefix == _output){
                        node_group = 3
                    } else {
                        node_group = 2
                    }
                    node_value = node_label.slice(node_label.split(':')[0].length + 1)
                    source_node_value = _result['input'];
                    if (source_node_value in node_dict){
                        source_node_id = node_dict[source_node_value];
                    } else {
                        console.log('source node not found', source_node_value);
                    }
                    
                    node_title = 'prefix: ' + _output;
                    if ('edge' in _result['output']) {
                        var edge_info = _result['output']['edge'];
                    } else {
                        var edge_info = {};
                    }
                    edge_info['predicate'] = _result['predicate'];
                    if (! (node_label in node_dict)){
                        NODES.push({'id': nodes_id, 'object_info': _result['output']['object'], 'title': node_title, 'font': {'color': 'blue'}, 'label': node_value, 'group': node_group});
                        node_dict[node_label] = nodes_id;
                        nodes_id += 1; 
                    };
                    EDGES.push({'from': source_node_id, 'to': node_dict[node_label], 'context': _result['context'], 'color': {'color': edge_color}, 'endpoint': _result['endpoint'], 'edge_info': edge_info, 'arrows': 'to', 'title': _result['predicate']});
                    if (node_prefix == _output) {
                        if (! (node_label in nodes_no_intermediate_dict)){
                            NODES_NO_INTERMEDIATE.push({'id': nodes_no_intermediate_id, 'object_info': _result['output']['object'], 'title': node_title, 'font': {'color': 'blue'}, 'label': node_value, 'group': node_group});
                            nodes_no_intermediate_dict[node_label] = nodes_no_intermediate_id;
                            nodes_no_intermediate_id += 1
                        } 
                        EDGES_NO_INTERMEDIATE.push({'from': 1, 'to': nodes_no_intermediate_dict[node_label], 'context': _result['context'], 'endpoint': _result['endpoint'], 'edge_info': edge_info, 'arrows': 'to', 'title': _result['predicate']});
                    }
                })
            });
            drawSemanticInputOutputGraph(new vis.DataSet(NODES), new vis.DataSet(EDGES));
            switchController();
            $("#DownloadCodeButton").show();
            $("#DownloadCodeButton").click(function() {
                download_file('bt_explorer_code_semanticinput2output.py', construct_semanticinput2output_text(_input, _value, _output), 'text/plain');
            });
            /**
            if (! ($("#intermediate").checked)) {
                console.log('intermediate set to false!')
                drawInputOutputGraph(new vis.DataSet(nodes_no_intermediate), new vis.DataSet(edges_no_intermediate))
            } else {
                console.log('intermediate set to true!')
                drawInputOutputGraph(new vis.DataSet(nodes), new vis.DataSet(edges));
            }
            **/
        }).fail(function (err) {
            $(".progress").hide();
            $(".mainview").hide();
            $("#error-message").html('<h2 class="center">' + err.responseJSON['error message'].replace('\n', '<br />') + '</h2>')
        });
    })
}

function switchController() {
    $("#intermediate").change(function() {
        if($(this).is(":checked") && CURRENT_SELECTION != 'intermediate') {
            CURRENT_SELECTION = 'intermediate';
            drawSemanticInputOutputGraph(new vis.DataSet(NODES), new vis.DataSet(EDGES));
        }
        else if (!$(this).is(":checked")) {
            drawSemanticInputOutputGraph(new vis.DataSet(NODES_NO_INTERMEDIATE), new vis.DataSet(EDGES_NO_INTERMEDIATE));
            CURRENT_SELECTION = 'non-intermediate'
        }
    })
    /*
    if ($("#intermediate").attr('checked') == 'checked' ) {
        console.log('checked!');
        
    } else if ($("#intermediate").attr('checked') != 'checked') {
        console.log('unchecked!')
        
    }
    */
}

function drawSemanticInputOutputGraph(nodes, edges){
  // create a network
  var container = document.getElementById('cy');
  var data = {
    nodes: nodes,
    edges: edges
  };
  var options = {
    nodes: {
        shape: 'dot',
        size: 5,
        font: {
            size:7
        },
        borderWidth:1,
        shadow: false
    },
    edges: {
        width:0.5,
        shadow: false,
        color: {
            inherit: false
        },
      font: {
        size:8,
        align: 'middle'
      }
    },
    physics: {barnesHut: {gravitationalConstant: 0,
        centralGravity: 0, springConstant: 0}},
    layout:{randomSeed:3}
  };
  var network_semantic = new vis.Network(container, data, options);
  network_semantic.on("click", function(params) {
    $(".tabs").tabs();
    var clicked_node_id = params.nodes;
    var clicked_edge_id = params.edges;
    var instance = M.Tabs.getInstance($(".tabs"));
    if (clicked_node_id.length > 0) {
        $("#edge_info").empty();
        $("#node_info").empty();
        var node_info = nodes.get(params.nodes)[0]['object_info'];
        var node_message = generateNodeTable(node_info);
        $("#node_info").html(node_message);
        instance.select('node_info');
    } else {
        $("#node_info").empty();
        $("#edge_info").empty();
        var target_node_id = edges.get(params.edges)[0]['to'];
        var node_info = nodes.get(target_node_id)['object_info'];
        var node_message = generateNodeTable(node_info);
        var edge_info = edges.get(params.edges)[0]['edge_info'];
        var endpoint_info = edges.get(params.edges)[0]['endpoint'];
        var edge_message = generateEdgeTable(endpoint_info, edge_info);
        var context_message = generateNodeTable(edges.get(params.edges)[0]['context'])
        $("#edge_info").html(edge_message);
        $("#node_info").html(node_message);
        $("#context_info").html(context_message);
        instance.select('edge_info');
    };
  });
  switchController();
};