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
            $(".progress").hide();
            $(".mainview").show();
            var results = jsonResonse.data;
            var node_title = 'prefix: ' + _input;
            var input_prefix = _input.toUpperCase();
            var input_curie = input_prefix + ":" + _value;
            var node_dict = {}
            node_dict[input_curie] = 1;
            var nodes = [{'id': 1, 'label': _value, 'title': node_title, 'size': 15, 'font': {'color': 'red'}, 'group': 1}];
            var nodes_id = 2;
            var edges = [];
            results.forEach(function(_item) {
                _item.forEach(function(_result){
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
                        nodes.push({'id': nodes_id, 'object_info': _result['output']['object'], 'title': node_title, 'font': {'color': 'blue'}, 'label': node_value, 'group': node_group});
                        node_dict[node_label] = nodes_id;
                        nodes_id += 1; 
                    };
                    edges.push({'from': source_node_id, 'to': node_dict[node_label], 'context': _result['context'], 'endpoint': _result['endpoint'], 'edge_info': edge_info, 'arrows': 'to', 'title': _result['predicate']})
                })
            });
            drawInputOutputGraph(new vis.DataSet(nodes), new vis.DataSet(edges));
        }).fail(function (err) {
            $(".progress").hide();
            $(".mainview").hide();
            $("#error-message").html('<h2 class="center">' + err.responseJSON['error message'].replace('\n', '<br />') + '</h2>')
        });
    })
}

