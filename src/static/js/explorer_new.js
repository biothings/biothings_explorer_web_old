/*
Add Checkbox
*/
function addCheckBox(_val) {
    var template = '<p><label><input type="checkbox" /><span>{value}</span></label></p>'
    return template.replace('{value}', _val)
}

/*
Display Sankey Plot for paths connecting two semantic types
*/
function displaySemanticType(_input, _output) {
    findPathBetweenTwoSemanticTypes(_input, _output).done(function(jsonResponse){
        $("#error-message").hide();
        drawSankeyPlot(jsonResponse, type='path');
        input_ids = jsonResponse['inputs'];
        output_ids = jsonResponse['outputs'];
        apis = jsonResponse['api'];
        predicates = jsonResponse['predicates']
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
        $("#DownloadCodeButton").hide();
        Plotly.purge('path-plotly');
        $(".error").html('<h2 class="center">' + err.responseJSON['error message'].replace('\n', '<br />') + '</h2>')
    });
};

/**
 * Display Sankey Plot for the Paths Connecting Input and Output
 * @return {Sankey Plot}
*/
function displayIDTypePath(_input, _output, max_api) {
    findStartEndConnection(_input, _output, max_api).done(function(jsonResponse){
        $("#error-message").hide();
        drawSankeyPlot(jsonResponse, type="path");
        $("#DownloadCodeButton").show();
        $("#DownloadCodeButton").click(function() {
            download_file('bt_explorer_code_id_connect.py', construct_id_connect_text(_input, _output, max_api), 'text/plain');
        });
    }).fail(function (err) {
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
    $(".overlay-group").show();
    $(".search-bar-center").removeClass("search-bar-center");
    $(".search-history").show();
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


/*
Example 1 event handler
*/
function example1handler() {
    $("#example1-button").click(function() {
        //$("#semanticswitchid").trigger("click");
        $("#cy").show();
        $("#semanticswitchid").prop("checked", true);
        semanticIDSwitchHandler();
        var _input = $("#direct-input").find("option:selected").attr('value');
        $("#direct-input").empty();
        populateBioEntity("#direct-input", "hgnc.symbol");
        $("#direct-output").empty();
        populateBioEntity("#direct-output", "chembl.compound");
        $(".checkboxrow").show();
        $("#singleswitchmulti").prop("checked", false);
        $("#synonymcheckbox").prop("checked", false);
        $("#isIDSelected").prop("checked", true);
        $(".userinputrow").toggle(true);
        $(".input-field label").css("opacity", "0");
        $("#textarea1").val("CXCR4");
        $(".example").hide();
        //$(".metadata").show();
        $(".navigation").show();
        DirectOutput2Graph('hgnc.symbol', 'chembl.compound', 'CXCR4');
    });
};

/*
Example 2 event handler
*/
function example2handler() {
    $("#example2-button").click(function() {
        //$("#semanticswitchid").trigger("click");
        $("#semanticswitchid").prop("checked", true);
        var _input = $("#direct-input").find("option:selected").attr('value');
        $("#direct-input").empty();
        populateBioEntity("#direct-input", "hgnc.symbol");
        $("#crawlercheckbox").prop("checked", true);
        $(".select-wrapper-output").hide();
        $(".forwardicon").hide();
        $(".checkboxrow").show();
        $("#singleswitchmulti").prop("checked", false).attr("disabled", true);
        $("#synonymcheckbox").prop("checked", true).attr("disabled", true);
        $("#isIDSelected").prop("checked", true).attr("disabled", true);
        $(".userinputrow").toggle(true);
        $(".input-field label").css("opacity", "0");
        $("#textarea1").val("CDK7");
        $(".example").hide();
        //$(".metadata").show();
        $(".crawler").show();
        displayCrawlerResults("hgnc.symbol", "CDK7");
    });
};

/*
Example 3 event handler
*/
function example3handler() {
    $("#example3-button").click(function() {
        //$("#semanticswitchid").trigger("click");
        $("#cy").show();
        $("#semanticswitchid").prop("checked", true);
        semanticIDSwitchHandler();
        var _input = $("#direct-input").find("option:selected").attr('value');
        $("#direct-input").empty();
        populateBioEntity("#direct-input", "mondo");
        $("#direct-output").empty();
        populateBioEntity("#direct-output", "hp");
        $(".checkboxrow").show();
        $("#singleswitchmulti").prop("checked", false);
        $("#synonymcheckbox").prop("checked", false);
        $("#isIDSelected").prop("checked", true);
        $(".userinputrow").toggle(true);
        $(".input-field label").css("opacity", "0");
        $("#textarea1").val("MONDO:0009101");
        $(".example").hide();
        //$(".metadata").show();
        $(".navigation").show();
        DirectOutput2Graph('mondo', 'hp', 'MONDO:0009101');
    });
};


/*
Example 4 event handler
*/
function example4handler() {
    $("#example4-button").click(function() {
        //$("#semanticswitchid").trigger("click");
        $("#semanticswitchid").prop("checked", false);
        semanticIDSwitchHandler();
        var _input = $("#direct-input").find("option:selected").attr('value');
        defaultsearchbarsetting();
        $(".example").hide();
        //$(".metadata").show();
        $(".metadata").show();
        displaySemanticType("gene", "chemical");
    });
};

/*
Back to Default Search Bar setting
*/
function defaultsearchbarsetting() {
    $("#semanticswitchid").prop("checked", false);
    $("#direct-input").empty();
    populateSemanticType("#direct-input", "gene");
    $("#direct-output").empty();
    populateSemanticType("#direct-output", "chemical");
    $(".checkboxrow").hide();
    $("#singleswitchmulti").prop("checked", false).removeAttr("disabled");
    $("#synonymcheckbox").prop("checked", false).removeAttr("disabled");
    $("#isIDSelected").prop("checked", false).removeAttr("disabled");
    $("#crawlercheckbox").prop("checked", false);
    $(".userinputrow").toggle(false);
    $("#textarea1").val("");
    $(".input-field label").css("opacity", "1");
    $(".select-wrapper-output").show();
    $(".forwardicon").show();

}

/*
Back to Example Handler
*/
function back2examplehandler() {
    $("#showexamplebutton").click(function() {
        defaultsearchbarsetting();
        $(".metadata").hide();
        $(".navigation").hide();
        $(".example").show();
        $(".crawler").hide();
    })
};








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
            // show the text input area
            $(".div-input-value").show();
            // restructure the search bar grid
            $(".searchbar").addClass("searchbar-withid");
        } else {
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
    example1handler();
    example3handler();
    example4handler();
    example2handler();
    back2examplehandler();
    // when user switch between semantic type and ID, repopulate the "select" options
    semanticIDSwitchHandler();
    // pop up the text input bar when user select they have an ID
    $('#isIDSelected').click(function() {
        $(".userinputrow").toggle(this.checked);
    });

    // hide output select when user chose crawler
    $("#crawlercheckbox").change(function() {
        if ($("#crawlercheckbox").is(":checked")) {
            // when crawler is selected, other options should be disabled
            $(".select-wrapper-output").hide();
            $(".userinputrow").toggle(this.checked);
            $("#isIDSelected").prop('checked', true).attr("disabled", true);
            $("#synonymcheckbox").prop('checked', true).attr("disabled", true);
            $("#singleswitchmulti").attr("disabled", true);
            $("#textarea1").val("");
            $("#textarea1").prop("placeholder", "A valid ID must be provided to use crawler function. Please type your ID here!");
            $(".forwardicon").hide();
            $(".input-field label").css("opacity", "0");
        } else {
            // when crawler is not selected, other options should be re-enabled
            $(".select-wrapper-output").show();
            $(".forwardicon").show();
            $(".userinputrow").prop('checked', false).toggle(this.checked);
            $("#isIDSelected").prop('checked', false).removeAttr("disabled");
            $("#synonymcheckbox").prop('checked', false).removeAttr("disabled");
            $("#singleswitchmulti").removeAttr("disabled");
            $("#semanticswitchid").removeAttr("disabled");
            $("#textarea1").val("");
            $("#textarea1").prop("placeholder", "Type your Input ID or name here");
            $(".input-field label").css("opacity", "1");
        }
    });


    //handle graph display after user submit query
    $("#explorebutton").click(function() {
        $(".dropdown-trigger").dropdown();
        // hide example section temporarily
        $(".example").hide();
        // hide all graph display sections temporarily
        $(".metadata").hide();
        $(".crawler").hide();
        $(".navigation").hide();
        $(".error").hide();
        var input_semantic_type = $("#select-input-semantic").find("option:selected").attr('value');
        var output_semantic_type = $("#select-output-semantic").find("option:selected").attr('value');
        var input_id_type = $("#select-input-id").find("option:selected").attr('value');
        var output_id_type = $("#select-output-id").find("option:selected").attr('value');
        var input_value = $("#textarea1").val();
        var max_api = $("#select-num-api").find("option:selected").attr("value");
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
                    return "id2id"
                }
            }
        } else {
            if (input_id_type == "all") {
                if (output_id_type == "all") {
                    $(".metadata").show();
                    displaySemanticType(input_semantic_type, output_semantic_type);
                } else {

                }
            } else {
                if (output_id_type == "all") {

                } else {
                    $(".metadata").show();
                    console.log(max_api);
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
        }
    });
});