
function drawSankeyPlot(jsonResponse, type){
  // hide all non sankey plots in the main div
  if (type=='path'){
      $("#error-message").empty();
      Plotly.purge('path-plotly');
      $("#explore-plotly-div").hide();
      $("#path-plotly-div").show();

  } else if (type=='explore'){
      Plotly.purge('explore-plotly');
      $("#path-plotly-div").hide();
      $("#explore-plotly-div").show();
  }

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
      label: fig.plotly.edge_labels,
      color: "#e3e5e8"
    }
  };

  var data = [data];

  var layout = {
    title: jsonResponse.title,
    font: {
      size: 10
    },
    paper_bgcolor: 'rgba(0,0,0,0)'
  };
  if (type=='path'){
    Plotly.plot('path-plotly', data, layout, {responsive: true});
  } else if (type=="explore"){
    Plotly.plot('explore-plotly', data, layout, {responsive: true});
  };
};
