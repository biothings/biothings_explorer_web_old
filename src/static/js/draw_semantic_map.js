
var nodes_semantic = new vis.DataSet([{'id': 1, 'label': 'clinical significance', 'group': 'm'},
 {'id': 2, 'label': 'variant', 'group': 2},
 {'id': 3, 'label': 'chemical', 'group': 3},
 {'id': 4, 'label': 'protein', 'group': 'k'},
 {'id': 5, 'label': 'transcript', 'group': 5},
 {'id': 6, 'label': 'organism', 'group': 6},
 {'id': 7, 'label': 'gene', 'group': 7},
 {'id': 8, 'label': 'disease', 'group': 8},
 {'id': 9, 'label': 'pathway', 'group': 9},
 {'id': 10, 'label': 'clinical trial', 'group': 10},
 {'id': 11, 'label': 'structure', 'group': 15},
 {'id': 12, 'label': 'phenotype', 'group': 12},
 {'id': 13, 'label': 'publication', 'group': 13}]);

  // create an array with edges
  var edges_semantic = new vis.DataSet([{'from': 1, 'label': 'associatedWithVariant', 'to': 2},
 {'from': 2, 'label': 'associatedWithChemical', 'to': 3},
 {'from': 3, 'label': 'carriedBy', 'to': 4},
 {'from': 2, 'label': 'hasXref', 'to': 2},
 {'from': 5, 'label': 'associatedWithOrganism', 'to': 6},
 {'from': 7, 'label': 'associatedWithChemical', 'to': 3},
 {'from': 7, 'label': 'associatedWithDisease', 'to': 8},
 {'from': 7, 'label': 'associatedWithProtein', 'to': 4},
 {'from': 5, 'label': 'associatedWithVariant', 'to': 2},
 {'from': 7, 'label': 'associatedWithTranscript', 'to': 5},
 {'from': 9, 'label': 'associatedWithOrganism', 'to': 6},
 {'from': 3, 'label': 'associatedWithDisease', 'to': 8},
 {'from': 8, 'label': 'associatedWithDisease', 'to': 8},
 {'from': 7, 'label': 'hasXref', 'to': 7},
 {'from': 4, 'label': 'associatedWithOrganism', 'to': 6},
 {'from': 9, 'label': 'associatedWithGene', 'to': 7},
 {'from': 3, 'label': 'associatedWithClinicalTrial', 'to': 10},
 {'from': 2, 'label': 'associatedWithTranscript', 'to': 5},
 {'from': 7, 'label': 'hasHomolog', 'to': 7},
 {'from': 11, 'label': 'associatedWithOrganism', 'to': 6},
 {'from': 7, 'label': 'associatedWithVariant', 'to': 2},
 {'from': 2, 'label': 'associatedWithProtein', 'to': 4},
 {'from': 4, 'label': 'associatedWithVariant', 'to': 2},
 {'from': 7, 'label': 'associatedWithProteinStructure', 'to': 11},
 {'from': 8, 'label': 'associatedWithPhenotype', 'to': 12},
 {'from': 3, 'label': 'associatedWithPublication', 'to': 13},
 {'from': 4, 'label': 'associatedWithChemical', 'to': 3},
 {'from': 2, 'label': 'associatedWithGene', 'to': 7},
 {'from': 7, 'label': 'physicallyInteractsWith', 'to': 7},
 {'from': 7, 'label': 'associatedWithGene', 'to': 7},
 {'from': 3, 'label': 'associatedWithVariant', 'to': 2},
 {'from': 2, 'label': 'hasProperty', 'to': 1},
 {'from': 2, 'label': 'associatedWithPublication', 'to': 13},
 {'from': 3, 'label': 'physicallyInteractsWith', 'to': 4},
 {'from': 8, 'label': 'associatedWithVariant', 'to': 2},
 {'from': 8, 'label': 'associatedWithChemical', 'to': 3},
 {'from': 8, 'label': 'hasXref', 'to': 8},
 {'from': 7, 'label': 'associatedWithPhenotype', 'to': 12},
 {'from': 3, 'label': 'catalyzedBy', 'to': 4},
 {'from': 13, 'label': 'associatedWithVariant', 'to': 2},
 {'from': 7, 'label': 'associatedWithPathway', 'to': 9},
 {'from': 3, 'label': 'transportedBy', 'to': 4},
 {'from': 11, 'label': 'associatedWithGene', 'to': 7},
 {'from': 2, 'label': 'associatedWithDisease', 'to': 8},
 {'from': 3, 'label': 'hasXref', 'to': 3},
 {'from': 5, 'label': 'associatedWithGene', 'to': 7},
 {'from': 8, 'label': 'associatedWithGene', 'to': 7},
 {'from': 2, 'label': 'associatedWithVariant', 'to': 2},
 {'from': 4, 'label': 'associatedWithGene', 'to': 7},
 {'from': 3, 'label': 'associatedWithChemical', 'to': 3},
 {'from': 3, 'label': 'physicallyInteractsWith', 'to': 7},
 {'from': 7, 'label': 'functionTogetherWith', 'to': 7},
 {'from': 7, 'label': 'associatedWithOrganism', 'to': 6}]
);

function drawSemanticMap(){
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
  		width:1,
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


