var table_name;
var category_type;
var project_id;
var exception;
var table_id;
var categories;
var modules;
var category_id;
var test_cycle_id;
var createprojectmode;
var columns;

function CreateTestCaseId (last_test_case_id) {
    var dynamicFormField = document.getElementById('testcaseidinputs');
    var versionErrorMessage = document.getElementById('versionErrorMessageAddEditTestCaseForm');

    // Clear existing content
    dynamicFormField.innerHTML = '';
    versionErrorMessage.textContent = '';  // Clear previous error messages

    // Check if last_test_case_id has 'decimal_part'
    if (last_test_case_id.some(item => 'decimal_part' in item)) {
        // If 'decimal_part' exists, create an input field for version

        // Create a label for the input field
        var label = document.createElement('label');
        label.textContent = 'Test Case ID';
        label.htmlFor = 'test_case_id';
        label.style.fontSize = '14px';
        label.className = 'control-label'; // Optional, for styling

        // Create an input field for version
        var inputField = document.createElement('input');
        inputField.type = 'text';
        inputField.id = 'test_case_id';
        inputField.placeholder = 'Enter Test Case ID (e.g., 1.11)';
        inputField.name = 'Test Case ID';
        inputField.required = true;
        inputField.className = 'form-control'; // Add form-control class

        // Append label and input field to the form group div
        dynamicFormField.appendChild(label);
        dynamicFormField.appendChild(inputField);

        // Add event listener to validate input
        inputField.addEventListener('input', function () {
            var enteredValue = inputField.value;
            versionErrorMessage.textContent = '';

            var numericString = enteredValue.match(/\d+(\.\d+)?/g); // Match sequences of digits with optional decimal point
            var numericFloat = parseFloat(numericString); // Convert the string to a float


            // Check if the entered ID is in the list
            if (test_case_ids.includes(numericFloat.toString())) {
                versionErrorMessage.textContent = 'The Test Case ID  is already In Use.';
            }
            else {
                versionErrorMessage.textContent = '';
            }
        });
    }
    else if (last_test_case_id.some(item => 'whole_number_part' in item)) {
        // If 'whole_number_part' exists, create a dropdown for 'prefix'

        // Create a label for the input field
        var label = document.createElement('label');
        label.textContent = 'Test Case ID';
        label.htmlFor = 'test_case_id';
        label.style.fontSize = '14px';
        label.className = 'control-label'; // Optional, for styling

        var inputField = document.createElement('input');
        inputField.type = 'text';
        inputField.className = 'form-control';
        inputField.id = 'test_case_id';
        inputField.name = 'Test Case ID';
        inputField.placeholder = 'Select Test Case ID';
        inputField.required = true;
        inputField.className = 'form-control'; // Add form-control class

        // Append label and input field to the form group div
        dynamicFormField.appendChild(label);
        dynamicFormField.appendChild(inputField);

        // Add event listener to validate input
        inputField.addEventListener('input', function () {
            var enteredValue = inputField.value;
            versionErrorMessage.textContent = '';

            // THe test_case_ids list has string values. So  if a test case id has numeric part as '01', and the entered
            // test case id has numeric part as '1', then they will not be considered equal and the test case id will be
            // inserted which should not be the case.
            var prefix_match = enteredValue.match(/^\D+(\.\D+)?/); // Match non-digits with optional decimal point not followed by digits

            // if "prefix_match" is empty when user deletes everything in the entry the error is shown if we directly
            // try extract the first index value, so we have put the if statement below that checks if the entry is not
            // empty
            if (prefix_match) {
                var prefix = prefix_match[0]; // Extracted prefix
            }

            //var numericString = enteredValue.replace(/\D/g, ''); // \D matches any non-digit character
            var numericString = enteredValue.match(/\d+(\.\d+)?/g); // Match sequences of digits with optional decimal point
            var numericFloat = parseFloat(numericString); // Convert the string to a float


            var modified_testcase_id = '';
            // If the length of numeric string is smaller than 2, then add '0' at the start (e.g., makes '1' as '01')
            // length of numeric string should also be bigger than 0 or else it will always be true even if number is
            // not added to entered the test case id
            // Note: Not all test case IDs will have format like "test-case-01" some might have "test-case-1" so check
            // both of them
            modified_testcase_id_float = prefix + numericFloat;


            // Check if the entered ID is in the list
            if (test_case_ids.includes(modified_testcase_id_float)) {
                versionErrorMessage.textContent = 'The Test Case ID  is already In Use.';
                }
            else {
                versionErrorMessage.textContent = '';
            }
        });
    }
}

function populateDropdowns(categoryType, cat_mod_array) {
    // Clear existing options in dropdown menus
    $('#categoryss').empty();
    $('#moduless').empty();
    $('#categoryDropdownDiv').hide();
    $('#moduleDropdownDiv').hide();

    // Check category_type values and populate dropdown menus accordingly
    if (categoryType[0] === 'm') {
        $('#moduless').append('<option value="" selected disabled hidden>Select Module</option>');
        // Populate the 'module' dropdown
        Object.values(cat_mod_array).forEach(function (option) {
            $('#moduless').append($('<option>', { value: option, text: option }));
        });

        $('#moduleDropdownDiv').show();
        $('#categoryDropdownDiv').hide();
        $('#moduless').prop('required', true);
        $('#categoryss').prop('required', false);
    } else if (categoryType[0] === 'c') {
        $('#categoryss').append('<option value="" selected disabled hidden>Select Category</option>');
        // Populate the 'category' dropdown
        Object.values(cat_mod_array).forEach(function (option) {
            $('#categoryss').append($('<option>', { value: option, text: option }));
        });

        $('#categoryDropdownDiv').show();
        $('#moduleDropdownDiv').hide();
        $('#categoryss').prop('required', true);
        $('#moduless').prop('required', false);
    } else {

        // Hide both dropdown menus if category_type is empty or unknown
        $('#categoryDropdownDiv').hide();
        $('#moduleDropdownDiv').hide();
        // Make dropdowns not required because these changes persist when filling other tables' form as well
        $('#categoryss').prop('required', false);
        $('#moduless').prop('required', false);
    }
}

$(document).ready(function(){
	$('#addtestcase').click(function(){
        table_name = $(this).data('table_name');
        var max_tids = $(this).data('last_test_case_id');

        // For new tables with 0 rows, last_test_case_id length will be zero and it will give error, also we wont be needing
        // last_test_case_id for new tables with 0 rows
        if (max_tids.length != 0) {
            max_tids = max_tids.replace(/'/g, '"');
            var max_tids = JSON.parse(max_tids);
        }

	    category_type = $(this).data('categorytype');
	    if (category_type.length > 2) {
            category_type = category_type.replace(/'/g, '"');
            category_type = JSON.parse(category_type);
	    }

	    project_id = $(this).data('project_id');
	    exception = $(this).data('exception');
	    table_id = $(this).data('table_id');
	    categories = $(this).data('categories');
	    modules = $(this).data('modules');
	    category_id = $(this).data('category_id');
        test_cycle_id = $(this).data('test_cycle_id');
        test_cycle_id = parseInt(test_cycle_id);
        createprojectmode = $(this).data('createprojectmode');
        createprojectmode = parseInt(createprojectmode);
        columns = $(this).data('columns');
        columns = columns.replace(/'/g, '"');
	    columns = JSON.parse(columns);
	    // the 'categories' and 'modules' was received as string and in the string the text/string values were enclosed
	    // in single quotes. JSON requires double quotes around keys.
	    var categories = categories.replace(/'/g, '"');
	    categories = JSON.parse(categories);

	    var modules = modules.replace(/'/g, '"');
	    modules = JSON.parse(modules);

		$('#TestCaseModal').modal({
			backdrop: 'static',
			keyboard: false
		});
		$("#TestCaseModal").on("shown.bs.modal", function () {
            // Call the function to create an input or dropdown for test case id
            if (max_tids.length != 0) {
                CreateTestCaseId(max_tids);
            }

			$('#TestCaseForm')[0].reset();

			// Set readonly property for all input fields within the form as either True or False
             $('#TestCaseForm :input').prop('readonly', false);

            // THe following properties should be absent initially to
            $('#actualresultDropdownDiv select').prop('disabled', true);

            // Sometimes while editing a form, if 'fail' is selected from 'actualresultDropdownDiv' this item opens, and
            // if the form is closed then this property will not hide, so we have to make sure it stays hidden
            if (max_tids.length != 0 && columns.includes('Actual Result')) {
                document.getElementById('reasonforfail').style.display = 'none';
            }

            $('#remarks').prop('readonly', true);

            if (category_type[0] === 'c') {
                // Call the function to populate dropdowns
                populateDropdowns(category_type, categories);
            }

            else if (category_type[0] === 'm') {
                // Call the function to populate dropdowns
                populateDropdowns(category_type, modules);
            }

            else {
                // Call the function to populate dropdowns
                populateDropdowns(category_type, [""]);
            }

            // Make input required
            $('#test_case_id').prop('required', true);
            $('#test_case_description').prop('required', true);
            $('#expected_result').prop('required', true);

			$('.modal-title').html("<i class='fa fa-plus'></i> Add Test Case");
			$('#action').val('addtestcase');

			// Change the id of the #Save element
//            $('#Save').attr('id', 'Add');
            $('#Add').val('Add');
		});
	});

	$('#Add').click(function(event){
        if (document.getElementById('Add').value != 'Add') {
            return;
        }

        // Checks if the form is valid (if it fulfills all the required fields) and prevents the default form submission
        // Otherwise it reports
        document.getElementById('TestCaseForm').checkValidity();
        let isFormValid = $('#TestCaseForm')[0].checkValidity();
        if(!isFormValid) {
            $('#TestCaseForm')[0].reportValidity();
            return;
        } else {
            event.preventDefault();
        }

        var versionErrorMessage = document.getElementById('versionErrorMessageAddEditTestCaseForm');


        if (versionErrorMessage.textContent != '') {
           alert(versionErrorMessage.textContent);
           return
        }

        // Update the form action with new values
        var newAction = "AddEditTestCase?table_name=&project_id=&exception=&table_id=&category_id=&test_cycle_id=&createprojectmode=";
        newAction = newAction.replace('table_name=', 'table_name=' + encodeURIComponent(table_name));
        newAction = newAction.replace('project_id=', 'project_id=' + encodeURIComponent(project_id));
        newAction = newAction.replace('exception=', 'exception=' + encodeURIComponent(exception));
        newAction = newAction.replace('table_id=', 'table_id=' + encodeURIComponent(table_id));
        newAction = newAction.replace('category_id=', 'category_id=' + encodeURIComponent(category_id));
        newAction = newAction.replace('test_cycle_id=', 'test_cycle_id=' + encodeURIComponent(test_cycle_id));
        newAction = newAction.replace('createprojectmode=', 'createprojectmode=' + encodeURIComponent(createprojectmode));

        // Set the new form action
        $('#TestCaseForm').attr('action', newAction);

        // Now submit the form
        $('#TestCaseForm').submit();
    });
});