
var query_info
var annotate_info
$(function(){
  /*
  For query results, 
  add selected candidate id onto the graph
  */
  function add_candidate_id_to_cy(type, node){
    $("#candidate").on('change', function(e){
      info = {'id': this.value, 'type': type, 'parent': node.data()['id'], 'relation': 'is_related_to'};
      $.ajax(
      {
        url: './id/',
        type: 'POST',
        data: JSON.stringify(info),
        success: function (jsonResponse){
          var objresponse = JSON.parse(jsonResponse);
          cy.add(objresponse);
          $("#log").prepend('<p>Add ' + info['type'] + ' (' + info['id'] + ') to the graph</p>')
          cy.layout({name: 'cose'});       
        }
      });
    });
  }
  /*
  For query results,
  add all candidate ids onto the graph
  */
  function add_all_ids_to_cy(ids, type, node){
    $("#addAllButton").on('click', function(){
      for (var i=0; i<ids.length; i++){
        info = {'id': ids[i], 'type': type, 'parent': node.data()['id']};
        $.ajax(
        {
          url: './id/',
          type: 'POST',
          data: JSON.stringify(info),
          success: function (jsonResponse){
            var objresponse = JSON.parse(jsonResponse);
            cy.add(objresponse);
            cy.layout({name: 'cose'});
            /*
            center_nodes = ''
            for (var j=0; j<objresponse.length; j++){
              if ('type' in objresponse[j]['data']){
                center_nodes = center_nodes + '#' + objresponse[i]['data']['id'] + ', ';
              }
            };
            center_nodes = center_nodes.slice(0, -2);
            cy.center(center_nodes);
            */
          }
        });
      };
    });
  }
  //highlight the path between two ids, e.g. how to connect between dbsnp_id and wikipathway_id
  function highlightpath(){
    _id1 = $('#Select1').find(":selected").text();
    _id2 = $('#Select2').find(":selected").text();
    cy.$().removeClass('highlighted');
    var dijkstra = cy.elements().dijkstra('#' + _id1);
    var bfs = dijkstra.pathTo( cy.$('#' + _id2) );
    var x=0;
    var highlightNextEle = function(){
      var el=bfs[x];
      el.addClass('highlighted');
      if(x<bfs.length-1){
        x++;
        setTimeout(highlightNextEle, 500);
      }
    };
    highlightNextEle();
  };
  //initialize cytoscape graph, define node styles based on type
  var cy = cytoscape({
  container: document.getElementById('cy'),
  style: [
      {
        'selector': "node",
        'style': {
          'font-size': '12px',
          'text-valign': 'top',
          'text-halign': 'center',
          'background-color': '#555',
          'color': 'black',
          'overlay-padding': '6px',
          'z-index': '10',
          'width': '18px',
          'height': '18px'
        }
      },
      {
        'selector': "node[type = 'field_name']",
        'style': {
            'shape': 'circle',
            'background-color': 'red',
            'font-size': '12px',
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
      },
      {
        'selector': 'node:selected',
        'style': {
          'border-width': '10px',
          'border-color': '#AAD8FF',
          'border-opacity': '0.5',
          'background-color': '#77828C',
          'text-outline-color': '#77828C'
        }
      },
      {
        'selector': "node[type = 'id']",
        'style': {
            'shape': 'circle',
            'background-color': 'green',
            'label': 'data(id)'
        }
      },
      {
        'selector': "node[type = 'api']",
        'style': {
            'background-color': 'blue',
            'label': 'data(id)'
        }
      },
      {
        'selector': "edge",
        'style': {
          'label': 'data(label)',
          'font-size': '10px',
          'target-arrow-shape': 'triangle',
          'curve-style': 'haystack',
          'haystack-radius': '0.5',
          'opacity': '0.4',
          'line-color': '#bbb',
          'overlay-padding': '3px',
          'width': 4,
          'target-arrow-color': '#ddd'
        }
      },
      {
        'selector': '.highlighted',
        'style': {
            'background-color': 'red',
            'line-color': 'red',
            'target-arrow-color': 'red',
            'transition-property': 'background-color, line-color, target-arrow-color',
            'transition-duration': '0.5s'
        }
      }]
  });
  /*
  This part is for users to explorer the relationship between different biological entities,
  e.g. how to connect between hgvs_id (variant) to wikipathays_id(pathway)
  When click 'explorer relationship' button in the 'input' div,
  empty the visualization div first,
  get data from backend through 'relation' tornado handler,
  and display node on the visualizaion div
  */
  cy.panzoom({});
  $("#exploreButton").on('click', function() {
    console.log('click explorer');
    $(".cy-path").show();
    $.ajax(
      {
        url: './relation/',
        type: 'POST',
        success: function(jsonResponse){
          cy.elements().remove();
          var objresponse = JSON.parse(jsonResponse);
          //display results on the graph
          cy.add([
          {'data': {'id': 'api', 'type': 'api'},'position': {x:800, y: -200},'locked': true},
          {'data': {'id': 'id', 'type': 'id'},'position': {x:800, y: -150},'locked': true}])
          cy.add(objresponse);
          cy.layout({name: 'concentric'});

        }
      });
    });
  $("#updatePathButton").on('click', function() {
    highlightpath();
  });
  $("#layout_types").on('change', function() {
    var layout = $('#layout_types').find(":selected").text();
    cy.layout({name: layout});
    $("#log").prepend('<p>Change layout to ' + layout + ' style</p>')
  })
  /*
  when click submit button in the 'input' div, 
  read user input 'id_type' and 'id', 
  empty the visualization div first,
  then get data from backend through 'initialize' tornado handler,
  and display node on the visulization div.
  */
  $("#submitButton").on('click', function() {
    //get user input 'id_type' and 'id_name, and construct 'data' object
    $(".cy-path").hide();
    $("#result-list").empty();
    var type = $("#id_type").val();
    var id = $("#id_name").val();
    var data = {'type': type, 'id': id};
    //fetch data from backend through 'initialize' handler,
    if (data) {
      $.ajax(
        {
          url: './initialize/',
          type: 'POST',
          data: JSON.stringify(data),
          success: function (jsonResponse){
            cy.elements().remove();
            var objresponse = JSON.parse(jsonResponse);
            //display the results on the graph
            cy.add(objresponse);
            $("#log").prepend('<hr>');
            $("#log").prepend('<p>Initialization: Add ' + type + ' (' + id + ') to the graph</p>')
            cy.layout({name: 'cose'});
          },
          error: function (error) {
            console.log(error);
          }
        })
    }
  });
  cy.on('mouseover', 'node', function(evt) {
    var node = evt.cyTarget;
    node.qtip({
      content: function(){
        if (node.data()['type'] == 'field_name'){
          var message = 'Click to show APIs related to ' + node.data()['kwargs'] + ' (' + node.data()['symbol'] + ')';
          return message
        }
        else if (node.data()['type'] == 'annotate_api'){
          var message = 'Click to annotate ' + node.data()['kwargs_type'] + ' (' + node.data()['kwargs'] + ') using ' + node.data()['symbol'] + '. Results shown on left.';
          return message
        }
        else if (node.data()['type'] == 'query_api'){
          var message = 'Click to query ' + node.data()['kwargs_type'] + ' (' + node.data()['kwargs'] + ') using ' + node.data()['symbol'] + '. Results shown on left.';
          return message
        }
        else if (node.data()['type'] == 'api'){
          var message = 'This node represent API (' + node.data()['id'] + ')';
          return message
        }
        else if (node.data()['type'] == 'id'){
          var message = 'This node represent ID (' + node.data()['id'] + ')';
          return message
        }
      },
      show: {
        event: evt.type,
        ready: true
      },
      hide: {
        event: 'mouseout unfocus'
      },
      position: {
        my: 'top center',
        at: 'bottom center'
      },
      style: {
        classes: 'qtip-bootstrap',
        tip: {
          width: 16,
          height: 8
        }
      }
    }, evt);
  });


/*
This part deals with graph user interaction,
when clicking the node, first determine the node type,
1> If the node type is 'field_name', e.g. 'entrez_gene_id'.
   Call the 'field' tornado handler, return all available APIs
   related to this field_name, and display on the graph
2> If the node type is 'annotate_api', e.g. 'mygene.info',
   Call the 'annotate' tornado handler, return a collapsible list,
   listing all ids available for further exploration 
   in the annotation resource
3> If the node type is 'query_api', e.g. 'mygene.info',
   Call the 'query' tornado handler, and return a selection list
*/
cy.on('click', 'node', function(evt){
  var node = evt.cyTarget;
  // This part deals with node type = 'field_name'
  if (node.data()['type'] == 'field_name'){
    //hide filter
    $("#filter").hide();
    $.ajax(
      {
        url: './field/',
        type: 'POST',
        data: JSON.stringify(node.data()),
        success: function (jsonResponse) {
            var objresponse = JSON.parse(jsonResponse);
            cy.add(objresponse);
            cy.layout({name: 'cose'});
            $("#log").prepend('<p>Listing APIs related to ' + node.data()['kwargs'] + ' (' + node.data()['symbol'] + ')</p>');
        },
        error: function (error) {
            console.log(error)
        }
    });
  // The following part deals with node type = 'annotate_api'
  } else if(node.data()['type'] == 'annotate_api'){
    //hide filter
    $("#pagination").hide();
    $("#filter").hide();
    $("#idlist").addClass("loading");
    console.log(node.data());
    $.ajax(
    {
      url: './annotate/',
      type: 'POST',
      data: JSON.stringify(node.data()),
      success: function (jsonResponse) {
        var objresponse = JSON.parse(jsonResponse);
        annotate_info = objresponse['xref']
        append_annotate_results(annotate_info);
        $("#idlist").removeClass("loading")
        $("#log").prepend('<p>Annotate ' + node.data()['kwargs_type'] + ' (' + node.data()['kwargs'] + ') using ' + node.data()['symbol'] + ' : <a href="' + objresponse['url'] + '">' + objresponse['url'] + '</p>')
        $('.list-group li').on('click', function(e){
          var _id;
          var _relation;
          var _type;
          console.log($(this).text());
          [_id, _type, _relation] = find_relation_type_from_id(annotate_info, $(this).text())
          info = {'id': $(this).text(), 'type': _type, 'parent': node.data()['id'], 'relation': _relation};
          console.log(_relation);
          $.ajax(
          {
            url: './id/',
            type: 'POST',
            data: JSON.stringify(info),
            success: function (jsonResponse){
              var objresponse = JSON.parse(jsonResponse);
              cy.add(objresponse);
              $("#log").prepend('<p>Add ' + info['type'] + ' (' + info['id'] + ') to the graph</p>')
              cy.layout({name: 'cose'});
            }
          })
        })
      },
      error: function (error) {
          console.log(error)
      }
    });
    // The following part deals with node type = 'query_api'
  } else if(node.data()['type'] == 'query_api'){
    $("#idlist").addClass("loading");
    $("#pagination").show();
    query_info = node.data();
    $.ajax(
    {
      url: './query/',
      type: 'POST',
      data: JSON.stringify(node.data()),
      success: function (jsonResponse) {
        var objresponse = JSON.parse(jsonResponse);
        ids = objresponse['ids'];
        type = objresponse['type'];
        $("#log").prepend('<p>Query ' + node.data()['kwargs_type'] + ' (' + node.data()['kwargs'] + ') using ' + node.data()['symbol'] + ' : <a href="' + objresponse['url'] + '">' + objresponse['url'] + '</p>')
        //remove existing filters and then create new ones
        $("#filter_list").empty();
        $("#filter_list").append(appendRowInFilter(filter_index));
        field_name_autocomplete(query_info);
        $("#filter").show();
        add_filter();
        if (objresponse['ids'].length == 0){
          $("#result-list").empty();
          $("addAllButton").remove();
          $("#pagination").twbsPagination('destroy');
          $("#result-list").append("<h4>Sorry! No results found when querying " + node.data()['kwargs_type'] + ' (' + node.data()['kwargs'] + ') using ' + node.data()['symbol'] + "</h4>")
        } else {
        append_query_results(objresponse)};
        $("#idlist").removeClass("loading");
        add_candidate_id_to_cy(type, node);
        add_all_ids_to_cy(ids, type, node);
        field_name_autocomplete(query_info);
        $("#updateButton").on('click', function(){
          $("#pagination").show();
          var para_combine = '';
          console.log(filter_index);
          for (i=0; i<= filter_index; i++) {
            para_combine += composePara(i);
          }
          query_info['para'] = para_combine;
          console.log(para_combine);
          // after clicking update, reinitialize filter index
          filter_index = 0;
          $("#filter_list").empty();
          $("#filter").hide();
          $.ajax(
          {
            url: './filter/',
            type: 'POST',
            data: JSON.stringify(query_info),
            success: function (jsonResponse) {
              var objresponse = JSON.parse(jsonResponse);
              ids = objresponse['ids'];
              type = objresponse['type'];
              $("#log").prepend('<p>Filter the query results for ' + node.data()['kwargs_type'] + ' (' + node.data()['kwargs'] + ') from ' + node.data()['symbol'] + ' : <a href="' + objresponse['url'] + '">' + objresponse['url'] + '</p>')
              if (objresponse['ids'].length != 0) {
              append_query_results(objresponse);
              add_candidate_id_to_cy(type, node);
              add_all_ids_to_cy(ids, type, node);
              }
            },
            error: function (error) {
                console.log(error)
            }
          })
        });
      },
      error: function (error) {
          console.log(error)
      }
    })
  }
});
})




/*
constructing html code to add a filter
*/
function appendFieldNameHtml(index){
  html = '<div class="form-group filter-larger"><label for="field_name' + index + '">Field_name</label><input class="form-control" id="field_name' + index + '" placeholder="dbnsfp.eigen.phred"></div>'
  return html
}

function appendCompareHtml(index){
  html = '<div class="form-group filter-small"><label for="compare' + index + '">Compare</label><select class="form-control" id="compare' + index + '"><option value=":>">></option><option value=":<"><</option><option value=":">=</option></select></div>'
  return html
}

function appendFieldValueHtml(index){
  html = '<div class="form-group filter-medium"><label for="field_value' + index + '">Field_value</label><input class="form-control" id="field_value' + index + '" placeholder="20"></div>'
  return html
}

function appendPlusIcon(index){
  html = '<span class="glyphicon glyphicon-plus" id="plus' + index + '" aria-hidden="true"></span>'
  return html
}

function appendRowInFilter(index){
  html = '<div class="row">' + appendFieldNameHtml(index) + appendCompareHtml(index) + appendFieldValueHtml(index) + '</div>'
  return html
}

function composePara(index){
  var field_name_id = '#field_name' + index;
  var compare_id = '#compare' + index;
  var field_value_id = '#field_value' + index;
  var fieldname = $(field_name_id).val();
  var compare = $(compare_id).val();
  var fieldvalue = $(field_value_id).val();
  var para = ' AND ' + fieldname + compare + fieldvalue;
  return para
}

var available_ids = ['entrez_gene_id', 'hgnc_gene_symbol', 'hgvs_id', 'dbsnp_id', 'drugbank_id', 'pubchem_id', 'clinicaltrial_id', 'uniprot_id', 'pubchem_id', 'wikipathway_id', 'ensembl_gene_id'];

/*
function(){
  $.ajax(
    {
      url: '/fetchid/',
      type: 'POST',
      dataType: 'json',
      success: function (jsonResponse) {
          available_ids = JSON.parse(jsonResponse);
      }
    });
}();
console.log(available_ids);
*/
$(function(){
  $.getJSON('http://myvariant.info/v1/metadata/fields', function(data){
    field_names = Object.keys(data);
      $("[id^='field_name']").autocomplete({
        source: [field_names]
    })
  })
  $("#id_type").autocomplete({
    source: [available_ids]
  })
})

/*
When clicking 'add' Button,
add one row of filter below
to allow performing complex queries
*/
var filter_index = 0;

function add_filter(){
  $('#addButton').on('click', function(){
    filter_index++;
    $("#filter_list").append(appendRowInFilter(filter_index));
    field_name_autocomplete(query_info);
  });
}

/*
Fetch metadata info from biothings APIs
to provide autocomplete function when users
input field names to filter down results
*/
function field_name_autocomplete(query_info){
  if (query_info.symbol == 'myvariant.info'){
    url = 'http://myvariant.info/v1/metadata/fields'
  } else if (query_info.symbol == 'mygene.info'){
    url = 'http://mygene.info/v3/metadata/fields'
  } else if (query_info.symbol == 'mydrug.info'){
    url = 'http://c.biothings.io/v1/metadata/fields'
  } else {
    url = null
  }
  $.getJSON(url, function(data){
  field_names = Object.keys(data);
    $("[id^='field_name']").autocomplete({
      source: [field_names]
    })
  })
}

/*
This function only deal with the 'results' div,
It is designed to display the annotate results from the backend onto the 'results' div
The JSON doc from annotate results include id_types, e.g. uniprot_id
and id_value, e.g. P301312.
The function first create a collapsible list for each id_type, 
then under each collapsible list, include the id_value as its child(ren)
*/
function append_annotate_results(objresponse){
  //Get all types of ids from the results, e.g. uniprot_id, wikipathways_id
  types = Object.keys(objresponse);
  // empty the div first
  $("#result-list").empty();
  // loop through each of the id_type, add as a collapsible list in 'id-list' div
  for (var i=0; i<types.length; i++){
    var dom_id1 = "#collapse" + i
    var domid = 'collapse' + i
    var domid1 = 'collapse_' + i
    ids = objresponse[types[i]];
    $("#result-list").append("<div class='panel-heading'><h4 class='panel-title'><a data-toggle='collapse' href=" + dom_id1
      + ">"+ types[i] + " (" +  ids.length + ")" + "</h4></div><div id=" + domid + " class='panel-collapse collapse'><ul class='list-group' id=" + types[i] + "></ul></div>");
    // loop through each id under a specific id_type, add as a list under the 'id_type' collapsible list
    
    for (var j=0; j<ids.length; j++){
      var dom_id = "#" + types[i];
      /*
      $(dom_id).append("<li class='list-group-item'>" + ids[j] + "</li>")
      */
      $(dom_id).append("<li class='list-group-item'> <label class='form-check-label'><input class='form-check-input' value=" + ids[j][0] + " type='checkbox'>" + ids[j][1] + "</label>")
    };
  };
}

function find_relation_type_from_id(objresponse, _id){
  types = Object.keys(objresponse);
  //THE FIRST CHARACTER IS EMPTY SPACE
  _id = _id.substr(1);;
  for (var i=0; i<types.length; i++){
    ids = objresponse[types[i]];
    for (var j=0; j<ids.length; j++){
      console.log(ids[j][1]);
      if (_id == ids[j][1]){
        return([_id, types[i], ids[j][0]])
      }
    }
  }
}

/*
This function only deal with the 'results' div,
It is designed to display the query results from the backend onto the 'results' div
The JSON doc from annotate results only include ids from the query result.
The function frist create a select
then for each id, include under the select as an option
*/
function append_query_results(objresponse){
  var ids = objresponse['ids'];
  //clean the result div         
  $("#result-list").empty();
  $("addAllButton").remove();
  $("#pagination").twbsPagination('destroy');
  //append a select section to the 'result-list' div
  $("#result-list").append('<div class="panel panel-default"><select class="select-container" multiple id ="candidate" name="selections"></select></div>');
  //add pagination, each page displaying 10 records,
  $('#pagination').twbsPagination({
      totalPages: Math.ceil(ids.length/10),
      visiblePages: 3,
      prev: '<<',
      next: '>>',
      onPageClick: function (event, page) {
        $("#candidate").empty();
        for (var i=(page*10-10); i<page*10; i++){
          if (i<ids.length){
            id_escape = ids[i].replace('>', "&gt;");
            $("#candidate").append("<option class='list-group-item variant-selections' value=" + id_escape + ">" + ids[i] + "</option>")
          }
        };
      }
    });
  $("#result-list").prepend('<h4> Total number of IDs found: ' + ids.length + '</h4>')
  // append an 'addallbutton'
  $("#result-list").append('<button id="addAllButton" type="submit" class="btn btn-primary">Add all</button>'); 
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
  $("#explorerButton").on('mouseover', 'node', function(evt) {
    $("#explorerButton").qtip({
    content: 'Click to explorer how to connect between two ids, e.g. the path between hgvs_id and drugbank_id',
    hide: {
        event: 'mouseout unfocus'
    },
    position: {
        target: 'mouse'
    },
    style: {
      classes: 'tooltipDefault',
      }
    });
  })
      $(document).ready(function() {
                    // Match all link elements with href attributes within the content div
                    $('#explorerButton').qtip({
                            content: 'Click to explorer how to connect between two ids, e.g. the path between hgvs_id and drugbank_id',
                            style: {
                              classes: 'qtip-bootstrap',
                              tip: {
                                width: 16,
                                height: 8
                              }
                            },
                            position: {
                              my: 'top center',
                              at: 'bottom center'
                            }
                        });
                    });
