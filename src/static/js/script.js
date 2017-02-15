$(function(){
    var cy = cytoscape({
    container: document.getElementById('cy'),
    elements: [
        {'data': {'id': 'n0', 'symbol': '1017', 'type': 'field_name', 'kwargs': 'hgnc_gene_id', 'kwargs_type': 'field_name'}}],
    style: [
        {
          'selector': "node[type = 'field_name']",
          'style': {
              'shape': 'hexagon',
              'background-color': 'red',
              'label': 'data(symbol)'
          }
        },
        {
          'selector': "node[type = 'annotate_api']",
          'style': {
              'shape': 'circle',
              'background-color': 'blue',
              'label': 'data(symbol)'
          }
        },
        {
          'selector': "node[type = 'query_api']",
          'style': {
              'shape': 'circle',
              'background-color': 'green',
              'label': 'data(symbol)'
          }
        },],
    layout: {name: 'concentric'}
});
cy.on('click', 'node', function(evt){
  var node = evt.cyTarget;
  if (node.data()['type'] == 'field_name'){
    $.ajax(
      {
        url: '/field/',
        type: 'POST',
        data: JSON.stringify(node.data()),
        success: function (jsonResponse) {
            var objresponse = JSON.parse(jsonResponse);
            cy.add(objresponse);
            cy.layout({name: 'concentric'});
        },
        error: function (error) {
            console.log(error)
        }
    });
  } else if(node.data()['type'] == 'annotate_api'){
    $.ajax(
      {
        url: '/annotate/',
        type: 'POST',
        data: JSON.stringify(node.data()),
        success: function (jsonResponse) {
            var objresponse = JSON.parse(jsonResponse);
            console.log(objresponse)
        },
        error: function (error) {
            console.log(error)
        }
    })
  } else if(node.data()['type'] == 'query_api'){
    $.ajax(
      {
        url: '/query/',
        type: 'POST',
        data: JSON.stringify(node.data()),
        success: function (jsonResponse) {
            var objresponse = JSON.parse(jsonResponse);
            console.log(objresponse)
        },
        error: function (error) {
            console.log(error)
        }
    })
  }

});
});

    /*
    $.ajax({
        url: '/add',
        data: node.data(),
        type: 'POST',
        success: function(response) {
            console.log(response)
        },
        error: function(error) {
            console.log(error);
        }
    });
  });
});
});
*/


