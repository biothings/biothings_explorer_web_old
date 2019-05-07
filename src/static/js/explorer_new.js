/*
Add Checkbox
*/

function myFunction() {
    var x = document.getElementById("myTopnav");
    if (x.className === "topnav") {
        x.className += " responsive";
    } else {
        x.className = "topnav";
    }
}


function addCheckBox(_val) {
    var template = '<p><label><input type="checkbox" /><span>{value}</span></label></p>'
    return template.replace('{value}', _val)
}

/*
Display Sankey Plot for paths connecting two semantic types
*/
function displaySemanticType(_input, _output) {
    $(".back_to_example").show();
    $(".preloader").show();
    findPathBetweenTwoSemanticTypes(_input, _output).done(function(jsonResponse){
        $(".preloader").hide()
        $(".error").hide();
        $(".download").show();
        $(".metadata").show();
        drawSankeyPlot(jsonResponse, type='path');
        input_ids = jsonResponse['inputs'];
        output_ids = jsonResponse['outputs'];
        apis = jsonResponse['api'];
        predicates = jsonResponse['predicates'];
        for (var bioentity_id in input_ids) {
            $(".filter-input .filters").append(addCheckBox(input_ids[bioentity_id]));
        };
        for (var bioentity_id in output_ids) {
            $(".filter-output .filters").append(addCheckBox(output_ids[bioentity_id]));
        };
        for (var api_id in apis) {
            $(".filter-api .filters").append(addCheckBox(apis[api_id]));
        };
        for (var predicate_id in predicates) {
            $(".filter-predicate .filters").append(addCheckBox(predicates[predicate_id]));
        };
        $("#DownloadCodeButton").show();
        $("#DownloadCodeButton").click(function() {
            download_file('bt_explorer_code_semantic_connect.py', construct_semantic_connect_text(_input, _output), 'text/plain');
        });
    }).fail(function (err) {
        $(".metadata").hide();
        $(".error").show();
        $(".error").empty();
        $(".download").hide();
        $(".preloader").hide();
        Plotly.purge('path-plotly');
        $(".error").html('<h2 class="center">' + err.responseJSON['error message'].replace('\n', '<br />') + '</h2>')
    });
};

/**
 * Display Sankey Plot for the Paths Connecting Input and Output
 * @return {Sankey Plot}
*/
function displayIDTypePath(_input, _output, max_api) {
    $(".back_to_example").show();
    findStartEndConnection(_input, _output, max_api).done(function(jsonResponse){
        $("#error-message").hide();
        drawSankeyPlot(jsonResponse, type="path");
        $(".download").show();
        $("#DownloadCodeButton").click(function() {
            download_file('bt_explorer_code_id_connect.py', construct_id_connect_text(_input, _output, max_api), 'text/plain');
        });
    }).fail(function (err) {
        $(".download").hide();
        $(".metadata").hide();
        $(".error").show();
        $(".error").empty();
        Plotly.purge('path-plotly');
        $(".error").html('<h2 class="center">' + err.responseJSON['error message'].replace('\n', '<br />') + '</h2>')
    });
};

/**
 * Display Sankey Plot for the Paths Connecting Input and Output
 * @return {Sankey Plot}
*/
function displaySemantic2IDTypePath(_input, _output, max_api) {
    findSemantic2IDConnection(_input, _output, max_api).done(function(jsonResponse){
        $("#error-message").hide();
        drawSankeyPlot(jsonResponse, type="path");
        input_ids = jsonResponse['inputs'];
        output_ids = jsonResponse['outputs'];
        apis = jsonResponse['apis'];
        nodes = jsonResponse['nodes'];
        predicates = jsonResponse['predicates'];
        for (var bioentity_id in input_ids) {
            $(".filter-input .filters").append(addCheckBox(input_ids[bioentity_id]));
        };
        for (var predicate_id in predicates) {
            $(".filter-predicate .filters").append(addCheckBox(predicates[predicate_id]));
        };
        for (var api_id in apis) {
            $(".filter-api .filters").append(addCheckBox(apis[api_id]));
        };
        for (var bioentity_id in nodes) {
            $(".filter-output .filters").append(addCheckBox(nodes[bioentity_id]));
        };
        $(".download").show();
        $("#DownloadCodeButton").click(function() {
            download_file('bt_explorer_code_id_connect.py', construct_id_connect_text(_input, _output, max_api), 'text/plain');
        });
    }).fail(function (err) {
        $(".download").hide();
        $(".metadata").hide();
        $(".error").show();
        $(".error").empty();
        Plotly.purge('path-plotly');
        $(".error").html('<h2 class="center">' + err.responseJSON['error message'].replace('\n', '<br />') + '</h2>')
    });
};

/*
Display crawler results
*/
function displayCrawlerResults(input_prefix, _input) {
    update_data_display(input_prefix, _input);
    $(".collapsible").collapsible();
}

/*
Display options based on semantic & ID switch
*/

function semanticIDSwitchHandler() {
    $("#semanticswitchid").change(function() {
        var $input = $(this);
        if ($input.prop("checked")) {
            $("#direct-input").empty();
            populateBioEntity("#direct-input", "hgnc.symbol");
            $("#direct-output").empty();
            populateBioEntity("#direct-output", "chembl.compound");
            // checkbox row should be hidden when user select semantic type level search
            $(".checkboxrow").show();
        } else {
            defaultsearchbarsetting();
        }
    });
};

function setSelectedOption(input_semantic_type, output_semantic_type, input_id_type, output_id_type, max_api, input_value) {
    $("#select-input-semantic").val(input_semantic_type).trigger('change');
    $("#select-output-semantic").val(output_semantic_type).trigger('change');
    setTimeout(function() {
        $("#select-input-id").val(input_id_type).trigger("change");
    }, 100);
    $("#select-num-api").val(max_api).trigger('change');
    setTimeout(function() {
        $("#select-output-id").val(output_id_type).trigger('change');
    }, 100);
    console.log(input_semantic_type, output_semantic_type, input_id_type, output_id_type);
    if (input_value) {
        $("#hasidswitch").prop('checked', true);
        $("#textarea1").val(input_value);
        $(".forward-icon").addClass("forward-icon-withid");
        // show the text input area
        $(".div-input-value").show();
        // restructure the search bar grid
        $(".searchbar").addClass("searchbar-withid");
    } else {
        $(".hint").empty();
        $("#textarea1").val("");
        $(".div-input-value").hide();
        $(".searchbar").removeClass("searchbar-withid");
        $(".forward-icon").removeClass("forward-icon-withid");
    }
};
/*
Example 1 event handler
*/
function example1handler() {
    $("#example1-button").click(function() {
        setSelectedOption('gene', 'chemical', 'hgnc.symbol', 'chembl.compound', '1', 'CXCR4');
        $(".example").hide();
        DirectOutput2Graph('hgnc.symbol', 'chembl.compound', 'CXCR4');
    });
};

/*
Example 2 event handler
*/
function example2handler() {
    $("#example2-button").click(function() {
        setSelectedOption('gene', 'all', 'hgnc.symbol', 'all', '1', 'CDK7');
        $(".example").hide();
        displayCrawlerResults("hgnc.symbol", "CDK7");
    });
};

/*
Example 3 event handler
*/
function example3handler() {
    $("#example3-button").click(function() {
        setSelectedOption('disease', 'phenotype', 'mondo', 'hp', '1', 'MONDO:0009101');
        $(".example").hide();
        DirectOutput2Graph('mondo', 'hp', 'MONDO:0009101');
    });
};


/*
Example 4 event handler
*/
function example4handler() {
    $("#example4-button").click(function() {
        setSelectedOption("gene", "chemical", "all", "all", "1", null);
        $(".example").hide();
        displaySemanticType("gene", "chemical");
    });
};


/*
Back to Example Handler
*/
function back2examplehandler() {
    $(".back_symbol").click(function() {
        $(".back_to_example").hide();
        $(".metadata").hide();
        $(".navigation").hide();
        $(".example").show();
        $(".crawler").hide();
        $(".error").hide();
    })
};

/*
Handle when user clicked on one of the log record 
*/
function logHandler() {
    $(".log-record").click(function() {
        $(".dropdown-trigger").dropdown();
        // hide example section temporarily
        $(".example").hide();
        // hide all graph display sections temporarily
        $(".metadata").hide();
        $(".crawler").hide();
        $(".navigation").hide();
        $(".error").hide();
        var input_semantic_type = $(this).attr('input_semantic_type');
        var output_semantic_type = $(this).attr('output_semantic_type');
        var input_id_type = $(this).attr('input_id_type');
        var output_id_type = $(this).attr('output_id_type');
        var input_value = $(this).attr('input_value');
        var max_api = $(this).attr('max_api');
        if (input_value) {
            if (input_id_type == "all") {
                if (output_id_type == "all") {
                    return "semantic2semantic"
                } else {
                    return "semantic2id"
                }
            } else {
                if (output_id_type == "all") {
                    return "id2semantic"
                } else {
                    DirectOutput2Graph(input_id_type, output_id_type, input_value);
                }
            }
        } else {
            if (input_id_type == "all") {
                if (output_id_type == "all") {
                    displaySemanticType(input_semantic_type, output_semantic_type);
                } else {

                }
            } else {
                if (output_id_type == "all") {

                } else {
                    $(".metadata").show();
                    displayIDTypePath(input_id_type, output_id_type, max_api);
                }
            }

        }

    })
}
/*
Display hint to users based on select
*/
function displayHint(hint_text) {
    $(".search-item").change(function() {
        $(".hint").empty();
        var input_semantic_type = $("#select-input-semantic").find("option:selected").attr('value');
        var output_semantic_type = $("#select-output-semantic").find("option:selected").attr('value');
        var input_id_type = $("#select-input-id").find("option:selected").attr('value');
        var output_id_type = $("#select-output-id").find("option:selected").attr('value');
        var input_value = $("#textarea1").val();
        var max_api = $("#select-num-api").find("option:selected").attr("value");
        if (input_value) {
            if (input_id_type == "all") {
                var hint_text = "<span>Warning: You must select an Input ID type!</span>";
                $(".hint").append(hint_text);
                $(".hint").css('color', 'red');
                $(".hint").css('font-size', '1.6rem');
            } else {
                $(".hint").css('color', '#f9843b');
                $(".hint").css('font-size', '1.1rem');
                if (output_semantic_type == "all") {
                    var hint_text = "<span>Hint: You are now searching for all information related to " + input_id_type + ":" + input_value + "!</span>";
                    $(".hint").append(hint_text);
                } else {
                    if (output_id_type == "all") {
                        var hint_text = "<span>Hint: You are now searching for all " + output_semantic_type + "-centric information related to " + input_id_type + ":" + input_value + "!</span>";
                        $(".hint").append(hint_text);
                    } else {
                        var hint_text = "<span>Hint: You are now searching for all " + output_semantic_type + "s in the form of " + output_id_type + " which are related to " + input_id_type + ":" + input_value + "!</span>";
                        $(".hint").append(hint_text);
                    }
                }

            }
        } else {
            $(".hint").css('color', '#f9843b');
            $(".hint").css('font-size', '1.1rem');
            if (input_id_type == "all") {
                if (output_id_type == "all") {
                    var hint_text = "<span>Hint: You are now searching for paths (chained by at most " + max_api + " APIs) connecting from All available " + input_semantic_type + ' IDs to All available ' + output_semantic_type + ' IDs!</span>';
                    $(".hint").append(hint_text);
                } else {
                    var hint_text = "<span>Hint: You are now searching for paths (chained by at most " + max_api + " APIs) connecting from All available " + input_semantic_type + ' IDs to ' + output_id_type + '!</span>';
                    $(".hint").append(hint_text);
                }
            } else {
                if (output_id_type == "all") {
                    var hint_text = "<span>Hint: You are now searching for paths (chained by at most " + max_api + " APIs) connecting from " + input_id_type + ' to All available ' + output_semantic_type + ' IDs!</span>';
                    $(".hint").append(hint_text);
                } else {
                    var hint_text = "<span>Hint: You are now searching for paths (chained by at most " + max_api + " APIs) connecting from " + input_id_type + ' to ' + output_id_type + '!</span>';
                    $(".hint").append(hint_text);
                }
            }
        };
        $(".hint span").css("background-color", "yellow");
        setTimeout(function() {
            $(".hint span").css("background-color", "transparent");
        }, 500);
    })
}


function validateInputValue(input_id_type, input_value) {
    var promise = $.ajax({
        type: "GET",
        url: "/explorer/api/v2/registry",
        data: {prefix: input_id_type},
        datatype: "json"
    });
    return promise;
    promise.done(function(jsonResponse) {
        var pattern = jsonResponse['pattern'];
        var example = jsonResponse['example'];
        if (input_value.match(pattern)) {
            return 'valid'
        } else {
            var error_message = 'Your input value ' + input_value + ' is not valid. A valid example of ' + input_id_type + 'is: ' + example;
            return error_message
        }
    })
}

LOG_NUM = 1;
/* Add Record to Log After User Hit Submit */
function addRecordToLog(input_semantic_type, output_semantic_type, input_id_type, output_id_type, max_api, input_value) {
    
    if (input_value) {
            if (input_id_type == "all") {

            } else {
                if (output_semantic_type == "all") {
                    var log_text = "Find all information related to " + input_id_type + ":" + input_value + "!";
                } else {
                    if (output_id_type == "all") {
                        var log_text = "Find all " + output_semantic_type + "-centric information related to " + input_id_type + ":" + input_value + "!";
                    } else {
                        var log_text = "Find all " + output_semantic_type + "s in the form of " + output_id_type + " which are related to " + input_id_type + ":" + input_value + "!";
                    }
                }

            }
        } else {
            if (input_id_type == "all") {
                if (output_id_type == "all") {
                    var log_text = "Find all paths (chained by at most " + max_api + " APIs) connecting from All available " + input_semantic_type + ' IDs to All available ' + output_semantic_type + ' IDs!';
                } else {
                    var log_text = "Find all paths (chained by at most " + max_api + " APIs) connecting from All available " + input_semantic_type + ' IDs to ' + output_id_type + '!';
                }
            } else {
                if (output_id_type == "all") {
                    var log_text = "Find all paths (chained by at most " + max_api + " APIs) connecting from " + input_id_type + ' to All available ' + output_semantic_type + ' IDs!';
                } else {
                    var log_text = "Find all paths (chained by at most " + max_api + " APIs) connecting from " + input_id_type + ' to ' + output_id_type + '!';
                }
            }

        }
    var record = "<span class='log-record' input_semantic_type=" + input_semantic_type + " output_semantic_type="
                + output_semantic_type + " input_id_type=" + input_id_type + " output_id_type=" + output_id_type
                + " max_api=" + max_api + " input_value=" + input_value + ">" + LOG_NUM + ". " + log_text + "</span><hr>";
    LOG_NUM += 1;
    $(".log-collapsible-body").append(record);
    $(".collapsible").collapsible();
}






$(document).ready(function() {
    //$('select').formSelect();
    $('.tooltipped').tooltip();
    //populate the select bar
    populateSemanticType("#select-input-semantic", "gene");
    populateSemanticType("#select-output-semantic", "chemical", true);
    populateBioEntity("#select-input-id", null, "gene");
    populateBioEntity("#select-output-id", null, "chemical");
    $("#select-num-api").select2();
    $("#hasidswitch").change(function() {
        if ($("#hasidswitch").is(":checked")) {
            // change the forward icon position
            $(".forward-icon").addClass("forward-icon-withid");
            $("#textarea1").val(null);
            // show the text input area
            $(".div-input-value").show();
            // restructure the search bar grid
            $(".searchbar").addClass("searchbar-withid");
        } else {
            $(".hint").empty();
            $("#textarea1").val(null);
            $(".div-input-value").hide();
            $(".searchbar").removeClass("searchbar-withid");
            $(".forward-icon").removeClass("forward-icon-withid");
        }
    });

    // change the select of input IDs by changing semantic types
    $("#select-input-semantic").change(function() {
        var _input_semantic = $("#select-input-semantic").find("option:selected").attr('value');
        populateBioEntity("#select-input-id", null, _input_semantic);
    });
    // change the select of output IDs by changing semantic types
    $("#select-output-semantic").change(function() {
        var _output_semantic = $("#select-output-semantic").find("option:selected").attr('value');
        populateBioEntity("#select-output-id", null, _output_semantic);
    });
    displayHint();
    example1handler();
    example3handler();
    example4handler();
    example2handler();
    back2examplehandler();
    // hide output id select and disable max——api when user select "all semantic types"
    $("#select-output-semantic").change(function() {
        if ($("#select-output-semantic").find("option:selected").attr("value") == "all") {
            $(".div-output-id").hide();
            $("#select-num-api").prop("disabled", "disabled");
        } else {
            $(".div-output-id").show();
            $("#select-num-api").prop("disabled", false);
        }
    });

    //handle graph display after user submit query
    $("#explorebutton").click(function() {
        // get user input from the search bar
        var input_semantic_type = $("#select-input-semantic").find("option:selected").attr('value');
        var output_semantic_type = $("#select-output-semantic").find("option:selected").attr('value');
        var input_id_type = $("#select-input-id").find("option:selected").attr('value');
        var output_id_type = $("#select-output-id").find("option:selected").attr('value');
        var input_value = $("#textarea1").val();
        var max_api = $("#select-num-api").find("option:selected").attr("value");
        if (input_value) {
            validateInputValue(input_id_type, input_value).done(function(jsonResponse) {
                var pattern = jsonResponse['pattern'];
                var example = jsonResponse['example'];
                if (input_value.match(pattern)) {
                    $(".example").hide();
                    $(".log").show();
                    $(".dropdown-trigger").dropdown();
                    // hide example section temporarily
                    // hide all graph display sections temporarily
                    $(".metadata").hide();
                    $(".crawler").hide();
                    $(".navigation").hide();
                    $(".error").hide();
                    addRecordToLog(input_semantic_type, output_semantic_type, input_id_type, output_id_type, max_api, input_value);
                    if (input_id_type == "all") {
                        if (output_id_type == "all") {
                            return "semantic2semantic"
                        } else {
                            return "semantic2id"
                        }
                    } else {
                        if (output_semantic_type == "all") {
                            displayCrawlerResults(input_id_type, input_value);
                        } else {
                            if (output_id_type == "all") {
                                return "id2semantic"
                            } else {
                                //DirectOutput2Graph(input_id_type, output_id_type, input_value);
                                MultiEdge2Graph(input_id_type, output_id_type, input_value, max_api);
                            } 
                        }
                    }
                } else {
                    $(".download").hide();
                    $(".example").hide();
                    $(".metadata").hide();
                    $(".navigation").hide();
                    $(".crawler").hide();
                    $(".back_to_example").show();
                    $(".error").show();
                    $(".error").empty();
                    Plotly.purge('path-plotly');
                    var error_message = 'Your input value "<b>' + input_value + '</b>" is not valid. A valid example of ' + input_id_type + ' is: ' + example;
                    $(".error").html('<h2 class="center">' + error_message + '</h2>');
                    $(".hint").empty();
                    $(".hint").append('<span>' + error_message + '</span>');
                    $(".hint span").css("background-color", "red");
                    $(".hint span").css("font-size", '1.5rem');
                    setTimeout(function() {
                        $(".hint span").css("background-color", "transparent");
                    }, 1000)
                }
            })
        } else {
            $(".example").hide();
            $(".log").show();
            $(".dropdown-trigger").dropdown();
            // hide example section temporarily
            // hide all graph display sections temporarily
            $(".metadata").hide();
            $(".crawler").hide();
            $(".navigation").hide();
            $(".error").hide();
            addRecordToLog(input_semantic_type, output_semantic_type, input_id_type, output_id_type, max_api, input_value);
            if (input_id_type == "all") {
                if (output_id_type == "all") {
                    displaySemanticType(input_semantic_type, output_semantic_type);
                } else {
                    $(".metadata").show();
                    displaySemantic2IDTypePath(input_semantic_type, output_id_type, max_api);
                }
            } else {
                if (output_id_type == "all") {

                } else {
                    $(".metadata").show();
                    displayIDTypePath(input_id_type, output_id_type, max_api);
                }
            }
        }
            
        // First handle cases for semantic type metadata exploration
        if ($("#semanticswitchid").is(":checked") == false) {
            //$(".metadata").show();
            //var _input = $("#select-input-semantic").find("option:selected").attr('value');
            //var _output = $("#select-output-semantic").find("option:selected").attr('value');
            //displaySemanticType(_input, _output);
        } else {
            if ($("#crawlercheckbox").is(":checked")) {
                $(".crawler").show();
                var _input = $("#direct-input").find("option:selected").attr('value');
                var _value = $("#textarea1").val();
                displayCrawlerResults(_input, _value);
            // handle cases for metadata search
            } else if ($("#isIDSelected").is(":checked") == false) {
                $(".metadata").show();
                var _input = $("#direct-input").find("option:selected").attr('value');
                var _output = $("#direct-output").find("option:selected").attr('value');
                if ($("#singleswitchmulti").is(":checked") == false) { 
                    displayIDTypePath(_input, _output, 1);
                } else {
                    displayIDTypePath(_input, _output, 3);
                }
            } else if ($("#isIDSelected").is(":checked")) {
                if ($("#singleswitchmulti").is(":checked") == false && $("#synonymcheckbox").is(':checked') == false) {
                    $(".navigation").show();
                    $("#cy").show();
                    var _input = $("#direct-input").find("option:selected").attr('value');
                    var _output = $("#direct-output").find("option:selected").attr('value');
                    var _value = $("#textarea1").val();
                    DirectOutput2Graph(_input, _output, _value);
                }
            }
        };
        logHandler();
    });


});
