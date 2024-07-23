# Introduction

These are the latest release notes for Test Case Database. We want to keep customer satisfaction at an all-time high, so incorporating these features and making some changes is essential to creating more engagement around Test Case Database.

# Overview

xFlow has been storing the information of test cases in google/excel spreadsheets. The company faces many problems associated with managing test cases on google/excel sheets which are as follows: 
- There is no centralized database for managing test cases in spreadsheets. 
- The spreadsheets create problems in a collaborative environment 
	- Especially when changes are performed on the data by a user.  
	- Changes by users require manual notifications. 
	- Multiple edits can lead to confusion and version tracking. 
- The teams face the problem in formatting the data. 
	- The formatted data is sometimes copied or viewed in a single line. 
	- This results in difficulty in viewing the data. 
- Keeping track of iterations for testing is a little challenging when running test cases. 
- Report generation does not exist in excel. 
	- Automating this process can save a lot of time. 

To solve these issues a database implementation is required where data is centralized, secured and available to multiple users with the most updated version of the data. The idea is to have a centralized database for managing test cases. The centralized test case DB will be able to keep track of iterations for testing. The centralized test case DB will not only take the release wise iterations into account but also give the reports based on each iteration. Database also has a satisfactory security mechanism which prevents unauthorized users from accessing the data. 

# Release

# Develop

## dev1.0.0

## testcase-database1.0.0

### Features

- GUI
- Database connection
- Role Based Access
  - Admin Role
  - User Role
- Register New User
- Delete User
- Logging
- View test case
- Create New Project
- Edit Draft Project
  - Add Operation
  - Edit Operation
  - Delete Operation
- Add test case in tables of draft project
- Import test cases from CSV file in tables of draft project
- Edit test case in tables of draft project
- Delete test case in tables of draft project
- Export test cases
- Delete Project
- Create or add new tables
  - Use standard template
  - User defined template
  - Add headers from CSV file
- Create & run test cycles
- Edit test cases results
- Filter test cases in a test cycle
- Delete Test Cycle

## testcase-database1.0.4

- Fixed the bug that occurs when importing test cases from a CSV file. The test case ids that are already present in the table are inserted again from the CSV, also the tesrt case ids with empty values are also inserted. After fixing this bug, the application does allows neither the re-addition of an existing test case ID nor the addition of empty test case id values.
- Resolved a bug in manually adding new test cases where the application did not display an error for duplicate test case IDs in specific scenarios. The application now shows an error when duplicate test case IDs are entered.
- Addressed a problem of multiple resubmissions of the new table form when it was repeatedly opened and closed. The application now ensures the form is submitted only once.

## testcase-database1.0.3

- Fixed a bug in importing test cases from a CSV file where the 'Remarks' and 'Actual Result' columns were case-sensitive. The columns are now handled case-insensitively.
- Resolved an issue with copying tables from an existing project where empty tables caused internal server errors. The application now skips insert queries for empty tables, preventing these errors.

## testcase-database1.0.2

- Fixed the bug when copying tables from existing product. Now the tables of exisitng products are visible.
- Fixed an issue with creating a table with headers through a CSV file, eliminating the internal server error.
- Addressed the password policy problem.
- Modified the "Add new test case" feature to enable adding test case IDs manually and to show an error when test case IDs are repeated.

## testcase-database1.0.1

- Resolved the test case ID format issue when adding new test cases.
- Fixed the download CSV file problem, ensuring files are automatically saved to the local Downloads folder.
- Corrected the duplicate table names issue across different projects.
- Fixed "hassaan" name when registering user.
- Fixed the logout issue. Now when the user goes back, he will not be able to see the GUI (or he will be redirected to the login page)
- Removed the "Error While Closing A Project" functionality, as it was not intended for the current development version.
- Fixed the issue where the dialog box opened on another user's computer when downloading a table to a CSV file. Now, files are automatically saved to the local Downloads folder, eliminating the need for the dialog box.
- Fixed the "Existing Projects Not Visible" issue. Now all the created projects can be seen in the New Project Form.
- Fixed the "Adding Test Cases via CSV File" issue. The CSV file can now be uploaded.
