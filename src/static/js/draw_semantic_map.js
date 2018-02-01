
var nodes_semantic = new vis.DataSet([{'id': 1, 'label': 'gene', 'group':1},
 {'id': 2, 'label': 'disease', 'group':2},
 {'id': 3, 'label': 'chemical', 'group':3},
 {'id': 4, 'label': 'variant', 'group':4},
 {'id': 5, 'label': 'protein', 'group':5},
 {'id': 6, 'label': 'organism', 'group':6},
 {'id': 7, 'label': 'publication', 'group':7},
 {'id': 8, 'label': 'compound', 'group':8},
 {'id': 9, 'label': 'ontology', 'group':9},
 {'id': 10, 'label': 'pathway', 'group':10},
 {'id': 11, 'label': 'structure', 'group':11},
 {'id': 12, 'label': 'transcript', 'group':12},
 {'id': 13, 'label': 'clinical significance', 'group':13},
 {'id': 15, 'label': 'clinical trial', 'group':14},
 {'id': 14, 'label': 'phenotype', 'group':15, 'color': 'green'}]);

  // create an array with edges
  var edges_semantic = new vis.DataSet([{'from': 1, 'label': 'associatedWithDisease', 'to': 2},
 {'from': 3, 'label': 'associatedWithChemical', 'to': 3},
 {'from': 4, 'label': 'hasXref', 'to': 2},
 {'from': 2, 'label': 'associatedWithDisease', 'to': 2},
 {'from': 2, 'label': 'associatedWithChemical', 'to': 3},
 {'from': 4, 'label': 'associatedWithProtein', 'to': 5},
 {'from': 4, 'label': 'associatedWithVariant', 'to': 4},
 {'from': 4, 'label': 'hasXref', 'to': 4},
 {'from': 3, 'label': 'associatedWithVariant', 'to': 4},
 {'from': 1, 'label': 'associatedWithVariant', 'to': 4},
 {'from': 1, 'label': 'associatedWithGene', 'to': 1},
 {'from': 1, 'label': 'hasHomolog', 'to': 1},
 {'from': 6, 'label': 'hasChild', 'to': 6},
 {'from': 4, 'label': 'associatedWithPublication', 'to': 7},
 {'from': 3, 'label': 'physicallyInteractsWith', 'to': 5},
 {'from': 3, 'label': 'hasXref', 'to': 8},
 {'from': 1, 'label': 'associatedWithOntology', 'to': 9},
 {'from': 4, 'label': 'associatedWithGene', 'to': 1},
 {'from': 3, 'label': 'physicallyInteractsWith', 'to': 3},
 {'from': 1, 'label': 'physicallyInteractsWith', 'to': 1},
 {'from': 7, 'label': 'associatedWithGene', 'to': 1},
 {'from': 1, 'label': 'associatedWithOrganism', 'to': 6},
 {'from': 10, 'label': 'associatedWithOrganism', 'to': 6},
 {'from': 11, 'label': 'associatedWithOrganism', 'to': 6},
 {'from': 7, 'label': 'associatedWithOrganism', 'to': 6},
 {'from': 12, 'label': 'associatedWithOrganism', 'to': 6},
 {'from': 1, 'label': 'associatedWithProtein', 'to': 5},
 {'from': 3, 'label': 'transportedBy', 'to': 5},
 {'from': 2, 'label': 'associatedWithVariant', 'to': 4},
 {'from': 1, 'label': 'associatedWithPublication', 'to': 7},
 {'from': 6, 'label': 'hasParent', 'to': 6},
 {'from': 4, 'label': 'associatedWithClinicalSignificance', 'to': 13},
 {'from': 3, 'label': 'associatedWithPublication', 'to': 7},
 {'from': 2, 'label': 'hasXref', 'to': 2},
 {'from': 3, 'label': 'carriedBy', 'to': 5},
 {'from': 1, 'label': 'associatedWithTranscript', 'to': 12},
 {'from': 1, 'label': 'associatedWithPhenotype', 'to': 14},
 {'from': 5, 'label': 'associatedWithOrganism', 'to': 6},
 {'from': 3, 'label': 'catalyzedBy', 'to': 5},
 {'from': 5, 'label': 'associatedWithGene', 'to': 1},
 {'from': 2, 'label': 'associatedWithPhenotype', 'to': 14},
 {'from': 12, 'label': 'associatedWithGene', 'to': 1},
 {'from': 4, 'label': 'associatedWithTranscript', 'to': 12},
 {'from': 1, 'label': 'functionTogetherWith', 'to': 1},
 {'from': 3, 'label': 'associatedWithDisease', 'to': 2},
 {'from': 11, 'label': 'associatedWithGene', 'to': 1},
 {'from': 10, 'label': 'associatedWithGene', 'to': 1},
 {'from': 7, 'label': 'associatedWithVariant', 'to': 4},
 {'from': 13, 'label': 'associatedWithVariant', 'to': 4},
 {'from': 4, 'label': 'associatedWithChemical', 'to': 3},
 {'from': 1, 'label': 'hasXref', 'to': 1},
 {'from': 5, 'label': 'associatedWithVariant', 'to': 4},
 {'from': 1, 'label': 'associatedWithPathway', 'to': 10},
 {'from': 5, 'label': 'associatedWithChemical', 'to': 3},
 {'from': 12, 'label': 'associatedWithVariant', 'to': 4},
 {'from': 2, 'label': 'associatedWithGene', 'to': 1},
 {'from': 3, 'label': 'hasXref', 'to': 3},
 {'from': 3, 'label': 'physicallyInteractsWith', 'to': 1},
 {'from': 1, 'label': 'associatedWithProteinStructure', 'to': 11},
 {'from': 3, 'label': 'associatedWithClinicalTrial', 'to': 15},
 {'from': 4, 'label': 'associatedWithDisease', 'to': 2},
 {'from': 1, 'label': 'associatedWithChemical', 'to': 3}]
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


