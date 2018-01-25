function draw_hierarchical_path(paths){
	var nodes = [];
	var edges = [];
	var node_id = 1;
	for (var path_index = 0; path_index < paths.length; path_index++) {
		nodes.push({'id': node_id, 'label': 'Path ' + (path_index + 1), 'shape': 'diamond', 'size': 10, 'color': 'red'});
		edges.push({'from': node_id, 'to': node_id + 1});
		node_id += 1;
		for (var node_index = 0; node_index < paths[path_index].length; node_index++) {
			var label = paths[path_index][node_index];
			if (label.length > 40){
				var new_label = ''
				for (var i = 0; i < label.length; i += 40) {
					if (i+40 < label.length) {
						new_label += label.slice(i, i+40);
						new_label += '\n';
					} else {
						new_label += label.slice(i, label.length)
					}
				}
				label = new_label
			};
			nodes.push({'id': node_id, 'label': label});
			node_id += 1;
			if (node_index < paths[path_index].length -1) {
				edges.push({'from': node_id - 1, 'to': node_id});
			}
		}
	};
	var container_explore = document.getElementById('explore-visjs');
	  var data = {
	    nodes: nodes,
	    edges: edges
	  };
  var options = {
  	nodes: {
  		shape: 'box',
  		size: 40,
  		font: {
  			size:8
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
  	layout:{hierarchical: {direction: "LR"}}
  };
  var network_explore = new vis.Network(container_explore, data, options);
};