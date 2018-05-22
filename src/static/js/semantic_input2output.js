/**
 * Get the 
 * @return {Promise} knowledgemap
*/

function retrieveSemanticOutput(input_prefix, input_value, output_prefix){
  var promise = $.ajax({
    type:"GET",
    url: "/explorer/api/v2/semanticquery",
    data: {'input_prefix': input_prefix, 'output_prefix': output_prefix, 'input_value': input_value},
    datatype: "json"
  });
  return promise;
};

function SemanticOutput2Graph(){
    $("#SemanticInput2OutputButton").click(function(){
        hide_all_graph_div();
        $("#cy").empty();
        $(".direct_output_display").show();
        var _input = $("#semantic-input").find("option:selected").attr('value');
        var _output = $("#semantic-output").find("option:selected").attr('value');
        var _value = $("#semantic_input_value").val();
    	retrieveSemanticOutput(_input, _value, _output).done(function(jsonResonse){
            $(".progress").hide();
    		var results = jsonResonse.data;
            var node_title = 'prefix: ' + _input;
    		var nodes = [{'id': 1, 'label': _value, 'title': node_title, 'font': {'color': 'red'}, 'group': 1}];
    		var nodes_id = 2;
    		var edges = [];
    		results.forEach(function(_result) {
                node_label = _result['output'][0]['object']['id'];
                node_title = 'prefix: ' + _output;
                nodes.push({'id': nodes_id, 'object_info': _result['output'][0]['object'], 'title': node_title, 'font': {'color': 'blue'}, 'label': node_label.slice(node_label.split(':')[0].length + 1), 'group': 2});
                edges.push({'from': 1, 'to': nodes_id, 'edge_info': _result['output'][0]['edge'], 'arrows': 'to', 'title': _result['predicate']})
                nodes_id += 1;
    		});
            drawInputOutputGraph(new vis.DataSet(nodes), new vis.DataSet(edges));
    	})
    })
}

