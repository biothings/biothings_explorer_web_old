"use strict";
// the stylesheet for the graph
var color_list = ["red", "blue", "green", "yellow"];
var concentric_style = [
    {
        selector: "node",
        style: {
            "height": 20,
            "width": 20,
            "background-color": function (ele) {
                return color_list[parseInt(ele.data("level"))];
            },
            "content": "data(id)"
        }
    },
    {
        selector: "edge",
        style: {
            "curve-style": "haystack",
            "haystack-radius": 0,
            "width": 5,
            "opacity": 0.5,
            "line-color": "#a2efa2", 
            "label": "data(label)"
        }
    }
];

//layout option for grid
// define concentric option
var concentricOptions = {
    name: "concentric",
    concentric: function (node) {
        return 10 - node.data("level");
    },
    levelWidth: function () {
        return 1;
    }
};

function extractPath () {
    var paths = [];
    $("#paths-list .collection-item").each(function (i, n) {
        paths.push($(n).text().replace(/Path[0-9]+: /g, "").split(" -> "));
    });
    return paths;
}

/**
 * Given a path, return all its subpaths;
 * Example input: ["a", "b", "c", "d", "e"]
 * Example Output: [["a", "b", "c"], ["c", "d", "e"]]
 * TODO: validate whether its valid path
*/
function findSubPath (path) {
    var path_length = path.length;
    var subPathList = [];
    var i = 0;
    while (i < path.length - 2) {
        subPathList.push(path.slice(i, i + 3));
        i = i + 2;
    };
    return subPathList;
}

/**
 * get the path as a list
*/
function getPath() {
    var _input_value = $("#input_value").val().split(",").map(function(item) { return item.trim(); });;
    var _path_id = parseInt($("#select-path").find("option:selected").attr("value"));
    var paths = extractPath();
    var selected_path = paths[_path_id];
    return [selected_path, _input_value]
}
/**
 * Display the connection between input and output based on selected path
 * return {Cytoscape graph}
*/
function displayOutputToCytoscape(selected_path, _input_value) {
    //extract value from input_value, and make it a list
    $("#log-list").empty();
    $("#log-list").show();
    $("#cy").empty();
    $("#paths-list").empty();
    var subpath = findSubPath(selected_path);
    var _level = 0;
    var sequence = Promise.resolve();
    var cy;
    $("#paths").hide();
    $("#log-list").append("<li class='collection-header'><h4>Your exploration starts now!</h4></li>")
    subpath.forEach(function(path) {
        sequence = sequence.then(function() {
        $("#log-list").append("<li class='collection-item'>" + "Step " + (_level + 1) + " STARTS: Connect from " + path[0] + " to " + path[2] + " using " + path[1] + ". The input value is " + _input_value + "</li>")
        var Response = findOutputBasedOnInputAndPath(_input_value, path, _level);
        return Response;
        }).then(function(jsonResponse) {
            $("#log-list").append("<li class='collection-item'>" + "Step " + (_level + 1) + " ENDS!" + "</li>")
            var parsedJson = $.parseJSON(jsonResponse);
            if (_level == 0) {
                cy = drawCytoscape("#cy", concentric_style, concentricOptions, parsedJson.cytoscape);
            } else {
                cy.add(parsedJson.cytoscape);
                cy.layout(concentricOptions);
            };
            _level = _level + 1;
            _input_value = parsedJson.output;
        });
    });
}