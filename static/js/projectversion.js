// This script is for the 'Select' functionality in top_menus, allowing users to view projects data, and for the
// 'Create Project' in create_project form, using which users can create new projects.
function updateVersionOptions() {
    // Get the selected project_name

    var selectedProject = document.getElementById('projectSelector').value;
    // Get the versionSelector dropdown
    var versionSelector = document.getElementById('versionSelector');

    // Clear existing options
    versionSelector.innerHTML = '<option value="" selected disabled hidden>Select Version</option>';
    // Filter projects based on the selected project_name
    var selectedProjectData = projects.find(function(project) {
        return project.project_name === selectedProject;
    });

//    // Add options for project_version values
//    matchingProjects.forEach(function(project) {
//        var option = document.createElement('option');
//        option.value = project.project_version;
//        option.textContent = project.project_version;
//        versionSelector.appendChild(option);
//    });

    // If the project is found, add options for project_versions
    if (selectedProjectData) {
        selectedProjectData.project_version.forEach(function(version) {
            var option = document.createElement('option');
            option.value = version;
            option.textContent = version;
            versionSelector.appendChild(option);
        });
    }
    // If the selectedProject is 'New Project', disable the project_versions dropdown
//     if (selectedProject === 'New Project') {
//        versionSelector.disabled = true;
//    } else {
//        versionSelector.disabled = false;
//    }
}


// This script is for the 'Run Project' functionality allowing users to work on projects.
function updateVersionOptionstwo() {
    // Get the selected project_name

    var selectedProject = document.getElementById('projectSelect').value;
    // Get the versionSelector dropdown
    var versionSelect = document.getElementById('versionSelect');
    // Clear existing options
    versionSelect.innerHTML = '<option value="none" selected disabled hidden>Select Version</option>';
    // Filter closed_projects based on the selected project_name
    var selectedProjectData = closed_projects.find(function(project) {
        return project.project_name === selectedProject;
    });

//    // Add options for project_version values
//    matchingProjects.forEach(function(project) {
//        var option = document.createElement('option');
//        option.value = project.project_version;
//        option.textContent = project.project_version;
//        versionSelector.appendChild(option);
//    });

    // If the project is found, add options for project_versions
    if (selectedProjectData) {
        selectedProjectData.project_version.forEach(function(version) {
            var option = document.createElement('option');
            option.value = version;
            option.textContent = version;
            versionSelect.appendChild(option);
        });
    }
}