// Renders the form that creates new user
$(document).ready(function(){
	$('#register_user').click(function(){
		$('#CreateNewUser').modal({
			backdrop: 'static',
			keyboard: false
		});		
		$("#CreateNewUser").on("shown.bs.modal", function () {
			$('#newUserForm')[0].reset();
			$('.modal-title').html("<i class='fa fa-plus'></i>Add New User");
			$('#action').val('addUser');
			$('#save').val('Save');
		});
	});

	$("#newUserForm").submit(function(event) {
        // Prevent the default form submission
        event.preventDefault();
        var new_username = $("#new_username").val().toLowerCase();
        var new_password = $("#new_password").val();
        var reenter_password = $("#reenter_password").val();

        let fetch_error;
        let shouldContinue;
        let statusCode;
        let AccountCreatedStatus;

        // The 'await' function that does not let the code to continue without executing the current code works on async
        // functions only. Also only that code will wait for the current code (that uses 'await') to execute that is in
        // the async function. So we added all the code starting from fetch till the end in this function to execute
        // each line in order.
        async function register_the_new_user() {
            // Fetch the result telling if the new tester's account has been created successfully with the required
            // privileges from the function 'register_new_user' in main.py
            const response =  await fetch('/register_new_user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ new_username: new_username, new_password: new_password }),
            });
            const data = await response.json();
            if ('error' in data) {
                fetch_error = data.error;
                // Access the status code from the response object
                statusCode = response.status;
                shouldContinue = false;
            }
            else {
                shouldContinue = true;
            }

            // If the account is created successfully, display the message in the returned json object with key 'SUCCESS'
            if ('SUCCESS' in data) {
                var columnsList = document.getElementById('userslist');
                var listItem = document.createElement('li');
                listItem.className = 'column-list-item';
                listItem.innerHTML = `<span class="column-name">${new_username}</span>`;
                columnsList.appendChild(listItem);
                alert(data.SUCCESS);
            }

            // If account was not created successfully, display the error that occurred
            if (!shouldContinue) {
                alert("HTTP status code: " + statusCode + "\n" + fetch_error);
                return;
            }

            // Simulate a click event on the close button
            const closeButton = document.querySelector('#newUserForm [data-dismiss="modal"]');
            closeButton.click();
        }

        async function check_tester_exists_and_register_user() {
            // Fetch the result telling if the new tester name exists or if the tester's account is already created from
            // function 'check_tester' in main.py
            const response =  await fetch('/check_tester', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ new_username: new_username }),
            });
            const data = await response.json();
            if ('error' in data) {
                fetch_error = data.error;
                shouldContinue = false;
            }
            else {
                shouldContinue = true;
            }
            if (!shouldContinue) {
                alert(fetch_error);
                return;
            }

            // If passwords don't match, show an error message or handle the situation accordingly
            if (!(new_password === reenter_password)) {
                alert("Passwords do not match. Please re-enter your passwords.");
                return;
            }
            register_the_new_user();
        }
        check_tester_exists_and_register_user();
    });
});