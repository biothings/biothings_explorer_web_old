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


$(document).ready(function() {
    $('.tooltipped').tooltip();
    //populate the select bar
    populateSemanticType("#direct-output");
    populateSemanticType("#direct-input");
    $("#direct-output").select2();
    $("#direct-output").val('gene').trigger('change');
    // when user switch between semantic type and ID, repopulate the "select" options
    $("#semanticswitchid").change(function() {
        var $input = $(this);
        if ($input.prop("checked")) {
            $("#direct-input").empty();
            populateBioEntity("#direct-input");
            $("#direct-output").empty();
            populateBioEntity("#direct-output");
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
    // pop up the text input bar when user select they have an ID
    $('#isIDSelected').click(function() {
        $(".userinputrow").toggle(this.checked);
    });

    //handle graph display after user submit query
    $("#explorebutton").click(function() {
        $(".example").hide();
        //$(".metadata").show();
        $(".navigation").show();
        var _input = $("#direct-input").find("option:selected").attr('value');
        var _output = $("#direct-output").find("option:selected").attr('value');
        var _value = $("#textarea1").val();
        //displaySemanticType(_input, _output);
        //DirectOutput2Graph(_input, _output, _value);
        SemanticOutput2Graph(_input, _output, _value);
    })
});