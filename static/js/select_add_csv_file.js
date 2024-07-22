$(document).ready(function(){
	$('#add_test_cases_from_csv').click(function(){
        $('#select_csv_file_to_upload').modal({
            backdrop: 'static',
            keyboard: false
        });
        $("#select_csv_file_to_upload").on("shown.bs.modal", function () {
            $('#upload_csv_form')[0].reset();
            $('.modal-title').html("<i class='fa fa-plus'></i>Choose File CSV To Upload Data");
            $('#action').val('upload_csv_form');
            $('#upload_csv').val('Upload CSV');
        });
    });
//    $('#upload_csv').click(function(event){
//        event.preventDefault();
//
//        // Update the form action with new values
//        var newAction = "/";
//
//        // Set the new form action
//        $('#upload_csv_form').attr('action', newAction);
//
////        // Now submit the form
////        $('#upload_csv_form').submit();
//    });
});

// Function to dynamically populate the table
function populateTable(tableColumns, tableData, table_name, table_id, exception, project_id, category_id, createprojectmode, cat_mod_list, cat_mod, empty_table) {
    $('#tableDisplay').modal({
        backdrop: 'static',
        keyboard: false
    });

    // Unbind previously bound event listener
    $('#tableDisplay').off('shown.bs.modal').on('shown.bs.modal', function () {
        // Your other code here
    });

    // Event listener for when the modal is shown
    $('#tableDisplay').on('shown.bs.modal', function () {


        $('#select_csv_test_cases_form')[0].reset();
        $('.modal-title').html("<i class='fa fa-plus'></i>Select Test Cases From The CSV File To Add");
        $('#action').val('select_csv_test_cases_form');
        $('#add_csv_test_cases').val('Add Test Cases');
        // Get a reference to the modal content
        let modalContent = document.querySelector('#tableDisplay .modal-content');

        modalContent.style.right = '300px'; // Adjust the right position as needed
        modalContent.style.bottom = '20px'; // Adjust the bottom position as needed

        // Set a max-width for the modal content
        modalContent.style.width = '1100px'; // Adjust the width as needed

        // Get a reference to the modal body
        let modalBody = document.querySelector('#tableDisplay .modal-body');

         // Set a fixed height for the modal body
        modalBody.style.height = '450px'; // Adjust the height as needed

        // Enable vertical scrolling for the modal body
        modalBody.style.overflowY = 'auto';

        tableData.forEach(tableRows => {
            let h4Element = document.createElement('h4');
            // Set the text content of the <h4> element

            if (cat_mod == 'm') {
                h4Element.textContent = 'Module: ' + cat_mod_list[tableRows[0].module_id];
            }
            else if (cat_mod == 'c') {
                h4Element.textContent = 'Category: ' + cat_mod_list[tableRows[0].category_id];
            }

            // Create a new table element
            let table = document.createElement('table');
            table.classList.add('table');
            table.classList.add('resizable');
            // table.setAttribute('id', 'formTable');

            // Create table header (thead)
            let thead = document.createElement('thead');
            let headerRow = document.createElement('tr');

            // Append headers to the header row
            tableColumns.forEach(column => {
                let th = document.createElement('th');
                th.textContent = column;

                // Conditionally hide the headers based on a condition
                if (column === 'module_id' || column === 'category_id') {
                    th.style.display = 'none'; // Hide the cell
                }

                headerRow.appendChild(th);
            });

            // Append the header row to the thead
            thead.appendChild(headerRow);

            // Append the thead to the table
            table.appendChild(thead);

            // Create table body (tbody)
            let tbody = document.createElement('tbody');

            // Append rows to the tbody
            tableRows.forEach((rowData, index) => {
                let row = document.createElement('tr');

                // Append cells to the row
                tableColumns.forEach(column => {
                    let cell = document.createElement('td');
                    cell.textContent = rowData[column];

                    // Conditionally hide the cell based on a condition
                    if (column === 'module_id' || column === 'category_id') {
                        cell.style.display = 'none'; // Hide the cell
                    }

                    row.appendChild(cell);
                });

                // Add a checkbox to each row for selection
                let checkboxCell = document.createElement('td');
                let checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.name = `selectedRows[${index}]`;
                checkboxCell.appendChild(checkbox);
                row.appendChild(checkboxCell);

                // Add event listener to checkboxes to checkbox, when the row is selected, its color changes to green
                // the 'selected-row' is a css defined on 'table_createproject.html'
                checkbox.addEventListener('change', function () {
                    if (checkbox.checked) {
                        // Change the color when checkbox is checked
                        row.classList.add('selected-row');
                    } else {
                        // Remove the color when checkbox is unchecked
                        row.classList.remove('selected-row');
                    }
                });

                // Append the row to the tbody
                tbody.appendChild(row);
            });

            // Append the tbody to the table
            table.appendChild(tbody);

            // Append the <h4> element to a parent element in the document
            if (cat_mod == 'm') {
                modalBody.appendChild(h4Element);
            }
            else if (cat_mod == 'c') {
                modalBody.appendChild(h4Element);
            }

            // Append the table to the modal body
            modalBody.appendChild(table);
        });

//        // Add event listener to Close button
//        let closeButton = document.querySelector('#tableDisplay .modal-footer button[data-dismiss="modal"]');
//        closeButton.addEventListener('click', function () {
//            // Remove all tables from the modal body
//            let tables = document.querySelectorAll('#tableDisplay .modal-body table');
//
//            // Remove 'selected-row' class (The green colour defined in CSS) from each row in every table
//            tables.forEach(table => {
//                let rows = table.querySelectorAll('tbody tr');
//                rows.forEach(row => {
//                    row.classList.remove('selected-row');
//                });
//            });
//
//            // Remove all tables from the modal body
//            tables.forEach(table => {
//                table.parentNode.removeChild(table); // Remove table
//            });
//
//            // Remove all h4 elements from the modal body
//            let h4Elements = document.querySelectorAll('#tableDisplay .modal-body h4');
//            h4Elements.forEach(h4 => {
//                h4.parentNode.removeChild(h4); // Remove h4 element
//            });
//        });
    });

    // Event listener for form submission
    // Ensure the event listener is attached only once by replacing ".('click', function (event)" with
    // ".off('click').on('click', function (event)"
    $('#add_csv_test_cases').off('click').on('click', function (event) {
        // Prevent the default form submission
        event.preventDefault();

        // Handle the selected rows
        let selectedRows = [];
//        $('input[name^="selectedRows"]:checked').sort(function(a, b) {
//            // Compare the position of checkboxes in the DOM
//            return $(a).closest('tr').index() - $(b).closest('tr').index(); }).each(function () {
//                var rowIndex = parseInt(this.name.match(/\[(\d+)]/)[1]);
//                var selectedRow = {};
//
//                // Iterate over columns
//                tableColumns.forEach(function (column, columnIndex) {
//                    // Get the cell value for the current column and row
//                    var cellValue = tableRows[rowIndex][column];
//
//                    // Add the cell value to the selectedRow object
//                    selectedRow[column] = cellValue;
//                });
//
//                // Push the selectedRow object to the selectedRows array
//                selectedRows.push(selectedRow);
//            });

        // Iterate over each table
        $('.table').each(function() {
            let table = $(this);
            let tableRows = table.find('tbody tr');

            // Iterate over checked checkboxes in each table
            table.find('input[name^="selectedRows"]:checked').sort(function(a, b) {
                // Compare the position of checkboxes in the DOM
                return $(a).closest('tr').index() - $(b).closest('tr').index();
            }).each(function() {
                var rowIndex = parseInt(this.name.match(/\[(\d+)]/)[1]);
                var selectedRow = {};

                // Iterate over columns
                tableColumns.forEach(function(column, columnIndex) {
                    // Get the cell value for the current column and row
                    var cellValue = tableRows.eq(rowIndex).find('td').eq(columnIndex).text();

                    // Add the cell value to the selectedRow object
                    selectedRow[column] = cellValue;
                });

                // Push the selectedRow object to the selectedRows array
                selectedRows.push(selectedRow);
            });
        });

        if (selectedRows.length === 0) {
            // Display an error message (you can customize this part)
            alert('Please select at least one test case');
            // Prevent the modal from closing
            return false;
        }

        // Do something with the selected rows (e.g., send them to the server)

        // Prepare the data to be sent
        var formData = {
            selectedRows: selectedRows,
            table_name: table_name,
            table_id: table_id,
            exception: exception,
            project_id: project_id,
            category_id: category_id,
            createprojectmode: createprojectmode,
            cat_mod: cat_mod,
            empty_table: empty_table
        };

        // Send the fetch POST request
        fetch('/add_test_cases_from_csv', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json' // Set the Content-Type header
            },
            body: JSON.stringify(formData) // Convert the data to JSON string
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // Parse JSON response
        })
        .then(data => {
            if ('error' in data) {
				alert(data.error);
			}
			else {
                var newAction = "table_createproj?table_name=&project_id=&exception=&table_id=&category_id=&createprojectmode=&category_module_type=";
                newAction = newAction.replace('table_name=', 'table_name=' + encodeURIComponent(table_name));
                newAction = newAction.replace('table_id=', 'table_id=' + encodeURIComponent(table_id));
                newAction = newAction.replace('exception=', 'exception=' + encodeURIComponent(exception));
                newAction = newAction.replace('project_id=', 'project_id=' + encodeURIComponent(project_id));
                newAction = newAction.replace('category_id=', 'category_id=' + encodeURIComponent(category_id));
                newAction = newAction.replace('createprojectmode=', 'createprojectmode=' + encodeURIComponent(createprojectmode));
                newAction = newAction.replace('category_module_type=', 'category_module_type=' + encodeURIComponent(cat_mod));
                // Set the new form action
                $('#select_csv_test_cases_form').attr('action', newAction);
                // Now submit the form
                $('#select_csv_test_cases_form').submit();
			}
        })
        .catch(error => {
            console.error('Error:', error);
            // Handle error here
        });

        // Close the modal (optional)
        $('#tableDisplay').modal('hide');
    });
}

// This function is called when Select/unselect all test cases is clicked to check all checkboxes (select all rows)
function formHandleSelectAll(event, id) {
    // Prevent the default form submission behavior
    event.preventDefault();

    // Select all checkboxes within the specific table
    var checkboxes = document.querySelectorAll('table input[type="checkbox"]');
    checkboxes.forEach(function(checkbox) {
        if (id == 'formSelectAllTestCases') {
            checkbox.checked = true;
        }
        else if (id == 'formUnselectAllTestCases') {
            checkbox.checked = false;
        }
        // Optionally, you can trigger the change event to execute any associated event listeners
        checkbox.dispatchEvent(new Event('change'));
    });
}