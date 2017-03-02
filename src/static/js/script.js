
$(function(){
  var cy = cytoscape({
  container: document.getElementById('cy'),
  elements: [
      {'data': {'id': 'n0', 'symbol': '2212', 'type': 'field_name', 'kwargs': 'hgnc_gene_id', 'kwargs_type': 'field_name'},'position': {x:-300, y: 100},'locked': true}],
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
  layout: {name: 'breadthfirst'}
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
            cy.layout({name: 'breadthfirst'});
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
            types = Object.keys(objresponse)
            $("#variant-candidate").empty();
            $("#id-list").empty();
            for (var i=0; i<types.length; i++){

              var dom_id1 = "#collapse" + i
              var domid = 'collapse' + i
              var domid1 = 'collapse_' + i
              $("#id-list").append("<div class='panel-heading'><h4 class='panel-title'><a data-toggle='collapse' href=" + dom_id1
                + ">"+ types[i] + "</h4></div><div id=" + domid + " class='panel-collapse collapse'><ul class='list-group' id=" + types[i] + "></ul></div>");
              ids = objresponse[types[i]];
              for (var j=0; j<ids.length; j++){
                var dom_id = "#" + types[i];
                $(dom_id).append("<li class='list-group-item'>" + ids[j] + "</li>")
              };
              };
              $('.list-group li').on('click', function(e){
                info = {'id': $(this).text(), 'type': $(this).closest('ul').attr('id'), 'parent': node.data()['id']};
                console.log(info);
                $.ajax(
                {
                  url: '/id/',
                  type: 'POST',
                  data: JSON.stringify(info),
                  success: function (jsonResponse){
                    var objresponse = JSON.parse(jsonResponse);
                    cy.add(objresponse);
                    cy.layout({name: 'breadthfirst'});
                  }
                })
              })
            },
        error: function (error) {
            console.log(error)
        }
    });
  } else if(node.data()['type'] == 'query_api'){
    $.ajax(
      {
        url: '/query/',
        type: 'POST',
        data: JSON.stringify(node.data()),
        success: function (jsonResponse) {
            var objresponse = JSON.parse(jsonResponse);
            ids = objresponse['ids']
            type = objresponse['type']
            $("#variant-candidate").empty();
            $("#id-list").empty();
            for (var i=0; i<ids.length; i++){
              id_escape = ids[i].replace('>', "&gt;");
              $("#variant-candidate").append("<option class='list-group-item variant-selections' value=" + id_escape + ">" + ids[i] + "</option>")
  }         $("#variant-candidate").on('change', function(e){
              info = {'id': this.value, 'type': type, 'parent': node.data()['id']};
              $.ajax(
              {
                url: '/id/',
                type: 'POST',
                data: JSON.stringify(info),
                success: function (jsonResponse){
                  var objresponse = JSON.parse(jsonResponse);
                  cy.add(objresponse);
                  cy.layout({name: 'breadthfirst'});
                }
              })
            })
        },
        error: function (error) {
            console.log(error)
        }
    })
  }
})
})
function initialize(){
  alert('button clicked!');
  var _type = $("#id_type").val();
  var _id = $("#id_name").val();
  alert(_type);
  alert(_id);
  var data = {'type': _type, 'id': _id};
  $.ajax(
  {
    url: '/initialize/',
    type: 'POST',
    data: JSON.stringify(data),
    success: function (jsonResponse){
      var objresponse = JSON.parse(jsonResponse);
      cy.add(objresponse);
      cy.layout({name: 'breadthfirst'});
    },
    error: function (error) {
      console.log(error);
    }
  });
}





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


