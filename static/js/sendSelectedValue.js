function createnewproject() {
    var newWindowWidth = 600;
    var newWindowHeight = 420;

    // Calculate center coordinates
    var screenWidth = window.screen.width;
    var screenHeight = window.screen.height;
    var leftPosition = (screenWidth - newWindowWidth) / 2;
    var topPosition = (screenHeight - newWindowHeight) / 2;

    var newWindow = window.open('create_project', '_blank', 'width=' + newWindowWidth + ',height=' + newWindowHeight + ',left=' + leftPosition + ',top=' + topPosition);
        // Focus on the new window (optional)
        if (newWindow) {
            newWindow.focus();
        }
    // Add an event listener to receive the message
    window.addEventListener('message', function(event) {
    // Check the origin of the message (for security reasons)
        if (event.origin !== window.location.origin) {
            return;
        }

        // Access the data from the posted message
        var data = event.data;

        // Use the received data as needed
//        var url = 'insertproject' + '?projectName=' + encodeURIComponent(data.projectName) + '&projectVersion=' + encodeURIComponent(data.projectVersion) + '&project_name=' + encodeURIComponent(data.project_name) + '&project_version=' + encodeURIComponent(data.project_version);
        var url = 'insertproject' + '?projectName=' + encodeURIComponent(data.projectName) + '&projectVersion=' + encodeURIComponent(data.projectVersion) + '&project_name=' + encodeURIComponent(data.project_name) + '&project_version=' + encodeURIComponent(data.project_version) + '&selecteditemsdicts=' + encodeURIComponent(data.selecteditemsdicts);
        // Redirect to the other HTML document
        window.location.href = url;
        // Now you can access the properties like data.projectName, data.projectNumber, etc.
    }, false);
}

//function sendprojectName() {
//    var projectName = document.getElementById('projectSelector').value;
//    var projectVersion = document.getElementById('versionSelector').value;
//    var url = 'dashboard?projectName=' + encodeURIComponent(projectName) + '&projectVersion=' + encodeURIComponent(projectVersion);
//    // Redirect to the other HTML document
//    window.location.href = url;
//}




// Another script that opens new window
//function openNewWindow() {
//    const winHtml = `<!DOCTYPE html>
//        <html>
//            <head>
//                <title>Window with Blob</title>
//            </head>
//            <body>
//                <h1>Hello from indow!</h1>
//            </body>
//        </html>`;
//
//    const winUrl = URL.createObjectURL(
//        new Blob([winHtml], { type: "text/html" })
//    );
//
//    const win = window.open(
//        winUrl,
//        "win",
//        `width=800,height=400,screenX=200,screenY=200`
//    );
//
//}