$(document).ready(function(){
    $('#deleteproject').click(function(){
        $('#selectprojecttodelete').modal({
            backdrop: 'static',
            keyboard: false
        });
        $("#selectprojecttodelete").on("shown.bs.modal", function () {
            $('#deleteprojectForm')[0].reset();
            $('.modal-title').html("<i class='fa fa-plus'></i>Select Project To Delete");
            $('#action').val('deleteprojectForm');
            $('#deleteproj').val('Delete');
        });
        document.querySelector('#selectprojecttodelete .column-list').addEventListener('click', function(e) {
          if (e.target.matches('.column-list-item')) {
            const selectedItems = document.querySelectorAll('.column-list-item.selected');
            selectedItems.forEach(item => item.classList.remove('selected'));
            e.target.classList.add('selected');
          }
        });
    });
    $('#deleteproj').click(function(event){
        event.preventDefault();

        var isConfirmed = window.confirm("Are you sure you want to Delete the Selected Project?");
		// Check the user's response
		if (isConfirmed) {
			// No code here, pass on.
		} else {
			// User clicked "Cancel", do nothing or handle accordingly
			return false;
		}

        // Display the custom confirmation box
        $('#deleteProjectConfirmationBox').modal({
            backdrop: 'static',
            keyboard: false
        });

        $("#deleteProjectConfirmationBox").on("shown.bs.modal", function () {
            // Set the confirmation message
            $('#deleteProjectConfirmationMessage').css("font-size", "14px");
            $('#deleteProjectConfirmationMessage').text("Deleting the project will also delete every table of the project containing test cases permanently. Are you sure you want to proceed?");
        });
         // Handle confirmation button click
        $('#confirmDeleteProject').click(function() {
            // Perform the delete logic here
            const selectedColumn = document.querySelector('.column-list-item.selected');

            // Close the confirmation box
            $('#deleteProjectConfirmationBox').modal('hide');

            if (selectedColumn) {
                const selectedColumn = document.querySelector('.column-list-item.selected');
                const columnNameSpan = selectedColumn.querySelector('.column-name');
                const columnNameSpanname = columnNameSpan.textContent.trim().split(' ')[0];
                const columnNameSpanversion = columnNameSpan.textContent.trim().split(' ')[1].slice(1);
                const columnStartDateSpana = selectedColumn.querySelector('.column-creationdate');
                const columnStartDateSpanb = columnStartDateSpana.textContent.trim().split(' ');

                // Remove the first three items
                const remainingStartDate = columnStartDateSpanb.slice(3);

                // Join the remaining items back into a string
                const modifiedStartDateSpan = remainingStartDate.join(' ');

                const columnPidSpan = selectedColumn.querySelector('.hiddenprojectid');

                projectName = columnNameSpanname
                projectVersion = parseFloat(columnNameSpanversion)
                project_id = parseFloat(columnPidSpan.textContent.trim())

                // Update the form action with new values
                var newAction = "delete_project?projectName=&projectVersion=&project_startdate=&project_id=&createprojectmode=";
                newAction = newAction.replace('projectName=', 'projectName=' + encodeURIComponent(projectName));
                newAction = newAction.replace('projectVersion=', 'projectVersion=' + encodeURIComponent(projectVersion));
                newAction = newAction.replace('project_startdate=', 'project_startdate=' + encodeURIComponent(modifiedStartDateSpan));
                newAction = newAction.replace('project_id=', 'project_id=' + encodeURIComponent(project_id));
                newAction = newAction.replace('createprojectmode=', 'createprojectmode=' + encodeURIComponent(1));

                // Set the new form action
                $('#deleteprojectForm').attr('action', newAction);

                // Now submit the form
                $('#deleteprojectForm').submit();
            }
        });
    });


    $('#resumeprojectreview').click(function(){
        $('#selectprojecttoresumereview').modal({
            backdrop: 'static',
            keyboard: false
        });
        $("#selectprojecttoresumereview").on("shown.bs.modal", function () {
            $('#resumeprojectreviewForm')[0].reset();
            $('.modal-title').html("<i class='fa fa-plus'></i>Select A Draft Project To Edit");
            $('#action').val('resumeprojectreviewForm');
            $('#continuereviewproj').val('Edit Draft');
        });
        document.querySelector('#selectprojecttoresumereview .column-list').addEventListener('click', function(e) {
          if (e.target.matches('.column-list-item')) {
            const selectedItems = document.querySelectorAll('.column-list-item.selected');
            selectedItems.forEach(item => item.classList.remove('selected'));
            e.target.classList.add('selected');
          }
        });
    });
    $('#continuereviewproj').click(function(event){
        event.preventDefault();
        const selectedColumn = document.querySelector('.column-list-item.selected');
        if (!selectedColumn) {
            alert('No project was selected.');
            return true;
        }
        const columnNameSpan = selectedColumn.querySelector('.column-name');

        // Splits the trimmed text content into an array of substrings (project name with version), using a space ' '
        // as the delimiter.
        const substrings = columnNameSpan.textContent.trim().split(' ');

        // Iterate over the array of substrings (project name with version) and store the project name and its version
        let columnNameSpanname = '';
        for (let i = 0; i < substrings.length; i++) {
            if (i < substrings.length - 1) {
                // Add the words of the project name into a string
                columnNameSpanname += substrings[i] + " ";
            }
            else {
                projectName = columnNameSpanname.slice(0, -1);
                // Retrieve the project version and remove the first character from the selected substring
                // (e.g., if "v1.0" then "v" will be removed).
                projectVersion = parseFloat(substrings[i].slice(1));
            }
        }

        // const columnNameSpanname = columnNameSpan.textContent.trim().split(' ')[0];
        // const columnNameSpanversion = columnNameSpan.textContent.trim().split(' ')[1].slice(1);
        const columnStartDateSpana = selectedColumn.querySelector('.column-creationdate');
        const columnStartDateSpanb = columnStartDateSpana.textContent.trim().split(' ');

        // Remove the first three items
        const remainingStartDate = columnStartDateSpanb.slice(3);

        // Join the remaining items back into a string
        const modifiedStartDateSpan = remainingStartDate.join(' ');

        const columnPidSpan = selectedColumn.querySelector('.hiddenprojectid');

        // projectName = columnNameSpanname
        // projectVersion = parseFloat(columnNameSpanversion)
        project_id = parseFloat(columnPidSpan.textContent.trim())

        // Update the form action with new values
        var newAction = "dashboard?projectName=&projectVersion=&project_startdate=&project_id=&createprojectmode=";
        newAction = newAction.replace('projectName=', 'projectName=' + encodeURIComponent(projectName));
        newAction = newAction.replace('projectVersion=', 'projectVersion=' + encodeURIComponent(projectVersion));
        newAction = newAction.replace('project_startdate=', 'project_startdate=' + encodeURIComponent(modifiedStartDateSpan));
        newAction = newAction.replace('project_id=', 'project_id=' + encodeURIComponent(project_id));
        newAction = newAction.replace('createprojectmode=', 'createprojectmode=' + encodeURIComponent(1));

        // Set the new form action
        $('#resumeprojectreviewForm').attr('action', newAction);

        // Now submit the form
        $('#resumeprojectreviewForm').submit();
    });



    $('#historicaldata').click(function(){
        $('#selectprojectresumeandhist').modal({
            backdrop: 'static',
            keyboard: false
        });
        $("#selectprojectresumeandhist").on("shown.bs.modal", function () {
            $('#resumeandhistprojectForm')[0].reset();
            $('.modal-title').html("<i class='fa fa-plus'></i>Select Historical Data To View");
            $('#action').val('resumeandhistprojectForm');
            $('#Selecthistproj').val('Select');
        });
        document.querySelector('#selectprojectresumeandhist .column-list').addEventListener('click', function(e) {
          if (e.target.matches('.column-list-item')) {
            const selectedItems = document.querySelectorAll('.column-list-item.selected');
            selectedItems.forEach(item => item.classList.remove('selected'));
            e.target.classList.add('selected');
          }
        });
    });
    $('#Selecthistproj').click(function(event){
        event.preventDefault();
        const selectedColumn = document.querySelector('.column-list-item.selected');
        const columnNameSpan = selectedColumn.querySelector('.column-name');
        const columnNameSpanname = columnNameSpan.textContent.trim().split(' ')[0];
        const columnNameSpanversion = columnNameSpan.textContent.trim().split(' ')[1].slice(1);
        const columnStartDateSpana = selectedColumn.querySelector('.column-startdate');
        const columnStartDateSpanb = columnStartDateSpana.textContent.trim().split(' ');

        // Remove the first two items
        const remainingStartDate = columnStartDateSpanb.slice(2);

        // Join the remaining items back into a string
        const modifiedStartDateSpan = remainingStartDate.join(' ');

        const columnEndDateSpana = selectedColumn.querySelector('.column-enddate');
        const columnEndDateSpanb = columnEndDateSpana.textContent.trim().split(' ');

        // Remove the first two items
        const remainingEndDate = columnEndDateSpanb.slice(2);

        // Join the remaining items back into a string
        const modifiedEndDateSpan = remainingEndDate.join(' ');

        const columnPidSpan = selectedColumn.querySelector('.hiddenprojectid');
        const columnTcidSpan = selectedColumn.querySelector('.hiddentestcycleid');

        projectName = columnNameSpanname
        projectVersion = parseFloat(columnNameSpanversion)
        project_id = parseFloat(columnPidSpan.textContent.trim())
        test_cycle_id = parseFloat(columnTcidSpan.textContent.trim())

        // Update the form action with new values
        var newAction = "dashboardrun?projectName=&projectVersion=&project_startdate=&project_enddate=&project_id=&test_cycle_id=";
        newAction = newAction.replace('projectName=', 'projectName=' + encodeURIComponent(projectName));
        newAction = newAction.replace('projectVersion=', 'projectVersion=' + encodeURIComponent(projectVersion));
        newAction = newAction.replace('project_startdate=', 'project_startdate=' + encodeURIComponent(modifiedStartDateSpan));
        newAction = newAction.replace('project_enddate=', 'project_enddate=' + encodeURIComponent(modifiedEndDateSpan));
        newAction = newAction.replace('project_id=', 'project_id=' + encodeURIComponent(project_id));
        newAction = newAction.replace('test_cycle_id=', 'test_cycle_id=' + encodeURIComponent(test_cycle_id));

        // Set the new form action
        $('#resumeandhistprojectForm').attr('action', newAction);

        // Now submit the form
        $('#resumeandhistprojectForm').submit();
    });



    $('#run_or_resume_test_cycle').click(function(){
        $('#select_test_cycle_to_run_or_resume').modal({
            backdrop: 'static',
            keyboard: false
        });
        $("#select_test_cycle_to_run_or_resume").on("shown.bs.modal", function () {
            $('#resume_or_run_test_cycle_form')[0].reset();
            $('.modal-title').html("<i class='fa fa-plus'></i>Select Test Cycle To Run");
            $('#action').val('resume_or_run_test_cycle_form');
            $('#RunResumeHistCycle').val('Resume');
        });
        document.querySelector('#select_test_cycle_to_run_or_resume .column-list').addEventListener('click', function(e) {
          if (e.target.matches('.column-list-item')) {
            const selectedItems = document.querySelectorAll('.column-list-item.selected');
            selectedItems.forEach(item => item.classList.remove('selected'));
            e.target.classList.add('selected');
          }
        });
    });
    $('#RunResumeHistCycle').click(function(event){
        event.preventDefault();
        const selectedColumn = document.querySelector('.column-list-item.selected');
        const columnNameSpan = selectedColumn.querySelector('.column-project-name-version');
        // const columnNameSpanname = columnNameSpan.textContent.trim().split(' ')[1];
        // const columnNameSpanversion = columnNameSpan.textContent.trim().split(' ')[2].slice(1);

        // Splits the trimmed text content into an array of substrings (project name with version), using a space ' '
        // as the delimiter.
        const substrings = columnNameSpan.textContent.trim().split(' ');

        // Iterate over the array of substrings (project name with version) and store the project name and its version
        let columnNameSpanname = '';
        for (let i = 1; i < substrings.length; i++) {
            if (i < substrings.length - 1) {
                // Add the words of the project name into a string
                columnNameSpanname += substrings[i] + " ";
            }
            else {
                projectName = columnNameSpanname.slice(0, -1);
                // Retrieve the project version and remove the first character from the selected substring
                // (e.g., if "v1.0" then "v" will be removed).
                projectVersion = parseFloat(substrings[i].slice(1));
            }
        }

        const columnStartDateSpana = selectedColumn.querySelector('.column-startdate');
        const columnStartDateSpanb = columnStartDateSpana.textContent.trim().split(' ');



        // Remove the first two items
        const remainingStartDate = columnStartDateSpanb.slice(2);

        // Join the remaining items back into a string
        const modifiedStartDateSpan = remainingStartDate.join(' ');

        const columnPidSpan = selectedColumn.querySelector('.hiddenprojectid');
        const columnTcidSpan = selectedColumn.querySelector('.hiddentestcycleid');

        // projectName = columnNameSpanname
        // projectVersion = parseFloat(columnNameSpanversion)
        project_id = parseFloat(columnPidSpan.textContent.trim())
        test_cycle_id = parseFloat(columnTcidSpan.textContent.trim())

        // Update the form action with new values
        var newAction = "dashboardrun?projectName=&projectVersion=&project_startdate=&project_id=&test_cycle_id=";
        newAction = newAction.replace('projectName=', 'projectName=' + encodeURIComponent(projectName));
        newAction = newAction.replace('projectVersion=', 'projectVersion=' + encodeURIComponent(projectVersion));
        newAction = newAction.replace('project_startdate=', 'project_startdate=' + encodeURIComponent(modifiedStartDateSpan));
        newAction = newAction.replace('project_id=', 'project_id=' + encodeURIComponent(project_id));
        newAction = newAction.replace('test_cycle_id=', 'test_cycle_id=' + encodeURIComponent(test_cycle_id));

        // Set the new form action
        $('#resume_or_run_test_cycle_form').attr('action', newAction);

        // Now submit the form
        $('#resume_or_run_test_cycle_form').submit();
    });



    // Delete Test Cycles, only 'admin' user can delete test cycles
    $('#delete_test_cycle').click(function(){
        $('#select_test_cycle_to_delete').modal({
            backdrop: 'static',
            keyboard: false
        });
        $("#select_test_cycle_to_delete").on("shown.bs.modal", function () {
            $('#delete_test_cycle_form')[0].reset();
            $('.modal-title').html("<i class='fa fa-plus'></i>Select Test Cycle To Delete");
            $('#action').val('delete_test_cycle_form');
            $('#deleteTestCycle').val('Delete');
        });
        document.querySelector('#select_test_cycle_to_delete .column-list').addEventListener('click', function(e) {
          if (e.target.matches('.column-list-item')) {
            const selectedItems = document.querySelectorAll('.column-list-item.selected');
            selectedItems.forEach(item => item.classList.remove('selected'));
            e.target.classList.add('selected');
          }
        });
    });
    $('#deleteTestCycle').click(function(event){
        event.preventDefault();

        var isConfirmed = window.confirm("Are you sure you want to Delete the Selected Test Cycle?");
		// Check the user's response
		if (isConfirmed) {
			// No code here, pass on.
		} else {
			// User clicked "Cancel", do nothing or handle accordingly
			return false;
		}

        // Display the custom confirmation box
        $('#deleteTestCycleConfirmationBox').modal({
            backdrop: 'static',
            keyboard: false
        });

        $("#deleteTestCycleConfirmationBox").on("shown.bs.modal", function () {
            // Set the confirmation message
            $('#deleteTestCycleconfirmationMessage').css("font-size", "14px");
            $('#deleteTestCycleconfirmationMessage').text("Deleting The Test Cycle Will Also Delete Every Test Case Of The Test Cycle Permanently. Are You Sure You Want To Proceed?");

            // Bring the modal to the front
            $(this).css('z-index', 10050); // or a higher value if necessary
        });
         // Handle confirmation button click
        $('#confirmDeleteTestCycle').click(function() {
            // Close the confirmation box
            $('#deleteTestCycleConfirmationBox').modal('hide');

            // Perform the delete logic here
            const selectedColumn = document.querySelector('.column-list-item.selected');
            const columnNameSpan = selectedColumn.querySelector('.column-project-name-version');
            const columnNameSpanname = columnNameSpan.textContent.trim().split(' ')[1];
            const columnNameSpanversion = columnNameSpan.textContent.trim().split(' ')[2].slice(1);
            const columnStartDateSpana = selectedColumn.querySelector('.column-startdate');
            const columnStartDateSpanb = columnStartDateSpana.textContent.trim().split(' ');

            // Remove the first two items
            const remainingStartDate = columnStartDateSpanb.slice(2);

            // Join the remaining items back into a string
            const modifiedStartDateSpan = remainingStartDate.join(' ');

            const columnPidSpan = selectedColumn.querySelector('.hiddenprojectid');
            const columnTcidSpan = selectedColumn.querySelector('.hiddentestcycleid');

            projectName = columnNameSpanname
            projectVersion = parseFloat(columnNameSpanversion)
            project_id = parseFloat(columnPidSpan.textContent.trim())
            test_cycle_id = parseFloat(columnTcidSpan.textContent.trim())

            // Update the form action with new values
            var newAction = "delete_test_cycle?project_id=&test_cycle_id=";
            newAction = newAction.replace('project_id=', 'project_id=' + encodeURIComponent(project_id));
            newAction = newAction.replace('test_cycle_id=', 'test_cycle_id=' + encodeURIComponent(test_cycle_id));

            // Set the new form action
            $('#delete_test_cycle_form').attr('action', newAction);

            // Now submit the form
            $('#delete_test_cycle_form').submit();
        });
    });



    // Opens the form that lists usernames that can be removed
     $('#remove_user').click(function(){
        $('#select_user_to_remove').modal({
            backdrop: 'static',
            keyboard: false
        });
        $("#select_user_to_remove").on("shown.bs.modal", function () {
            $('#remove_user_form')[0].reset();
            $('.modal-title').html("<i class='fa fa-plus'></i>Select User To Remove");
            $('#action').val('remove_user_form');
            $('#removeuser').val('Remove');
        });
        document.querySelector('#select_user_to_remove .column-list').addEventListener('click', function(e) {
          if (e.target.matches('.column-list-item')) {
            const selectedItems = document.querySelectorAll('.column-list-item.selected');
            selectedItems.forEach(item => item.classList.remove('selected'));
            e.target.classList.add('selected');
          }
        });
    });
    $('#removeuser').click(function(event){
        event.preventDefault();
        const selectedColumn = document.querySelector('.column-list-item.selected');
        const columnNameSpan = selectedColumn.querySelector('.column-name').textContent.trim();

        let shouldContinue;

        async function delete_user() {
            // Fetch the result telling if the new tester name exists or if the tester's account is already created from
            // function 'check_tester' in main.py
            const response =  await fetch('/remove_user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username: columnNameSpan }),
            });
            const data = await response.json();
            if ('error' in data) {
                fetch_error = data.error;
                shouldContinue = false;
            }
            else {
                // Remove the selected item from the list
                if (selectedColumn) {
                    selectedColumn.parentNode.removeChild(selectedColumn);
                }
                alert(data.SUCCESS);
                shouldContinue = true;
            }
            if (!shouldContinue) {
                alert(fetch_error);
                return;
            }
            // Simulate a click event on the close button
            const closeButton = document.querySelector('#remove_user_form [data-dismiss="modal"]');
            closeButton.click();
        }

        delete_user();
        // Set the new form action
//        $('#resume_or_run_test_cycle_form').attr('action', newAction);

        // Now submit the form
//        $('#resume_or_run_test_cycle_form').submit();
    });
});