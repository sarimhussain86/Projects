# Test Case Database Release Notes

## Overview

As per our use case, the intended organization has been managingtest cases using Google/Excel spreadsheets, which has led to several issues: 
- Lack of a centralized database for test case management
- Collaboration difficulties when multiple users make changes
  - Manual notifications required for changes
  - Confusion and difficulty tracking multiple edits
- Formatting issues causing data to display improperly
- Challenges in tracking test case iterations
- No built-in report generation
  - Time-consuming manual processes

To address these challenges, we have implemented a centralized database for managing test cases. This database provides a secure, centralized repository accessible by multiple users, ensuring data is always up-to-date. Key features include:
- Centralized data management
- Improved security
- Tracking iterations for testing
- Comprehensive reporting based on each iteration

## Version Updates

### testcase-database v1.0.0

#### Features:

#### GUI Implementation
- GUI
- Role Based Access (Admin/User Roles)
- Logging

#### Database Implementation
- Database connection
- Register New User
- Delete User

#### Project Management
- View, create, edit, and test cases
- View, create, edit, and delete projects
- Add, edit, and delete operations within projects
- Manage test cases in project tables
- Import test cases from CSV files
- Edit test case in tables of draft project
- Export test cases
- Create or add new tables
  - Use standard or user-defined templates
  - Add headers from CSV file

#### Test Cycle Management
- Create and run test cycles
- Edit test cases results
- Filter test cases in a test cycle
- Delete Test Cycle

## Known Limitations

- Usernames must be unique and a single word without spaces.
- Automated reporting is not included in this version; test case reports must be created manually by the QA team.
- Closed projects remain editable after completion due to the lack of reporting, so the "close project" functionality was not included.
- The CSV can only be downloaded to the local Downloads folder; the user cannot select a directory of their choice to export the CSV file.
- The CSV files can only be recognized the the application if they adhere to the following rules:
  - **Remove Trailing Spaces**: Delete any blank spaces after the last column of data.
  - **Delete Unnecessary Columns**: Remove columns beyond the last data column to eliminate any blank spaces and prevent copying unnecessary columns.
  - **Follow Format Guidelines**: Verify that notes adhere to the specified format. 
  - **Check Spelling and Standards**: Verify correct spelling and consistency with standards.
  - **Consistent Column Placement**: Keep module or category headings in the same column.
  - **Eliminate Empty Row Spaces**: Remove blank spaces from rows that should be empty. 
  - **Header Formatting**: Rename headers by replacing '/' with 'Or', '#' with 'No', and removing any '-' characters.
- Notes cannot be added to the tables.
- New modules or categories cannot be added; QA must request additions from the database team.
