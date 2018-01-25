
function drawSankeyPlot(jsonResponse){
  // hide all non sankey plots in the main div
  Plotly.purge('path-plotly');
  $(".overview_map").hide();
  $("#path-plotly-div").show();
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

  Plotly.plot('path-plotly', data, layout, {displayModeBar: false});

};
