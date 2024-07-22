var action;
var datjs;
var fieldjs;
var columnsjs;
var table_namejs;
var project_idjs;
var except;
var table_id;
var category_id;
var test_cycle_id;
var max_tids;


function addtext() {
    // Gets the result of the actual result dropdown menu
    var actualres = document.getElementById('actual_result').value;

    // The text area with id 'reasonforfail'should become visible if the actual result is 'Fail' so the test engineer
    // can type in the reason for failure, otherwise hide the textarea
    if (actualres == 'Fail') {
        document.getElementById('reasonforfail').style.display = 'block';
    }
    else {
        document.getElementById('reasonforfail').style.display = 'none';
    }
}

function CreateandAddTestCaseId() {
    var dynamicFormField = document.getElementById('testcaseidinputs');
    dynamicFormField.innerHTML = '';

    if ('whole_number_part' in max_tids[0]){
         // Create a label for the input field
        var label = document.createElement('label');
        label.textContent = 'Test Case ID';
        label.htmlFor = 'test_case_id';
        label.style.fontSize = '14px';
        label.className = 'control-label'; // Optional, for styling

        var selectField = document.createElement('select');
        selectField.className = 'form-control';
        selectField.id = 'test_case_id';
        selectField.name = 'Test Case ID';
        selectField.required = true;
        selectField.className = 'form-control'; // Add form-control class

        // Add default option
//        var defaultOption = document.createElement('option');
//        defaultOption.value = datjs[fieldjs[i]];
//        defaultOption.textContent = datjs[fieldjs[i]];
//        selectField.appendChild(defaultOption);

        // Append label and input field to the form group div
        dynamicFormField.appendChild(label);
        dynamicFormField.appendChild(selectField);
    }

    else if ('decimal_part' in max_tids[0]){
        // Create a label for the input field
        var label = document.createElement('label');
        label.textContent = 'Test Case ID';
        label.htmlFor = 'test_case_id';
        label.style.fontSize = '14px';
        label.className = 'control-label'; // Optional, for styling

        // Create an input field for version
        var inputField = document.createElement('input');
        inputField.type = 'number';
        inputField.id = 'test_case_id';
        inputField.step = 'any';  // Allow decimals
        inputField.name = 'Test Case ID';
        inputField.className = 'form-control'; // Add form-control class
//        inputField.value = datjs[fieldjs[i]];

        // Append label and input field to the form group div
        dynamicFormField.appendChild(label);
        dynamicFormField.appendChild(inputField);
    }
}

function getrowid(button, dat, field, columns, table_name, exception, project_id, tableid, categoryid, testcycleid, maxtid) {
    // The id of the 'edit' button, the id is dynamic as each edit button in the table should have separate id
    // Hence the reason why edit button's id is not hard coded in this script
    action = button.id;
    // Data of the row where edit was clicked
    datjs = dat

    // MySQL fields of the table
    fieldjs = field

    // Column headers (fields with spaces and each word capitalized)
    columnsjs = columns

    // Name of the table
    table_namejs = table_name

    // Project ID of the project being run
    project_idjs = project_id

    // The 'exception' value of the table
    except = exception

    table_id = tableid

    // The category Id that will be sent to Addedittestcase which will further sent it to tablerun
    category_id = categoryid

    // test_cycle_id to be sent to addedittestcases to edit test_case_result tables based on the test_cycle_id
    test_cycle_id = testcycleid

    // max_tids dictionary to check for 'whole_number_part' or 'decimal_part' to specify what to insert into 'test_case_id'
    max_tids = maxtid

    makemodal();
}

function makemodal() {
    $('#TestCaseModal').modal({
        backdrop: 'static',
        keyboard: false
    });
    $("#TestCaseModal").on("shown.bs.modal", function () {
        CreateandAddTestCaseId();

        $('#TestCaseForm')[0].reset();

        // If addtestcase button was clicked on table with modules/categories, then one of the following dropdown
        // values will be inserted into the form, in edittestcase, we have to hide them
        $('#categoryDropdownDiv').hide();
        $('#moduleDropdownDiv').hide();
        $('#moduless').prop('required', false);
        $('#categoryss').prop('required', false);

        $('.modal-title').html("<i class='fa fa-plus'></i> Edit Test Case");

        // Set parameters in the form or use them as needed
        for (var i = 0; i < columnsjs.length; i++) {

            // Since 'id' field is not on the form, show it should be skipped
            if (fieldjs[i] != 'id') {
                var columnid = '#'+fieldjs[i];

                // Fill the field with the value that was currently in the cell of the selected row
                if (fieldjs[i] == 'test_case_id') {
                    if ('whole_number_part' in max_tids[0]) {
                        // Get the select element
                        var selectElement = document.getElementById('test_case_id');

                        // Create a new option element
                        var defaultOption = document.createElement('option');

                        // Set the text and value of the default option
                        defaultOption.textContent = datjs[fieldjs[i]];
                        defaultOption.value = datjs[fieldjs[i]];

                        // Append the default option to the select element
                        selectElement.add(defaultOption, 0); // Adding it at the beginning (change index if you want it at a different position)

                        // Assuming 'selectedValue' is the value you want to keep selected
                        var selectedValue = datjs[fieldjs[i]];

                        // Disable all options except the selected one
                        $('#testcaseidinputs select option').each(function() {
                            if ($(this).val() !== selectedValue) {
                                $(this).prop('disabled', true);
                            }
                        });
                    }
                    else if ('decimal_part' in max_tids[0]) {
                        var numberInput = document.getElementById('test_case_id');
                        numberInput.value = datjs[fieldjs[i]];
                    }
                }
                else if (fieldjs[i] == 'actual_result') {
                    if (datjs[fieldjs[i]].length === 0) {
                        $(columnid).val(datjs[fieldjs[i]]);
                    }
                    else{
                        if (['Skipped', 'Pass'].indexOf(datjs[fieldjs[i]]) === -1) {
                            var columnrff = '#reason_for_fail'
                            $(columnid).val('Fail');
                            $(columnrff).val(datjs[fieldjs[i]]);
                        }
                        else {
                            $(columnid).val(datjs[fieldjs[i]]);
                        }
                    }
                }
                else {
                    $(columnid).val(datjs[fieldjs[i]]);
                }
            }
            else {

            // The row id ('id' field in the MySQL table) should be sent in the URL
            var rowid = datjs[fieldjs[i]];
            }
        }

        // Set readonly property for all input fields within the form as either True or False
        $('#TestCaseForm :input').prop('readonly', true);

        $('#actualresultDropdownDiv select').prop('disabled', false);

        // Sometimes while editing a form, if 'fail' is selected from 'actualresultDropdownDiv' this item opens, and
        // if the form is closed then this property will not hide, so we have to make sure it stays hidden
        if (['Skipped', 'Pass', ''].indexOf(datjs['actual_result']) === -1) {
            document.getElementById('reasonforfail').style.display = 'block';
        }
        else {
            document.getElementById('reasonforfail').style.display = 'none';
        }

        $('#remarks').prop('readonly', false);
        $('#reason_for_fail').prop('readonly', false);

        $('#test_case_description').prop('required', true);
        $('#expected_result').prop('required', true);

        $('#action').val(action);

        // Update the form action with new values
        var newAction = "AddEditTestCase?table_name=&project_id=&row_id=&exception=&table_id=&category_id=&test_cycle_id=";
        newAction = newAction.replace('table_name=', 'table_name=' + encodeURIComponent(table_namejs));
        newAction = newAction.replace('project_id=', 'project_id=' + encodeURIComponent(project_idjs));
        newAction = newAction.replace('row_id=', 'row_id=' + encodeURIComponent(rowid));
        newAction = newAction.replace('exception=', 'exception=' + encodeURIComponent(except));
        newAction = newAction.replace('table_id=', 'table_id=' + encodeURIComponent(table_id));
        newAction = newAction.replace('category_id=', 'category_id=' + encodeURIComponent(category_id));
        newAction = newAction.replace('test_cycle_id=', 'test_cycle_id=' + encodeURIComponent(test_cycle_id));

        // Set the new form action
        $('#TestCaseForm').attr('action', newAction);

       // Change the id of the #Save element
//        $('#Add').attr('id', 'Save');

        $('#Add').val('Save');
    });
}

//$(document).ready(function(){
//	$('#edittestcase').click(function(){
//		// Retrieve data attributes
//		var param1 = $(this).data('param1');
//		var param2 = $(this).data('param2');
//
//		$('#TestCaseModal').modal({
//			backdrop: 'static',
//			keyboard: false
//		});
//		$("#TestCaseModal").on("shown.bs.modal", function () {
//			$('#TestCaseForm')[0].reset();
//			$('.modal-title').html("<i class='fa fa-plus'></i> Add Test Case");
//
//			// Set parameters in the form or use them as needed
//			$('#param1Input').val(param1);
//			$('#param2Input').val(param2);
//
//			$('#action').val('edittestcase');
//			$('#save').val('Save');
//		});
//	});
//});
