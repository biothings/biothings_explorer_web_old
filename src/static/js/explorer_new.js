/*
Display Sankey Plot for paths connecting two semantic types
*/
function displaySemanticType(_input, _output) {
    findPathBetweenTwoSemanticTypes(_input, _output).done(function(jsonResponse){
        $("#error-message").hide();
        drawSankeyPlot(jsonResponse, type='path');
        $("#DownloadCodeButton").show();
        $("#DownloadCodeButton").click(function() {
            download_file('bt_explorer_code_semantic_connect.py', construct_semantic_connect_text(_input, _output), 'text/plain');
        });
    }).fail(function (err) {
        $("#error-message").show();
        $("#DownloadCodeButton").hide();
        Plotly.purge('path-plotly');
        $("#error-message").html('<h2 class="center">' + err.responseJSON['error message'].replace('\n', '<br />') + '</h2>')
    });
};

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
            $("#direct-input").empty();
            populateSemanticType("#direct-input");
            $("#direct-output").empty();
            populateSemanticType("#direct-output");
            $(".checkboxrow").hide();
        }
    });
};


/*
Example 1 event handler
*/
function example1handler() {
    $("#example1-button").click(function() {
        //$("#semanticswitchid").trigger("click");
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
Example 3 event handler
*/
function example3handler() {
    $("#example3-button").click(function() {
        //$("#semanticswitchid").trigger("click");
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
    $("#singleswitchmulti").prop("checked", false);
    $("#synonymcheckbox").prop("checked", false);
    $("#isIDSelected").prop("checked", false);
    $(".userinputrow").toggle(false);
    $("#textarea1").val("");
    $(".input-field label").css("opacity", "1");
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
    })
};






$(document).ready(function() {
    $('.tooltipped').tooltip();
    //populate the select bar
    populateSemanticType("#direct-output", "gene");
    populateSemanticType("#direct-input", "chemical");
    example1handler();
    example3handler();
    example4handler();
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
            $("#semanticswitchid").attr("disabled", true);
            $("#textarea1").val("");
            $("#textarea1").prop("placeholder", "Type your Input ID or name here");
            $(".forwardicon").hide();
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
        }
    });


    //handle graph display after user submit query
    $("#explorebutton").click(function() {
        $(".example").hide();
        //$(".metadata").show();
        $(".navigation").show();
        var _input = $("#direct-input").find("option:selected").attr('value');
        console.log(_input);
        var _output = $("#direct-output").find("option:selected").attr('value');
        var _value = $("#textarea1").val();
        //displaySemanticType(_input, _output);
        DirectOutput2Graph(_input, _output, _value);
        //SemanticOutput2Graph(_input, _output, _value);
    })
});