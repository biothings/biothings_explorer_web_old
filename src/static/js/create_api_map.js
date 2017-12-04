"use strict";
/**
 * Find the connection between start and end biological entity
 * @param {String} _start
 * @param {String} _end
 * @return {Promise} findStartEndConnection
*/

function findApiMap() {
    var promise = $.getJSON("http://localhost:8990/apimap");
    return promise;
}

// the stylesheet for the graph
var style = [
    {
        selector: "node[type = 'api']",
        style: {
            "background-color": "blue",
            "label": "data(id)",
            "height": 300,
            "width": 300,
            "font-size": "20px",
            "text-valign": "center",
            "text-halign": "center",
            "text-outline-color": "#555",
            "text-outline-width": "2px"
        }
    },
    {
        selector: "node[type = 'bio-entity']",
        style: {
            "background-color": "green",
            "label": "data(id)",
            "font-size": "1000px !important",
            "height": 50,
            "width": 50
        }
    },
    {
        selector: "node[type= 'endpoint']",
        style: {
            "background-color": "red",
            "label": "data(id)",
            "font-size": "30px",
            "height": 200,
            "width": 200
        }
    },
    {
        selector: "edge",
        style: {
            "curve-style": "haystack",
            "haystack-radius": 0,
            "width": 30,
            "opacity": 0.5,
            "line-color": "#a8eae5"
        }
    }
];

// define concentric option
var concentricOptions = {
    name: "concentric",
    concentric: function (node) {
        return 10 - node.data("level");
    },
    levelWidth: function () {
        return 1;
    },
    minNodeSpacing: 1,
    padding: -1
};


function draw_api_map() {
    findApiMap().done(function (jsonResponse) {
        drawCytoscape("#cy", style, concentricOptions, jsonResponse);
    });
}