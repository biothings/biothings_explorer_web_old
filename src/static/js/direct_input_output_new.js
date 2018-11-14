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

function DirectOutput2Graph(_input, _output, _value){
    $(".error").hide();
    $(".preloader-wrapper").show();
    $(".tabs").tabs();
    var instance = M.Tabs.getInstance($(".tabs"));
    var helper_text = '<div id="graph-details-info"><p class="help-text">Click on one of the nodes or edges in the network to view more details...</p><img src="./static/img/help-left-arrow.png" width="75"></div>'
    $("#node_info").empty();
    $("#edge_info").empty();
    $("#context_info").empty();
    $("#node_info").html(helper_text);
    $("#edge_info").html(helper_text);
    $("#context_info").html(helper_text);
    instance.select('node_info');
    retrieveDirectOutput(_input, _value, _output).done(function(jsonResonse){
        $(".preloader-wrapper").hide();
        var results = jsonResonse.data;
        var node_title = 'prefix: ' + _input;
        var nodes = [{'id': 1, 'label': _value, 'title': node_title, 'font': {'color': 'red'}, 'group': 1}];
        var nodes_id = 2;
        var edges = [];
        results.forEach(function(_result) {
            node_label = _result['output']['object']['id'];
            node_title = 'prefix: ' + _output;
            if ('edge' in _result['output']) {
                var edge_info = _result['output']['edge'];
            } else {
                var edge_info = {};
            }
            edge_info['predicate'] = _result['predicate'];
            nodes.push({'id': nodes_id, 'object_info': _result['output']['object'], 'title': node_title, 'font': {'color': 'blue'}, 'label': node_label.slice(node_label.split(':')[0].length + 1), 'group': 2});
            edges.push({'from': 1, 'to': nodes_id, 'context': _result['context'], 'api': _result['api'], 'edge_info': edge_info, 'arrows': 'to', 'title': _result['predicate']})
            nodes_id += 1;
        });
        drawInputOutputGraph(new vis.DataSet(nodes), new vis.DataSet(edges));
        $(".download").show();
        $("#DownloadCodeButton").click(function() {
            download_file('bt_explorer_code_directinput2output.py', construct_directinput2output_text(_input, _value, _output), 'text/plain');
        });
    }).fail(function (err) {
        $("#DownloadCodeButton").hide();
        $(".navigation").hide();
        $(".error").show();
        $(".error").empty();
        $(".error").html('<h2 class="center">' + err.responseJSON['error message'].replace('\n', '<br />') + '</h2>')
    });
}

function createUnorderedList(ul) {
    if (typeof ul == 'string') {
        return '<ul><li>' + ul + '</li></ul>';
    } else {
        results = '<ul>'
        ul.forEach(function(ele){
            results += '<li>' + ele + '</li>'
        });
        results += '</ul>'
        return results;
    }
};

function createTableRow(ul) {
    if (typeof ul == 'string') {
        return ul;
    } else {
        results = ''
        ul.forEach(function(ele) {
            results += ele + '<br />';
        });
        return results;
    }
};

/**
function generateNodeTable(object_info) {
    var append_text = '<h4>Description</h4>';
    for (var key in object_info) {
        append_text += '<b>' + key + '</b>';
        append_text += createUnorderedList(object_info[key]);
    };
    return append_text;
};
**/


function generateNodeTable(object_info) {
    var table_html = '<table style="width:100%" class="centered striped responsive-table"><thead><tr><th style="width:30%">Name</th><th style="width:70%">Value</th></tr></thead><tbody>';
    for (var key in object_info) {
        table_html += '<tr><td>' + key + '</td><td>' + createTableRow(object_info[key]) + '</td></tr>';
    };
    table_html += '</tbody></table>';
    return table_html;
};

function generateEdgeTable(endpoint_info, edge_info) {
    var table_html = '<table style="width:100%" class="centered striped responsive-table"><thead><tr><th style="width:30%">Name</th><th style="width:70%">Value</th></tr></thead><tbody>';
    table_html += '<tr><td>API</td><td>' + endpoint_info + '</td></tr>';
    for (var key in edge_info) {
        table_html += '<tr><td>' + key + '</td><td>' + createTableRow(edge_info[key]) + '</td></tr>';
    };
    return table_html;
};

/**
function generateEdgeTable(endpoint_info, edge_info) {
    var append_text = '<h4>Description</h4>';
    append_text += '<b>Endpoint</b>';
    append_text += createUnorderedList(endpoint_info);
    for (var key in edge_info) {
        append_text += '<b>' + key + '</b>';
        append_text += createUnorderedList(edge_info[key]);
    };
    return append_text;
}
**/

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
        var endpoint_info = edges.get(params.edges)[0]['api'];
        var edge_message = generateEdgeTable(endpoint_info, edge_info);
        var context_message = generateNodeTable(edges.get(params.edges)[0]['context'])
        $("#edge_info").html(edge_message);
        $("#node_info").html(node_message);
        $("#context_info").html(context_message);
        instance.select('edge_info');
    }
  })
};