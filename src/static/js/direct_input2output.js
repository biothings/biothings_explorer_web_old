/**
 * Get the 
 * @return {Promise} knowledgemap
*/

function retrieveDirectOutput(input_prefix, input_value, output_prefix){
  var promise = $.ajax({
    type:"GET",
    url: "/explorer/api/v2/directinput2output",
    data: {'input_prefix': input_prefix, 'output_prefix': output_prefix, 'input_value': input_value},
    datatype: "json"
  });
  return promise;
};

function DirectOutput2Graph(){
    $("#DirectInput2OutputButton").click(function(){
        hide_all_graph_div();
        $(".direct_output_display").show();
        var _input = $("#direct-input").find("option:selected").attr('value');
        var _output = $("#direct-output").find("option:selected").attr('value');
        var _value = $("#direct_input_value").val();
    	retrieveDirectOutput(_input, _value, _output).done(function(jsonResonse){
            $(".progress").hide();
    		var results = jsonResonse.data;
            var node_title = 'prefix: ' + _input;
    		var nodes = [{'id': 1, 'label': _value, 'title': node_title, 'font': {'color': 'red'}, 'group': 1}];
    		var nodes_id = 2;
    		var edges = [];
    		results.forEach(function(_result) {
                console.log(_result['endpoint']);
                node_label = _result['output'][0]['object']['id'];
                node_title = 'prefix: ' + _output;
                nodes.push({'id': nodes_id, 'object_info': _result['output'][0]['object'], 'title': node_title, 'font': {'color': 'blue'}, 'label': node_label.slice(node_label.split(':')[0].length + 1), 'group': 2});
                edges.push({'from': 1, 'to': nodes_id, 'endpoint': _result['endpoint'], 'edge_info': _result['output'][0]['edge'], 'arrows': 'to', 'title': _result['predicate']})
                nodes_id += 1;
    		});
            drawInputOutputGraph(new vis.DataSet(nodes), new vis.DataSet(edges));
    	})
    })
}

function createUnorderedList(ul) {
    if (typeof ul == 'string') {
        console.log('string!');
        return '<ul><li>' + ul + '</li></ul>';
    } else {
        results = '<ul>'
        ul.forEach(function(ele){
            results += '<li>' + ele + '</li>'
        });
        results += '</ul>'
        return results;
    }
}
function drawInputOutputGraph(nodes, edges){
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
        color: 'grey',
      font: {
        size:8,
        align: 'middle'
      }
    },
    layout:{randomSeed:3}
  };
  var network_semantic = new vis.Network(container, data, options);
  network_semantic.on("click", function(params) {
    var clicked_node_id = params.nodes;
    var clicked_edge_id = params.edges;
    if (clicked_node_id.length > 0) {
        $("#node_edge_description").empty();
        var append_text = '<h4>Description</h4>';
        var object_info = nodes.get(params.nodes)[0]['object_info'];
        for (var key in object_info) {
            append_text += '<b>' + key + '</b>';
            append_text += createUnorderedList(object_info[key]);
        };
        console.log(append_text);
        $("#node_edge_description").html(append_text);
    } else {
        $("#node_edge_description").empty();
        var append_text = '<h4>Description</h4>';
        var edge_info = edges.get(params.edges)[0]['edge_info'];
        console.log(edges.get(params.edges)[0]['endpoint']);
        append_text += '<b>Endpoint</b>';
        append_text += createUnorderedList(edges.get(params.edges)[0]['endpoint']);
        for (var key in edge_info) {
            append_text += '<b>' + key + '</b>';
            append_text += createUnorderedList(edge_info[key]);
        };
        $("#node_edge_description").html(append_text);
        console.log(append_text);
    }
    
    nodes.forEach(function(node_info){
        if (node_info['id'] == clicked_node_id) {
            //console.log(node_info);
        }
    })
  })
};