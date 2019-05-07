function fetch_knowledgemap(){
  var promise = $.ajax({
      type:"GET",
      url: "/explorer_beta/api/v2/knowledgemap",
      datatype: "json"
  });
  return promise;
};

function constructAPIMap(){
  fetch_knowledgemap().done(function(jsonResponse) {
    var nodes_dict = {};
    var nodes = [];
    var edges = [];
    var edge_list = [];
    var node_id = 1;
    var api_dict = {};
    jsonResponse['associations'].forEach(function(assoc) {
      if (!(assoc['subject']['prefix'] in nodes_dict)) {
        nodes_dict[assoc['subject']['prefix']] = node_id;
        nodes.push({'group': assoc['api'], 'id': node_id, 'label': assoc['subject']['prefix']});
        node_id += 1;
      };
      if (!(assoc['api'] in api_dict)) {
        api_dict[assoc['api']] = node_id;
        nodes.push({'group': 'api', 'id': node_id, 'label': assoc['api']});
        node_id += 1;
      }
      if (!(assoc['object']['prefix'] in nodes_dict)) {
        nodes_dict[assoc['object']['prefix']] = node_id;
        nodes.push({'group': assoc['api'], 'id': node_id, 'label': assoc['object']['prefix']});
        node_id += 1;
      };
      edge = nodes_dict[assoc['subject']['prefix']] + 'hasInput' + api_dict[assoc['api']];
      if (!(edge_list.includes(edge))) {
        edges.push({'from': nodes_dict[assoc['subject']['prefix']],
                    'to': api_dict[assoc['api']],
                    'label': 'hasInput'});
        edge_list.push(edge);
      };
      edge = api_dict[assoc['api']] + nodes_dict[assoc['object']['prefix']] + assoc['predicate'];
      if (!(edge_list.includes(edge))) {
        edges.push({'from': api_dict[assoc['api']],
                    'to': nodes_dict[assoc['object']['prefix']],
                    'label': assoc['predicate']});
        edge_list.push(edge);
      };
    });
    var container = document.getElementById('api_view');
    var data = {
      nodes: nodes,
      edges: edges
    };
    console.log(data);
    var options = {
      nodes: {
        shape: 'box',
        size: 10,
        font: {
          size:10
        },
        borderWidth:1,
        shadow: true
      },
      edges: {
        width:1,
        shadow: true,
        font: {
          size:5,
          align: 'middle'
        }
      },
      layout:{randomSeed:3}
    };
    var network_api = new vis.Network(container, data, options);
    network_api.fit();
    });
}

function constructSemanticMap(){
  fetch_knowledgemap().done(function(jsonResponse) {
    var nodes_dict = {};
    var nodes = [];
    var edges = [];
    var edge_list = [];
    var node_id = 1;
    var api_dict = {};
    jsonResponse['associations'].forEach(function(assoc) {
      if (!(assoc['subject']['semantic_type'] in nodes_dict)) {
        nodes_dict[assoc['subject']['semantic_type']] = node_id;
        nodes.push({'id': node_id, 'label': assoc['subject']['semantic_type']});
        node_id += 1;
      };
      if (!(assoc['object']['semantic_type'] in nodes_dict)) {
        nodes_dict[assoc['object']['semantic_type']] = node_id;
        nodes.push({'id': node_id, 'label': assoc['object']['semantic_type']});
        node_id += 1;
      };
      edge = nodes_dict[assoc['subject']['semantic_type']] + nodes_dict[assoc['predicate'] + assoc['object']['semantic_type'];
      if (!(edge_list.includes(edge))) {
        edges.push({'from': nodes_dict[assoc['subject']['semantic_type']],
                    'to': api_dict[assoc['object']['semantic_type'],
                    'label': assoc['predicate']});
        edge_list.push(edge);
      };
    });
    var container = document.getElementById('api_view');
    var data = {
      nodes: nodes,
      edges: edges
    };
    console.log(data);
    var options = {
      nodes: {
        shape: 'box',
        size: 10,
        font: {
          size:10
        },
        borderWidth:1,
        shadow: true
      },
      edges: {
        width:1,
        shadow: true,
        font: {
          size:5,
          align: 'middle'
        }
      },
      layout:{randomSeed:3}
    };
    var network_api = new vis.Network(container, data, options);
    network_api.fit();
    });
}


$(document).ready(function(){
  //drawApiLevelMap();
  //constructAPIMap();
  constructSemanticMap();
});


