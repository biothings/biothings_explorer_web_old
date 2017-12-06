function drawSankeyPlot(jsonResponse){
  var fig = jsonResponse;
  console.log(fig);
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
    width: 1118,
    height: 772,
    font: {
      size: 10
    }
  };
  $("#log-list").empty();
  $("#cy").empty();
  $("#paths-list").empty();
  $("#cy").hide();
  Plotly.purge('plotly-div');
  $("#plotly-div").show();
  Plotly.plot('plotly-div', data, layout);
};
