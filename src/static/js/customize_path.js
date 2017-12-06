/**
 * Find the integer in a string
 * @return {integer value}
*/
function findIntInString(string_input) {
    return parseInt(string_input.match(/\d+/)[0]);
}

/**
 * Given an customize option id, return the type it belongs to
 * @return {value type, e.g. input, output, endpoint}
*/
function optionID2Type(option_id) {
    var id_num = findIntInString(option_id);
    if (id_num > 0) {
        if (id_num % 2 == 1) {
            return 'input';
        } else {
            return 'endpoint';
        } 
    } else {
        return 'not found';
    }
}

var ENDPOINT_SELECT_DIV = '<div class="select-wrapper"> <select disabled id="selectid" class="customizeoptions"> <option value="" disabled selected>Choose your option</option> </select> <label>labelname</label> </div>'
var OUTPUT_SELECT_DIV = '<div><div class="select-wrapper" style="display: inline-block;width: 80%"><select disabled id="selectid" class="customizeoptions"><option value="" disabled selected>Choose your option</option></select><label>labelname</label></div><i class="append-customize-select material-icons orange-text text-darken-2" id="iconid">add</i></div>'

/**
 * Add an endpoint select div to the customized div
*/
function addEndpointSelectDiv(selectid, labelname, _input) {
    var new_endpoint_div = ENDPOINT_SELECT_DIV.replace('selectid', selectid).replace('labelname', labelname);
    $(new_endpoint_div).insertBefore("#customizePathButton");
    $("#" + selectid).material_select();
    $("#"+selectid).prop("disabled", false);
    poplulateEndpointFromInput("#" + selectid, _input);
}
/**
 * Add an output select div to the customized div
*/
function addOutputSelectDiv(selectid, labelname, iconid) {
    var new_output_div = OUTPUT_SELECT_DIV.replace('selectid', selectid).replace('labelname', labelname).replace('iconid', iconid);
    $(new_output_div).insertBefore("#customizePathButton");
    $("#" + selectid).material_select();
}

/**
 * Display Sankey Plot for the selected Input
 * @return {Sankey Plot}
*/
function changeCustomizeOption() {
    $(".append-customize-select").hover(function() {
        $(this).css('cursor','pointer');
    });
    $(document).on("change", ".customizeoptions", function () {
        var option_id = $(this).attr('id');
        if (option_id) {
            var selected_value = $(this).find("option:selected").attr("value");
            var option_id_next = '#customize'
            var id_num = findIntInString(option_id);
            if (id_num > 0) {
                option_id_next = option_id_next + (id_num + 1).toString();
            } else {
                return ;
            };
            var type = optionID2Type(option_id);
            if (type == 'input') {
                $(option_id_next).prop("disabled", false);
                poplulateEndpointFromInput(option_id_next, selected_value);
            } else if (type == 'endpoint') {
                $(option_id_next).prop("disabled", false);
                populateOutputFromEndpoint(option_id_next, selected_value);
                $(".append-customize-select").prop("disabled",false);
            };
        };
    });
    $(".append-customize-select").click(function () {
        var icon_id = $(this).attr('id');
        var id_num = findIntInString(icon_id);
        var output_select_id = "customize" + (id_num + 4).toString();
        var endpoint_select_id = "customize" + (id_num + 3).toString();
        var output_label_name = "output " + (id_num + 1).toString() + "/input " + (id_num + 2).toString();
        var endpoint_label_name = "endpoint" + (id_num + 1).toString();
        var new_icon_id = "append" + (id_num + 1).toString();
        var output_value = $("#customize" + (id_num + 2).toString()).find("option:selected").attr("value");
        $(this).prev().css( "width", "94%" );
        $(this).remove();
        addEndpointSelectDiv(endpoint_select_id, endpoint_label_name, output_value);
        addOutputSelectDiv(output_select_id, output_label_name, new_icon_id);
    });
};

/**
Extract all the select from options, and construct into a path
*/
function constructCustomizePath(){
    var path = []
    $('select.customizeoptions').each(function() {
        path.push($(this).find("option:selected").attr("value"));
    });
    console.log(path);
    return path;
}

/**
 * display customized output to the graph
*/
function displayCustomizedOutput(){
    $("#customizePathButton").click(function(){
        var customized_path = constructCustomizePath();
        $("#explore-customize-path").show();
        $("#exploreCustomizePathButton").click(function(){
            var _input_value = $("#customized_input_value").val().split(",").map(function(item) { return item.trim(); });
            console.log(_input_value);
            displayOutputToCytoscape(customized_path, _input_value);
        });
    });
}