
function drawSankeyPlot(jsonResponse, type){
  // hide all non sankey plots in the main div
  $(".overview_map").hide();
  $("#cy").hide();
  if (type=='path'){
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
      color: "#ffffff"
    }
  };

  var data = [data];

  var layout = {
    autosize: false,
    width: 1200,
    height: 772,
    font: {
      size: 10
    },
    paper_bgcolor: 'rgba(0,0,0,0)'
  };
  if (type=='path'){
    Plotly.plot('path-plotly', data, layout);
  } else if (type=="explore"){
    Plotly.plot('explore-plotly', data, layout);
  };
};
