var projectName;
var projectVersion;

$(document).ready(function(){
    $('#DeleteTable').click(function(){

     projectName = $(this).data('project_name');
     projectVersion = $(this).data('projectVersion');

        $('#selecttabletodelete').modal({
            backdrop: 'static',
            keyboard: false
        });
        $("#selecttabletodelete").on("shown.bs.modal", function () {
            $('#deleteTableForm')[0].reset();
            $('.modal-title').html("<i class='fa fa-plus'></i>Select Table To Delete");
            $('#action').val('deleteTableForm');
            $('#deleteThisTable').val('Delete');
        });
        document.querySelector('#selecttabletodelete .column-list').addEventListener('click', function(e) {
          if (e.target.matches('.column-list-item')) {
            const selectedItems = document.querySelectorAll('.column-list-item.selected');
            selectedItems.forEach(item => item.classList.remove('selected'));
            e.target.classList.add('selected');
          }
        });
    });
    $('#deleteThisTable').click(function(event){
        event.preventDefault();

        const selectedColumn = document.querySelector('.column-list-item.selected');

        if (selectedColumn === null || selectedColumn === undefined) {
            alert("Please select a table first");
            return;
        }

        var isConfirmed = window.confirm("Are you sure you want to Delete the Selected Table?");
		// Check the user's response
		if (isConfirmed) {
			// No code here, pass on.
		} else {
			// User clicked "Cancel", do nothing or handle accordingly
			return false;
		}

        // Display the custom confirmation box
        $('#tableConfirmationBox').modal({
            backdrop: 'static',
            keyboard: false
        });

        $("#tableConfirmationBox").on("shown.bs.modal", function () {
            // Set the confirmation message
            $('#confirmationMessage').css("font-size", "14px");
        });
         // Handle confirmation button click
        $('#confirmDeleteTable').click(function() {
            // Perform the delete logic here
            const selectedColumn = document.querySelector('.column-list-item.selected');

            // Close the confirmation box
            $('#tableConfirmationBox').modal('hide');

            if (selectedColumn) {
                const selectedColumn = document.querySelector('.column-list-item.selected');
                const columnNameSpan = selectedColumn.querySelector('.column-name').textContent.trim();

                const columnPidSpan = selectedColumn.querySelector('.hiddenprojectid');
                project_id = parseFloat(columnPidSpan.textContent.trim())

                const columnTidSpan = selectedColumn.querySelector('.hiddentableid');
                table_id = parseFloat(columnTidSpan.textContent.trim())

                const columnExcSpan = selectedColumn.querySelector('.hiddentableexception');
                table_exception = columnExcSpan.textContent.trim()

                // Update the form action with new values
                var newAction = "delete_table?projectName=&projectVersion=&project_id=&table_id=&table_name=&createprojectmode=&exception=";
                newAction = newAction.replace('projectName=', 'projectName=' + encodeURIComponent(projectName));
                newAction = newAction.replace('projectVersion=', 'projectVersion=' + encodeURIComponent(projectVersion));
                newAction = newAction.replace('project_id=', 'project_id=' + encodeURIComponent(project_id));
                newAction = newAction.replace('table_name=', 'table_name=' + encodeURIComponent(columnNameSpan));
                newAction = newAction.replace('table_id=', 'table_id=' + encodeURIComponent(table_id));
                newAction = newAction.replace('createprojectmode=', 'createprojectmode=' + encodeURIComponent(1));
                newAction = newAction.replace('exception=', 'exception=' + encodeURIComponent(table_exception));

                // Set the new form action
                $('#deleteTableForm').attr('action', newAction);

                // Now submit the form
                $('#deleteTableForm').submit();
            }
        });
    });




    $('#download_csv').click(function(){
     projectName = $(this).data('project_name');
     projectVersion = $(this).data('projectVersion');

        $('#select_table_to_download').modal({
            backdrop: 'static',
            keyboard: false
        });
        $("#select_table_to_download").on("shown.bs.modal", function () {
            $('#download_csv_form')[0].reset();
            $('.modal-title').html("<i class='fa fa-plus'></i>Select Table To Download Into CSV File");
            $('#action').val('download_csv_form');
            $('#download_this_table').val('Download');
        });
        document.querySelector('#select_table_to_download .column-list').addEventListener('click', function(e) {
          if (e.target.matches('.column-list-item')) {
            const selectedItems = document.querySelectorAll('.column-list-item.selected');
            selectedItems.forEach(item => item.classList.remove('selected'));
            e.target.classList.add('selected');
          }
        });
    });
    $('#download_this_table').click(function(event){
        event.preventDefault();

        // Perform the delete logic here
        const selectedColumn = document.querySelector('.column-list-item.selected');

        // Close the confirmation box
        $('#tableConfirmationBox').modal('hide');

        if (selectedColumn === null || selectedColumn === undefined){
            alert("Please Select A Table To Download");
            return;
        }
        else {
            const selectedColumn = document.querySelector('.column-list-item.selected');
            const columnNameSpan = selectedColumn.querySelector('.column-name').textContent.trim();

            const columnPidSpan = selectedColumn.querySelector('.hiddenprojectid');
            project_id = parseFloat(columnPidSpan.textContent.trim())

            const columnTidSpan = selectedColumn.querySelector('.hiddentableid');
            table_id = parseFloat(columnTidSpan.textContent.trim())

            const columnExcSpan = selectedColumn.querySelector('.hiddentableexception');
            table_exception = columnExcSpan.textContent.trim()

            var formData = new FormData();
            formData.append('table_name', columnNameSpan);
            formData.append('table_id', table_id);
            formData.append('project_id', project_id);
            formData.append('exception', table_exception);

            let shouldContinue = true;
            let fetch_error = '';  // Variable to hold any errors
            // Make an asynchronous request to fetch items based on the selected project
            fetch('/download_csv', {
                method: 'POST',
                body: formData
            })
                .then(response => response.blob())
                .then(blob => {
                // Create an <a> element
                const link = document.createElement('a');

                let downloadname;
                downloadname = columnNameSpan.replace(new RegExp(" ", 'g'), "_");;
                downloadname = downloadname + ".csv";
                // Set the download attribute and file name
                link.download = downloadname;

                // Create a URL for the Blob and set it as the href attribute
                link.href = URL.createObjectURL(blob);

                // Append the <a> element to the document
                document.body.appendChild(link);

                // Trigger a click event on the <a> element to start the download
                link.click();

                // Remove the <a> element from the document
                document.body.removeChild(link);
                })
                .catch(error => {
                    console.error('Error:', error);
                    fetch_error = error.message;
                    shouldContinue = false;
                })
                .finally(() => {
                    if (shouldContinue) {
                        alert("Table Downloaded Into CSV File Successfully");
                    } else {
                        alert(fetch_error);
                    }
                });
        }
    });
});