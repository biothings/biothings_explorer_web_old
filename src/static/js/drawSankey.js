var datapoints = [
                    {'type': 'ClinicalTrial', 'color': 'rgba(144, 144, 28, 0.4)'}, 
                    {'type': 'Gene', 'color': 'rgba(55, 230, 84, 0.93)'},
                    {'type': 'Drug', 'color': 'rgba(230, 55, 218, 0.93)'}, 
                    {'type': 'Protein', 'color': 'rgba(55, 227, 230, 0.6)'},
                    {'type': 'Allele/Variant', 'color': 'rgba(230, 174, 55, 0.83)'}, 
                    {'type': 'ExperimentalStudy', 'color': 'rgba(86, 28, 144, 0.3)'},
                    {'type': 'Phenotype', 'color': 'rgba(28, 86, 144, 0.3)'}, 
                    {'type': 'Pathway', 'color': 'rgba(230, 55, 116, 0.63)'},
                    {'type': 'Disease', 'color': 'rgba(166, 55, 230, 0.84)'}, 
                    {'type': 'Reaction', 'color': 'rgba(100, 88, 77, 0.4)'}
                ];

function drawSankeyPlot(jsonResponse){
  var fig = jsonResponse;
  var data = {
    type: "sankey",
    domain: {
      x: [0,1],
      y: [0,1]
    },
    orientation: "h",
    valueformat: ".0f",
    valuesuffix: "TWh",
    node: {
      pad: 15,
      thickness: 15,
      line: {
        color: "black",
        width: 0.5
      },
     label: fig.plotly.labels,
     color: fig.plotly.colors
        },
    link: {
      source: fig.plotly.source,
      target: fig.plotly.target,
      value: fig.plotly.value,
      label: fig.plotly.edge_labels
    }
  };

  var data = [data];

  var layout = {
    autosize: false,
    width: 1200,
    height: 772,
    font: {
      size: 10
    }
  };
  $("#log").hide();
  $("#paths").hide();
  $("#log-list").empty();
  $("#cy").empty();
  $("#paths-list").empty();
  $("#cy").hide();
  Plotly.purge('plotly-div');
  $("#plotly-div").show();
  Plotly.plot('plotly-div', data, layout, {displayModeBar: false});
  var svg = d3.select("#color-schema")
             .append("svg")
             .attr("width", 600)
             .attr("height", 300);
var rectangles = svg.selectAll('rect')
                    .data(datapoints)
                    .enter()
                    .append('rect')
                    .attr('x', 95)
                    .attr('y', function(d, i) { return i * 30; })
                    .attr('height', 20)
                    .attr('width', 30)
                    .style('fill', function(d) {
                      return d['color']});

var annotations = svg.selectAll('text')
                    .data(datapoints)
                    .enter()
                    .append('text')
                    .attr('x', 80)
                    .attr('y', function(d, i) { return i * 30 + 15; })
                    .text(function(d) { return d['type']; })
                    .attr('font-size', 10)
                    .attr('text-anchor', 'end');
  $("#color-schema").show();
};
