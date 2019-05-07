/**
 * Get the knowledge map
 * @return {Promise} knowledgemap
*/

function retrieveKnowledgeMap(){
  var promise = $.ajax({
    type:"GET",
    url: "/explorer_beta/api/v2/knowledgemap",
    datatype: "json"
  });
  return promise;
};

function drawSemanticMap(nodes_semantic, edges_semantic){
// create an array with nodes


  // create a network
  var container = document.getElementById('semantic_type_view');
  var data = {
    nodes: nodes_semantic,
    edges: edges_semantic
  };
  var options = {
    nodes: {
        shape: 'box',
        size: 13,
        font: {
            size:13
        },
        borderWidth:1,
        shadow: true
    },
    edges: {
        width:2.5,
        shadow: true,
      font: {
        size:8,
        align: 'middle'
      }
    },
    layout:{randomSeed:3}
  };
  var network_semantic = new vis.Network(container, data, options);
};

function drawIdLevelMap(nodes_id, edges_id){
// create an array with nodes


  // create a network
  var container = document.getElementById('bioentity_id_view');
    // legend
  var x = - container.clientWidth / 2 + 50;
  var y = - container.clientHeight / 2 + 50;
  var step = 70;
  var data = {
    nodes: nodes_id,
    edges: edges_id
  };
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
  var network_id = new vis.Network(container, data, options);
};

function convertKnowledgeMapToVisJsGraph(){
    //initialize nodes, edges
  var semantic_nodes = [];
  var semantic_edges = [];
  var semantic_node_id = 1;
  var semantic_nodes_dict = {};
  var entity_nodes = [];
  var entity_edges = [];
  var entity_node_id = 1;
    var entity_nodes_dict = {};
  var api_nodes = []
  var api_edges = []
  var api_node_id = 1
    var api_nodes_dict = {};
  retrieveKnowledgeMap().done(function(jsonResonse){
    var map = jsonResonse.associations;
    map.forEach(function(triple){
            if (!(triple['object']['prefix'] in entity_nodes_dict)) {
                entity_nodes_dict[triple['object']['prefix']] = entity_node_id;
                entity_nodes.push({'id': entity_node_id, 'label': triple['object']['prefix'], 'group': entity_node_id});
                entity_node_id += 1;
            };
            if (!(triple['subject']['prefix'] in entity_nodes_dict)) {
                entity_nodes_dict[triple['subject']['prefix']] = entity_node_id;
                entity_nodes.push({'id': entity_node_id, 'label': triple['subject']['prefix'], 'group': entity_node_id});
                entity_node_id += 1;
            };
            if (!(triple['object']['semantic_type'] in semantic_nodes_dict)) {
                semantic_nodes_dict[triple['object']['semantic_type']] = semantic_node_id;
                semantic_nodes.push({'id': semantic_node_id, 'label': triple['object']['semantic_type'], 'group': semantic_node_id});
                semantic_node_id += 1;
            };
            if (!(triple['subject']['semantic_type'] in semantic_nodes_dict)) {
                semantic_nodes_dict[triple['subject']['semantic_type']] = semantic_node_id;
                semantic_nodes.push({'id': semantic_node_id, 'label': triple['subject']['semantic_type'], 'group': semantic_node_id});
                semantic_node_id += 1;
            };
            entity_edges.push({'from': entity_nodes_dict[triple['subject']['prefix']], 'to': entity_nodes_dict[triple['object']['prefix']], 'label': triple['predicate'], 'endpoint': triple['endpoint']});
            semantic_edges.push({'from': semantic_nodes_dict[triple['subject']['semantic_type']], 'to': semantic_nodes_dict[triple['object']['semantic_type']], 'label': triple['predicate'], 'endpoint': triple['endpoint']});
    });
        console.log(semantic_edges);
        console.log(semantic_nodes);
        drawSemanticMap(semantic_nodes, semantic_edges);
        drawIdLevelMap(entity_nodes, entity_edges);
        return semantic_edges;
  });
    //return (entity_edges, semantic_edges)
};
