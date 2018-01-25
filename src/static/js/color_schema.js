var datapoints = [
                    {'type': 'clinical trial', 'color': 'rgba(144, 144, 28, 0.4)'}, 
                    {'type': 'gene', 'color': 'rgba(55, 230, 84, 0.93)'},
                    {'type': 'chemical', 'color': 'rgba(230, 55, 218, 0.93)'}, 
                    {'type': 'protein', 'color': 'rgba(55, 227, 230, 0.6)'},
                    {'type': 'variant', 'color': 'rgba(230, 174, 55, 0.83)'}, 
                    {'type': 'publication', 'color': 'rgba(86, 28, 144, 0.3)'},
                    {'type': 'phenotype', 'color': 'rgba(28, 86, 144, 0.3)'}, 
                    {'type': 'pathway', 'color': 'rgba(230, 55, 116, 0.63)'},
                    {'type': 'disease', 'color': 'rgba(166, 55, 230, 0.84)'}, 
                    {'type': 'transcript', 'color': 'rgba(100, 88, 77, 0.4)'},
                    {'type': 'clinical significance', 'color': 'rgba(70, 33, 77, 0.4)'},
                    {'type': 'organism', 'color': 'rgba(10, 133, 177, 0.4)'},
                    {'type': 'structure', 'color': 'rgba(8, 233, 7, 0.4)'}
                ];


function drawColorSchema(){
    var svg = d3.select("#color-schema")
               .append("svg")
               .attr("width", 600)
               .attr("height", 400);
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
};
