# Introduction

These are the latest release notes for Test Case Database. We want to keep customer satisfaction at an all-time high, so incorporating these features and making some changes is essential to creating more engagement around Test Case Database.

# Overview

xFlow has been storing the information of test cases in google/excel spreadsheets. The company faces many problems associated with managing test cases on google/excel sheets which are as follows: 
- There is no centralized database for managing test cases in spreadsheets. 
- The spreadsheets create problems in a collaborative environment 
-- Especially when changes are performed on the data by a user.  
-- Changes by users require manual notifications. 
-- Multiple edits can lead to confusion and version tracking. 
- The teams face the problem in formatting the data. 
-- The formatted data is sometimes copied or viewed in a single line. 
-- This results in difficulty in viewing the data. 
- Keeping track of iterations for testing is a little challenging when running test cases. 
- Report generation does not exist in excel. 
-- Automating this process can save a lot of time. 

To solve these issues a database implementation is required where data is centralized, secured and available to multiple users with the most updated version of the data. The idea is to have a centralized database for managing test cases. The centralized test case DB will be able to keep track of iterations for testing. The centralized test case DB will not only take the release wise iterations into account but also give the reports based on each iteration. Database also has a satisfactory security mechanism which prevents unauthorized users from accessing the data. 

# Release

# Develop

## dev1.0.0

## testcase-database1.0.0

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

The following bugs were fixed in the previous versions 

### testcase-database1.0.4

- Fixed the bug that occurs when importing test cases from a CSV file. The test case ids that are already present in the table are inserted again from the CSV, also the tesrt case ids with empty values are also inserted. After fixing this bug, the application does allows neither the re-addition of an existing test case ID nor the addition of empty test case id values.
- Fixed the bug that occurs when adding new test case is added manually. The application does not give error when a test case id is repeated for specific scenarios. After resolving the bug application shows error when test case ids are repeated.
- Fixed the issue of multiple resubmissions of new table form if a form is repeatedly opened and closed, the application now submits the form only once.

### testcase-database1.0.3

- Fixed the bug that occurs when importing importing test cases from a CSV file. the code deals with 'Remarks' and 'Actual Result' column to remove it but in our case it was case sensitive. Making it case-insensitive resolved the bug.
- Fixed the bug that occurs when coyping tables from an exisitng project. The empty tables that are to be copied cause the internal server error issue. The code creates insert queries for all tables but for empty tables, the insert query will be half empty that results in the error. Skipping the insert query execution in case of copying the empty tables from an existing project resolved the issue.

### testcase-database1.0.2

- Fixed the bug when copying tables from existing product. Now the tables of exisitng products are visible.
- Fixed the bug when creating a Table with headers through CSV File. Now the application does not show Internal Server Error.
- Fixed the password policy problem.
- Modified the "Add new test case" feature to enable editting test case ids and give error when test case ids are repeated.

### testcase-database1.0.1

- Fixed the test case id format issue when adding new test cases.
- Fixed the download CSV file problem, now the files will be automatically downloaded to the local machine on Downloads folder.
- Fixed the duplicate table names issue for different projects.
- Fixed "hassaan" name when registering user.
- Fixed the logout issue. Now when the user goes back, he will not be able to see the GUI (or he will be redirected to the login page)
- Fixed the "Error While Closing A Project" isse. This functionality was not to be released in the current dev version so I have removed it.
- Fixed the "Different User Downloading A CSV File" issue.
- Fixed the "Existing Projects Not Visible" issue. Now all the created projects can be seen in the New Project Form.
- Fixed the "Adding Test Cases via CSV File" issue. The CSV file can now be uploaded.
