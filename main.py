from flask import Flask, render_template, request, redirect, url_for, session, jsonify, g, send_file
from flask_mysqldb import MySQL
import MySQLdb.cursors
from urllib.parse import unquote
import json
import pandas as pd
import numpy as np
import io
from io import TextIOWrapper
import logging
from functools import wraps

# String representation of list to list using ast.literal_eval()
import ast

app = Flask(__name__)
app.secret_key = 'aquickbrownfoxjumpedoverthelazydog'


# If the user is not logged in, redirect them to the login page.
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'mysql_user' in session and session['mysql_user'] == 'login_db':
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


# Set appropriate HTTP headers to prevent browsers from caching pages that require authentication. This can be done
# using the after_request decorator:
@app.after_request
def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
    return response


# This class is used to change the value of 'mysql_user' that specifies the mysql user in logger.
class CustomFilter(logging.Filter):
    def __init__(self, mysql_user):
        super().__init__()
        self.mysql_user = mysql_user

    def filter(self, record):
        record.mysql_user = self.mysql_user
        return True


# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler
handler = logging.FileHandler('app.log')
handler.setLevel(logging.INFO)

# Define a custom formatter
formatter = logging.Formatter(
    '[[%(asctime)s] - User: %(mysql_user)s - %(levelname)s in File: %(module)s - Funtion: %(funcName)s()] : %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'login_db'
# app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'test_case_db'

# Initialize MySQL
mysql = MySQL(app)


# This function connects to DB and returns the cursor object after connecting to DB
def get_db():
    if 'db' not in g:
        app.config['MYSQL_USER'] = session['mysql_user']
        app.config['MYSQL_PASSWORD'] = session['mysql_password']
        g.db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    return g.db


# The @app.teardown_appcontext decorator ensures that the database connection is closed when the application context is
# torn down.
@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()


# Renders the first page of the application; The login page
@app.route('/', methods=['GET', 'POST'])
def login():
    # Remove existing CustomFilter
    for f in logger.filters:
        if isinstance(f, CustomFilter):
            logger.removeFilter(f)

    # Add a new CustomFilter with the updated value
    logger.addFilter(CustomFilter('login_db'))

    # provide mysql login user credentials to the session object
    session['mysql_user'] = 'login_db'
    session['mysql_password'] = '12345'

    logger.info('Login To The Application')
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = get_db()
        cursor.execute(f"CALL check_credentials('{username.lower()}', '{password}')")
        user = cursor.fetchone()
        if user['result'] == 'true':
            session['loggedin'] = True
            session['user'] = username.lower()
            session['mysql_user'] = username.lower()
            session['mysql_password'] = password
            app.config['MYSQL_USER'] = username.lower()
            app.config['MYSQL_PASSWORD'] = password
            # Remove existing CustomFilter
            for f in logger.filters:
                if isinstance(f, CustomFilter):
                    logger.removeFilter(f)

            # Add a new CustomFilter with the updated value
            logger.addFilter(CustomFilter(username.lower()))
            logger.info(f' {username.lower()} Logged In Successfully')
            return redirect(url_for('index'))
        else:
            logger.error('Wrong Credentials Entered.')
            message = 'Please enter correct username / password !'
    return render_template('login.html', message=message)


# This function is called from top_menus when the user clicks on "logout" to log out of the application.
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    logger.info('User logging out')
    return redirect(url_for('login'))


# After login page, this page will be rendered.
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    logger.info(f'Welcome to the Test Case DB App!!!')

    cursor = get_db()

    cursor.execute("SELECT project_name, project_version from projects WHERE project_created = 1")
    projs = cursor.fetchall()

    grouped_items = {}
    for item in projs:
        project_name = item['project_name']
        if project_name not in grouped_items:
            grouped_items[project_name] = []
        grouped_items[project_name].append(item['project_version'])

    # Create a new list of dictionaries
    closed_projects = [{'project_name': project_name, 'project_version': project_version} for
                       project_name, project_version in grouped_items.items()]

    # Used to filter test cases based on their modules and categories, also used to insert module and category names for
    # test cases with different modules and categories. cat_type value of 0 is modules and value of 1 is categories
    cursor.execute("SELECT * from categories")
    categories = cursor.fetchall()
    # categories = {item['category_id']: [item['category_name'], item['cat_type']] for item in categories}
    categories = {item['category_id']: item['category_name'] for item in categories}

    # Used to filter test cases based on their modules and categories, also used to insert module and category names for
    # test cases with different modules and categories. cat_type value of 0 is modules and value of 1 is categories
    cursor.execute("SELECT * from modules")
    modules = cursor.fetchall()
    modules = {item['module_id']: item['module_name'] for item in modules}


    # Used for inserting notes for tables which require, the notes are inserted based on their note ids
    cursor.execute("SELECT * from notes")
    notes = cursor.fetchall()
    notes = {item['note_id']: item['note'] for item in notes}

    cursor.execute('select t. *, p. * from test_cycles t join projects p on(t.project_id = p.project_id)')
    resumeandhist = cursor.fetchall()

    # For resuming the new project creation functionality if left without clicking on create project
    cursor.execute("SELECT * FROM projects WHERE project_created <> 1")
    newprojectincomplete = cursor.fetchall()

    newproject_incomplete = []
    for newproject in newprojectincomplete:
        newproject_incomplete.append(newproject)

    # For deleting projects
    cursor.execute("SELECT * FROM projects")
    allprojects = cursor.fetchall()

    all_projects = []
    for project in allprojects:
        all_projects.append(project)

    grouped_items = {}
    for item in allprojects:
        project_name = item['project_name']
        if project_name not in grouped_items:
            grouped_items[project_name] = []
        grouped_items[project_name].append(item['project_version'])

    projects = [{'project_name': project_name, 'project_version': project_version} for project_name, project_version in
                grouped_items.items()]


    cursor.execute(
        'select tc.*, p.project_name, p.project_version from test_cycles tc join projects p on (tc.project_id = p.project_id)')
    run_resume_hist_cycles = cursor.fetchall()
    running_cycles = []
    historical_cycles = []


    # Separate projects based on project_closed value
    for rrhc in run_resume_hist_cycles:
        if rrhc['test_cycle_completed'] == 0:
            running_cycles.append(rrhc)
        elif rrhc['test_cycle_completed'] == 1:
            historical_cycles.append(rrhc)

    running_cycles = tuple(running_cycles)
    historical_cycles = tuple(historical_cycles)

    # Mysql username that is logged in.
    user = session.get('user')

    # Fetch the xFlow test engineers' name and flag depicting if their account has been created or not. only admin
    # has the privileges to table 'xflow_testers', the rest of users do not have the privileges and will not user
    # the testers info anywhere if the testers value is NULL
    if user == 'admin':
        cursor.execute('CALL get_users()')
        users = cursor.fetchall()
        session['users'] = users

        cursor.execute('select * from xflow_testers')
        data = cursor.fetchall()

        # Initialize an empty dictionary
        testers_info = {}

        # Extract keys and values from each dictionary
        for dictionary in data:
            for key, value in dictionary.items():
                # Check if the key exists in the dictionary
                if key not in testers_info:
                    # If the key doesn't exist, create a new list for its values
                    testers_info[key] = []
                # Append the value to the list corresponding to the key
                if isinstance(value, str):
                    testers_info[key].append(value.lower())
                else:
                    testers_info[key].append(value)
    else:
        users = {}

    # Used in add_create_table to check if the table is 'mastertestcases' or the exceptions one
    session['defaultcolumns'] = ['Test Case ID', 'Test Case Type', 'Test Case Description', 'Prerequisites',
                                 'Steps To Execute', 'Expected Result', 'Actual Result', 'Remarks']
    session['projects'] = projects
    session['categories'] = categories
    session['modules'] = modules
    session['notes'] = notes
    session['closed_projects'] = closed_projects
    session['newproject_incomplete'] = newproject_incomplete
    session['project_tables_info'] = session.get('project_tables_info')
    session['all_projects'] = all_projects
    session['running_cycles'] = running_cycles
    session['historical_cycles'] = historical_cycles
    if user == 'admin':
        session['testers_info'] = testers_info

    return render_template("front_page.html", projects=projects,
                           closed_projects=closed_projects, newproject_incomplete=newproject_incomplete,
                           all_projects=all_projects,
                           running_cycles=running_cycles, historical_cycles=historical_cycles, user=user, users=users)


# When creating users, this will be called from the 'top_menus.html' to check if the new username matches the name of
# the test engineer in xflow and if the account with this name is already created.
@app.route('/check_tester', methods=['GET', 'POST'])
def check_tester():
    testers_info = session.get('testers_info')
    tester_name = request.json['new_username']
    logger.info(f'Checking if the tester with the username: "{tester_name}" is an employee of xflow')

    if tester_name.lower() in testers_info['tester_name']:
        index = testers_info['tester_name'].index(tester_name.lower())
    else:
        logger.error(f'Tester with the username: "{tester_name}" is NOT an employee of xflow')
        return jsonify({'error': 'The Tester Name Does Not Exist In xFlow'})

    logger.info(f'Checking if the account with the username: "{tester_name}" exists')
    if testers_info['account_created'][index] == 1:
        logger.error(f'Account with the username: "{tester_name}" already exists')
        return jsonify({'error': 'Account With The Entered Tester Name Is Already Created'})

    logger.info(f'Account with the username: "{tester_name}" does not exist and will be created')
    return jsonify({'SUCCESS': 'successful'})


# To create a new user if the username and password entered in the form are valid. This function will be called to
# register new user with the credentials provided.
@app.route('/register_new_user', methods=['GET', 'POST'])
def register_new_user():
    new_tester_name = request.json['new_username'].lower()
    new_password = request.json['new_password']

    logger.info('Connecting to the Database')
    cursor = get_db()

    logger.info(f'Creating Account username: "{new_tester_name}" in MySQL')
    try:
        cursor.execute(f"CREATE USER '{new_tester_name}'@'%' identified by '{new_password}'")
    except Exception as e:
        # Handle error
        error_message = str(e)
        # returns json object and status code. In HTTP, status code 500 corresponds to "Internal Server Error". It
        # indicates that an unexpected error occurred on the server while processing the request.
        return jsonify({'error': error_message}), 500

    cursor.execute(f"SELECT DISTINCT CONCAT(\"GRANT SELECT, INSERT ON \", TABLE_NAME, \" TO \", \"'{new_tester_name}'@'%'\") \
        AS sql_statement FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = 'test_case_db' AND TABLE_NAME NOT IN \
        ('user_roles', 'xflow_testers', 'test_cases_result', 'test_cycles')")
    grants01 = cursor.fetchall()

    for grant in grants01:
        try:
            cursor.execute(grant['sql_statement'])
        except Exception as e:
            # Handle error
            error_message = str(e)
            logger.error(f'{error_message}')
            return jsonify({'error': error_message}), 500

    cursor.execute(
        f"SELECT DISTINCT CONCAT(\"GRANT SELECT, INSERT, UPDATE ON \", TABLE_NAME, \" TO \", \"'{new_tester_name}'@'%'\") \
        AS sql_statement FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = 'test_case_db' AND TABLE_NAME IN \
        ('test_cases_result', 'test_cycles')")
    grants02 = cursor.fetchall()

    for grant in grants02:
        try:
            cursor.execute(grant['sql_statement'])
        except Exception as e:
            # Handle error
            error_message = str(e)
            logger.error(f'{error_message}')
            return jsonify({'error': error_message}), 500

    try:
        cursor.execute(f'GRANT DROP ON selected_test_cases_for_new_test_cycle TO \'{new_tester_name}\'@\'%\'')
    except Exception as e:
        # Handle error
        error_message = str(e)
        return jsonify({'error': error_message}), 500

    cursor.execute("flush privileges")

    # Store the user credentials by calling the procedure 'store_credentials'
    cursor.execute(f"call store_credentials('{new_tester_name}', '{new_password}')")
    mysql.connection.commit()

    # If the account is created successfully, set the cell value of column 'account_created' in table 'xflow_testers' to
    # 1 which means that the account for this employee has been created
    cursor.execute(f"update xflow_testers set account_created=1 where tester_name='{new_tester_name}'")
    mysql.connection.commit()

    cursor.execute('select * from xflow_testers')
    data = cursor.fetchall()

    # Initialize an empty dictionary
    testers_info = {}

    # Extract keys and values from each dictionary
    for dictionary in data:
        for key, value in dictionary.items():
            # Check if the key exists in the dictionary
            if key not in testers_info:
                # If the key doesn't exist, create a new list for its values
                testers_info[key] = []
            # Append the value to the list corresponding to the key
            if isinstance(value, str):
                testers_info[key].append(value.lower())
            else:
                testers_info[key].append(value)

    session['testers_info'] = testers_info

    # Update the users list
    cursor.execute('CALL get_users()')
    users = cursor.fetchall()

    session['users'] = users

    logger.info(f'Account with the username: "{new_tester_name}" successfully created')
    return jsonify({'SUCCESS': f'Account With Username: "{new_tester_name}" Successfully Created'})


# When removing users, this will be called from the function "$('#removeuser').click(function(event)" in
# 'top_menus_unordered_lists.js' file that also opens form rendered by 'top_menus.html'. The following script will
# receive the username selected from the list and will delete it.
@app.route('/remove_user', methods=['GET', 'POST'])
def remove_user():
    tester_name = request.json['username']
    logger.info(f'Deleting Account with the username: "{tester_name}"')

    logger.info('Connecting to the Database')
    cursor = get_db()

    cursor.execute("SET sql_safe_updates=0")


    # The procedure in the query below will drop the user, delete it from the users table and will set the
    # account_created column of 'xflow_testers' table to 0
    cursor.execute(f"call delete_user('{tester_name}')")
    mysql.connection.commit()

    # Get the list of usernames again
    cursor.execute('CALL get_users()')
    users = cursor.fetchall()
    session['users'] = users

    cursor.execute('select * from xflow_testers')
    data = cursor.fetchall()

    # Initialize an empty dictionary
    testers_info = {}

    # Extract keys and values from each dictionary. This dictionary will store the tester's account information if it
    # has been created or if the tester exists in the database.
    for dictionary in data:
        for key, value in dictionary.items():
            # Check if the key exists in the dictionary
            if key not in testers_info:
                # If the key doesn't exist, create a new list for its values
                testers_info[key] = []
            # Append the value to the list corresponding to the key
            if isinstance(value, str):
                testers_info[key].append(value.lower())
            else:
                testers_info[key].append(value)

    session['testers_info'] = testers_info

    logger.info(f'Account with the username: "{tester_name}" Successfully deleted')
    return jsonify({'SUCCESS': f'Account With Username: "{tester_name}" Successfully Deleted'})


@app.route('/create_project', methods=['GET', 'POST'])
def create_project():
    projects = session.get('projects')

    logger.info('Opening the Create New Project Form')
    return render_template("create_project.html", projects=projects)


# This function is called from top menus when user submits form to create a new project. This function will save the
# project information in the database.
@app.route("/insertproject", methods=['GET', 'POST'])
def insertproject():
    # Fetch new project name and its version, and the selected existing tables with their project ids
    # which should be included copied to the new project
    projectName = request.args.get('projectName', '')
    projectVersion = request.args.get('projectVersion', '')
    logger.info(f'Creating a new project with project name: "{projectName}" and provect version: {projectVersion}')
    # existing_project_name = request.args.get('project_name', '')
    # existing_project_version = request.args.get('project_version', '')
    # selecteditemsdicts = request.args.get('selecteditemsdicts', '')

    # # If no existing tables are selected from existing projects, then add only project info into Database
    # if len(x_array) == 0:
    cursor = get_db()

    # Insert the new project and its version to the database
    cursor.execute(
        f'INSERT INTO projects (project_name, project_version, creation_date, project_created) VALUES ("{projectName}", {projectVersion}, now(), 0)')
    mysql.connection.commit()

    # For resuming the new project creation functionality if left without clicking on create project
    cursor.execute("SELECT * FROM projects WHERE project_created <> 1")
    newprojectincomplete = cursor.fetchall()

    newproject_incomplete = []
    for newproject in newprojectincomplete:
        newproject_incomplete.append(newproject)

    session['newproject_incomplete'] = newproject_incomplete

    # For deleting projects whether they are complete or not
    cursor.execute("SELECT * FROM projects")
    allprojects = cursor.fetchall()

    all_projects = []
    for project in allprojects:
        all_projects.append(project)

    grouped_items = {}
    for item in allprojects:
        project_name = item['project_name']
        if project_name not in grouped_items:
            grouped_items[project_name] = []
        grouped_items[project_name].append(item['project_version'])

    projects = [{'project_name': project_name, 'project_version': project_version} for project_name, project_version in
                grouped_items.items()]

    session['projects'] = projects
    session['all_projects'] = all_projects

    logger.info(
        f'New project with project name: "{projectName}" and project version: {projectVersion} created successfully')

    return redirect(url_for('dashboard', projectName=projectName, projectVersion=projectVersion,
                            createprojectmode=1))


# Fetches the CSV headers and sends it to the "newtableform.html" for adding headers from CSV to create new table
@app.route('/get_csv_headers', methods=['GET', 'POST'])
def get_csv_headers():
    if request.method == 'POST':
        modules = session.get('modules')
        modules_lower = {key: value.lower() for key, value in modules.items()}

        categories = session.get('categories')
        categories_lower = {key: value.lower() for key, value in categories.items()}

        requested_csv_file = request.files
        csv_file = requested_csv_file['csv_file']
        logger.info(f'Getting headers from CSV file with name: "{csv_file}"')
        # Read the content of the FileStorage object into memory
        csv_content = csv_file.read()

        # List of encodings to try
        encodings_to_try = ['utf-8', 'latin1', 'ISO-8859-1', 'cp1252', 'utf-16', 'utf-32', 'ascii', 'cp437', 'cp850',
                            'cp858', 'cp866', 'mac_roman', 'mac_cyrillic', 'windows-1250', 'windows-1251',
                            'windows-1252', 'windows-1253', 'windows-1254', 'windows-1255', 'windows-1256',
                            'windows-1257', 'windows-1258']

        for encoding in encodings_to_try:
            try:
                # Convert the FileStorage object to a TextIOWrapper
                csv_file_wrapper = TextIOWrapper(io.BytesIO(csv_content), encoding=encoding)

                # Print the encoding and the content

                # Reset the stream position for the next encoding
                csv_file_wrapper.seek(0)

                # Read CSV file and create a Pandas DataFrame
                df = pd.read_csv(csv_file_wrapper)

                # The following filter the whole column of the dataframe where the entered column's header name exists
                # df = df.filter(regex='^(?!Unnamed:)')

                # Read CSV file and print its contents
                # csv_reader = csv.reader(csv_file_wrapper)
                #
                # for row in csv_reader:

                # Break after the first successful encoding
                break

            except UnicodeDecodeError:
                pass
            except Exception as e:
                pass

        # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        # Drop rows with missing values in all columns
        df = df.dropna(how='all')

        # Check if DataFrame has only one header and the rest are "Unnamed: X"
        count_named_headers = 0
        header_index = []
        csv_header = []
        for index, col in enumerate(df.columns):
            if col.startswith("Unnamed:"):
                pass
            else:
                header_index.append(index)
                csv_header.append(col)
                count_named_headers = count_named_headers + 1


        #  Check if the header row with single named header is a module/category
        if count_named_headers == 1:

            # Check if the header is a category/module. If it is not, return this value as a header for the new table.
            if csv_header[0].lower() in modules_lower.values():
                pass
            elif csv_header[0].lower() in categories_lower.values():
                pass
            else:
                logger.info(f'Column headers successfully fetched from file: "{csv_file}"')
                # Return the items in JSON format
                return jsonify({'column_headers': csv_header})

            # Insert a new row at index 0 and set the value at the specified column position
            df.loc[-1] = [None] * len(df.columns)

            # Insert a new row at index 0 and set the value at the specified column position
            df.loc[-1] = [None] * len(df.columns)

            # Assign a row index to each row starting from 0 and increasing sequentially. The new row added above
            # will not be part of the dataframe just yet.
            df.index = df.index + 1

            # Sort the dataframe row indexes, this will make the new empty row added above appear at the first
            # row with index 0.
            df.sort_index(inplace=True)

            # Insert the module/category at the same column position where the rest of modules/categories are stored
            df.iloc[0, header_index[0]] = df.columns[header_index[0]]
            df.columns = df.iloc[1,]

        # The Test Case ID field must be present as the first field in the CSV file or return error
        if df.columns[0].lower() != "test case id":
            return jsonify({'error': 'The Test Case ID Field is either not present in the table or is in some other '
                                     'positoon in the CSV file'})

        # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

        logger.info(f'Column headers successfully fetched from file: "{csv_file}"')
        # Return the items in JSON format
        return jsonify({'column_headers': list(df.columns.values)})


# Fetch the table names of the project name and version received. send the table names back to the function
# 'updateAvailableItems' of the file 'newtableform.html'. This is for the functionality to add tables from an existing
# project
@app.route('/get_tables', methods=['POST'])
def get_tables():
    try:
        # Get the selected items from the request
        project_name = request.json['project_name']
        version_name = request.json['version_name']
        logger.info(
            f'Fetching the table names of the project with name: "{project_name}" and version: "{version_name}"')

        logger.info('Connecting to the Database')
        # Connect to MySQL
        cursor = get_db()

        # Execute the query to fetch items based on the selected project name
        cursor.execute(
            f"SELECT project_id from projects where project_name='{project_name}' and project_version={version_name}")
        project_id = cursor.fetchall()
        project_id = project_id[0]['project_id']

        cursor.execute(f"SELECT * from table_names where project_id={project_id}")
        table_info = cursor.fetchall()
        session['table_info'] = table_info
        # Fetch all the items
        items = [row['table_name'] for row in table_info]
        hidden_items = [row['project_id'] for row in table_info]
        # Close the cursor
        cursor.close()

        logger.info(
            f'The table names of the project with name: "{project_name}" and version: "{version_name}" fetched successfully')
        # Return the items in JSON format
        return jsonify({'items': items, 'hidden_items': hidden_items})

    except Exception as e:
        logger.info(f'{e}')
        return jsonify({'error': str(e)})


# This is called when dashboard is opened for "View Test Cases", "Draft Project" or "Create test cycle mode".
@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    projectName = request.args.get('projectName', '')
    projectVersion = request.args.get('projectVersion', '')
    try:
        createprojectmode = int(request.args.get('createprojectmode', ''))
    except:
        createprojectmode = ""

    try:
        CreateTestCycleMode = int(request.args.get('CreateTestCycleMode', ''))
    except:
        CreateTestCycleMode = 0

    if createprojectmode == 1:
        logger.info(f'Opening the Draft project dashboard of project: {projectName} v{projectVersion}')
    elif CreateTestCycleMode == 1:
        logger.info(f'Opening the Test Cycle dashboard of project: {projectName} v{projectVersion}')
    else:
        logger.info(f'Opening View test cases dashboard of project: {projectName} v{projectVersion}')
    # The following are used to send to the dashboardrun which is using these variables, since we do not need them, we
    # Are assigning as their values empty strings
    test_cycle_id = ""
    project_startdate = ""
    project_enddate = ""

    logger.info('Connecting to the Database')
    cursor = get_db()

    cursor.execute(
        f"SELECT project_id, project_name, project_version from projects where project_name='{projectName}' and project_version={projectVersion}")
    print(
        f"SELECT project_id, project_name, project_version from projects where project_name='{projectName}' and project_version={projectVersion}")
    projs = cursor.fetchall()
    project_id = projs[0]['project_id']
    project_name = projs[0]['project_name']
    projectVersion = projs[0]['project_version']

    projects = session.get('projects')
    categories = session.get('categories')
    modules = session.get('modules')
    closed_projects = session.get('closed_projects')
    newproject_incomplete = session.get('newproject_incomplete')
    all_projects = session.get('all_projects')
    project_tables_info = session.get('project_tables_info')
    running_cycles = session.get('running_cycles')
    historical_cycles = session.get('historical_cycles')
    user = session.get('user')
    users = session.get('users')

    session['projectName'] = projectName
    session['projectVersion'] = projectVersion

    cursor.execute(f"SELECT * from table_names where project_id={project_id}")
    table_inf = cursor.fetchall()
    table_info = []
    for info in table_inf:
        if info['category_ids'] is not None:
            info['category_ids'] = json.loads(info['category_ids'])
        if info['module_ids'] is not None:
            info['module_ids'] = json.loads(info['module_ids'])
        table_info.append(info)
    table_info = tuple(table_info)
    session['table_info'] = table_info

    if CreateTestCycleMode == 1:
        # Check if the table exists
        cursor.execute("SHOW TABLES LIKE \"selected_test_cases_for_new_test_cycle\"")
        table_exists = cursor.fetchall()

        # Create table if not exists, OR TRUNCATE if exists
        if len(table_exists) == 0:
            cursor.execute(
                "CREATE TABLE selected_test_cases_for_new_test_cycle (row_id int, table_id int, project_id int,  test_case_id VARCHAR(12))")
            mysql.connection.commit()
        else:
            cursor.execute("TRUNCATE TABLE selected_test_cases_for_new_test_cycle")
            mysql.connection.commit()

    if createprojectmode == 1:
        return render_template("dashboard_createproject.html", project_id=project_id, project_name=project_name,
                               projectVersion=projectVersion, projects=projects, table_info=table_info, user=user,
                               categories=categories, modules=modules, CreateTestCycleMode=0,
                               users=users, closed_projects=closed_projects, project_startdate=project_startdate,
                               project_enddate=project_enddate, createprojectmode=createprojectmode,
                               newproject_incomplete=newproject_incomplete, all_projects=all_projects,
                               running_cycles=running_cycles, historical_cycles=historical_cycles)
    elif CreateTestCycleMode == 1:
        return render_template('dashboard_createproject.html', project_id=project_id, project_name=project_name,
                               projectVersion=projectVersion, projects=projects, table_info=table_info, user=user,
                               categories=categories, modules=modules, CreateTestCycleMode=1,
                               users=users, closed_projects=closed_projects, project_startdate=project_startdate,
                               project_enddate=project_enddate, createprojectmode=createprojectmode,
                               newproject_incomplete=newproject_incomplete, all_projects=all_projects,
                               running_cycles=running_cycles, historical_cycles=historical_cycles)
    else:
        return render_template("dashboard.html", project_id=project_id, project_name=project_name,
                               projectVersion=projectVersion, projects=projects, table_info=table_info, users=users,
                               categories=categories, modules=modules, user=user,
                               closed_projects=closed_projects, newproject_incomplete=newproject_incomplete,
                               all_projects=all_projects, running_cycles=running_cycles,
                               historical_cycles=historical_cycles)


@app.route('/tables', methods=['GET', 'POST'])
@login_required
def tables():
    table_id = request.args.get('table_id', '')
    table_name = request.args.get('table_name', '')
    project_id = request.args.get('project_id', '')
    try:
        category_id = int(request.args.get('category_id', ''))
    except:
        category_id = None

    try:
        module_id = int(request.args.get('module_id', ''))
    except:
        module_id = None

    category_or_module = request.args.get('category_module_type', '')

    categories = session.get('categories')
    modules = session.get('modules')

    logger.info(f"Fetching the selected table's data; table name: \"{table_name}\"")


    logger.info('Connecting to the Database')
    cursor = get_db()

    cursor.execute(f"SELECT * from table_names where table_id={table_id}")
    dat = cursor.fetchall()
    dat = dat[0]

    columns = []
    field = []
    if dat['exception'] == 1:
        table = table_name.lower()
        table = table.replace(' ', '_')

        # check if the table has prefix
        try:
            check_prefix = dat['table_prefix'] > 0
        except:
            check_prefix = False

        # If the table has prefix then append it to the "table"
        if check_prefix:
            table = table + "_" + str(dat['table_prefix'])

        cursor.execute(f"DESCRIBE {table}")
        fetched_data = cursor.fetchall()
        cols = ""
        for fd in fetched_data:
            if fd['Field'] not in ['id', 'project_id', 'table_id']:
                cols = cols + f"{fd['Field']}, "
                x = str(fd['Field'])
                field.append(x)
                x = x.replace('_', ' ')
                x = x.title()
                columns.append(x.replace("Id", "ID"))
        cols = cols[:-2]

        # If specific module's data of a table is requested e.g., hardware client sniffer, then
        # only the module's data for that table will be fetched, specified by its category_id,
        # or category in case of sanity test calls
        if isinstance(category_id, int):
            cursor.execute(f"SELECT {cols} from {table} where table_id={table_id} and category_id={category_id}")
        elif isinstance(module_id, int):
            cursor.execute(f"SELECT {cols} from {table} where table_id={table_id} and module_id={module_id}")
        else:
            cursor.execute(f"SELECT {cols} from {table} where table_id={table_id}")
        data = cursor.fetchall()

    else:
        if isinstance(category_id, int):
            cursor.execute(
                f"SELECT test_case_id, test_case_type, test_case_description, prerequisites, steps_to_execute, expected_result, actual_result, remarks, module_id, note_id, category_id FROM master_test_cases where table_id={dat['table_id']} and category_id={category_id} ORDER BY test_case_id")
        elif isinstance(module_id, int):
            cursor.execute(
                f"SELECT test_case_id, test_case_type, test_case_description, prerequisites, steps_to_execute, expected_result, actual_result, remarks, module_id, note_id, category_id FROM master_test_cases where table_id={dat['table_id']} and module_id={module_id} ORDER BY test_case_id")
        else:
            cursor.execute(
                f"SELECT test_case_id, test_case_type, test_case_description, prerequisites, steps_to_execute, expected_result, actual_result, remarks, module_id, note_id, category_id FROM master_test_cases where table_id={dat['table_id']} ORDER BY test_case_id")

        columns = ['Test Case ID', 'Test Case Type', 'Test Case Description', 'Prerequisites', 'Steps To Execute',
                   'Expected Result', 'Actual Result', 'Remarks', 'Module ID', 'Note ID', 'Category ID']
        field = ['test_case_id', 'test_case_type', 'test_case_description', 'prerequisites', 'steps_to_execute',
                 'expected_result', 'actual_result', 'remarks', 'module_id', 'note_id', 'category_id']
        data = cursor.fetchall()

    cursor.execute(f"SELECT project_name, project_version from projects where project_id={project_id}")
    projs = cursor.fetchall()
    project_name = projs[0]['project_name']
    projectVersion = projs[0]['project_version']
    projects = session.get('projects')
    table_info = session.get('table_info')
    notes = session.get('notes')
    closed_projects = session.get('closed_projects')
    newproject_incomplete = session.get('newproject_incomplete')
    all_projects = session.get('all_projects')
    running_cycles = session.get('running_cycles')
    historical_cycles = session.get('historical_cycles')
    user = session.get('user')
    users = session.get('users')
    # data = tuple(sorted(data, key=lambda x: x['module_id']))

    # Group data based on se_id and se_version
    grouped_data = {}
    for entry in data:
        if category_or_module == 'c':
            catid = entry['category_id']
        elif category_or_module == 'm':
            catid = entry['module_id']
        else:
            catid = entry['category_id']
        note = entry['note_id']

        if catid not in grouped_data:
            grouped_data[catid] = {}

        if note not in grouped_data[catid]:
            grouped_data[catid][note] = []

        grouped_data[catid][note].append(entry)
    # Convert the dictionary values to tuples
    data = tuple(
        tuple(
            tuple(entries) for entries in subdict.values()
        )
        for subdict in grouped_data.values()
    )


    logger.info(
        f'Data of the selected table fetched successfully where table name: \"{table_name}\" and project: {project_name} v{projectVersion}')
    return render_template("tables.html", project_name=project_name, projectVersion=projectVersion,
                           table_name=table_name, data=data, columns=columns, field=field, projects=projects,
                           table_info=table_info, categories=categories, modules=modules, notes=notes,
                           closed_projects=closed_projects, newproject_incomplete=newproject_incomplete,
                           all_projects=all_projects,
                           running_cycles=running_cycles, historical_cycles=historical_cycles, user=user, users=users)


@app.route('/delete_table', methods=['GET', 'POST'])
def delete_table():
    # Fetch new project name and its version, and the selected existing tables with their project ids
    # which should be included copied to the new project
    project_id = request.args.get('project_id', '')
    table_name = request.args.get('table_name', '')
    table_id = request.args.get('table_id', '')
    createprojectmode = request.args.get('createprojectmode', '')
    try:
        exception = int(request.args.get('exception', ''))
    except:
        exception = request.args.get('exception', '')

    logger.info(f"Deleting the selected table: \"{table_name}\"")

    logger.info('Connecting to the Database')
    cursor = get_db()

    cursor.execute('SET sql_safe_updates=0')
    mysql.connection.commit()

    cursor.execute('SET FOREIGN_KEY_CHECKS = 0')
    mysql.connection.commit()

    cursor.execute(f"SELECT * from table_names where table_id={table_id}")
    dat = cursor.fetchall()
    dat = dat[0]

    if exception == 1:
        # pass
        # The database table name of exception tables is just the lower case
        # form of the table name with ' ' replaced with '_'
        table = table_name.lower()
        table = table.replace(' ', '_')

        # check if the table has prefix
        try:
            check_prefix = dat['table_prefix'] > 0
        except:
            check_prefix = False

        # If the table has prefix then append it to the "table"
        if check_prefix:
            table = table + "_" + str(dat['table_prefix'])

        cursor.execute(f"DELETE FROM {table} WHERE table_id={table_id}")
        mysql.connection.commit()

        query = f'ALTER TABLE {table} AUTO_INCREMENT = 1'
        cursor.execute(query)
        mysql.connection.commit()
    else:
        cursor.execute(f"DELETE FROM master_test_cases WHERE table_id={table_id}")
        mysql.connection.commit()

        query = 'ALTER TABLE master_test_cases AUTO_INCREMENT = 1'
        cursor.execute(query)
        mysql.connection.commit()

    query = f'DELETE FROM table_names WHERE table_id={table_id}'
    cursor.execute(query)
    mysql.connection.commit()

    query = 'ALTER TABLE table_names AUTO_INCREMENT = 1'
    cursor.execute(query)
    mysql.connection.commit()

    if exception == 1:
        query = f'SELECT * FROM table_names'
        cursor.execute(query)
        all_tables_inf = cursor.fetchall()

        all_tables_info = []
        for tables in all_tables_inf:
            if tables['exception'] == 1:
                if isinstance(tables['table_prefix'], int):
                    all_tables_info.append(
                        tables['table_name'].lower().replace(' ', '_') + "_" + str(tables['table_prefix']))
                else:
                    all_tables_info.append(tables['table_name'].lower().replace(' ', '_'))

        all_tables_info = list(set(all_tables_info))

        if table not in all_tables_info:
            query = f'DROP TABLE {table}'
            cursor.execute(query)
            mysql.connection.commit()

    cursor.execute(f'SELECT * FROM projects WHERE project_id={project_id}')
    projnv = cursor.fetchall()
    projectName = projnv[0]['project_name']
    projectVersion = projnv[0]['project_version']

    logger.info(f'Selected table: "{table_name}" of project: {projectName} v{projectVersion} deleted successfully')

    return redirect(url_for('dashboard', projectName=projectName, projectVersion=projectVersion, createprojectmode=1))


@app.route('/add_create_table', methods=['GET', 'POST'])
def add_create_table():
    # Fetch new project name and its version, and the selected existing tables with their project ids
    # which should be included copied to the new project
    AddOrCreateTable = request.args.get('AddOrCreateTable', '')
    tableName = request.args.get('tableName', '')
    project_id = request.args.get('project_id', '')
    columnListValues = request.args.get('columnListValues', '')
    templateType = request.args.get('templateType', '')
    selectedTablesDicts = request.args.get('selectedTablesDicts', '')
    existing_project_name = request.args.get('project_name', '')
    existing_project_version = request.args.get('project_version', '')


    projectName = session.get('projectName')
    projectVersion = session.get('projectVersion')

    if AddOrCreateTable == 'add':
        logger.info(
            f'Adding tables from the project: {existing_project_name} v{existing_project_name} into project: {projectName} v{projectVersion}')
        add_tables(project_id, selectedTablesDicts, existing_project_name, existing_project_version)
        logger.info(
            f'Tables added successfully from the project: {existing_project_name} v{existing_project_name} into project: {projectName} v{projectVersion}')
    else:
        logger.info(f'Creating new table for the project: {projectName} v{projectVersion}')
        create_table(tableName, project_id, columnListValues, templateType)
        logger.info(f'New table created successfully for the project: {projectName} v{projectVersion}')

    return redirect(url_for('dashboard', projectName=projectName, projectVersion=projectVersion, createprojectmode=1))


def add_tables(project_id, selectedTablesDicts, existing_project_name, existing_project_version):
    projectName = session.get('projectName')
    projectVersion = session.get('projectVersion')
    # Decode the URL parameter
    decoded_x = unquote(selectedTablesDicts)

    # Parse the JSON string to obtain the original 'x' array
    x_array = json.loads(decoded_x)



    # Create a dictionary to group items by hiddenItem
    grouped_items = {}
    for item in x_array:
        hidden_item = item['hiddenItem']
        if hidden_item not in grouped_items:
            grouped_items[hidden_item] = []
        grouped_items[hidden_item].append(item['item'])

    # Create a new list of dictionaries
    result_list = [{'hiddenItem': hidden_item, 'items': items} for hidden_item, items in grouped_items.items()]


    cursor = get_db()

    # Fetch the selected existing tables based on their project ids which should be included
    # copied to the new project, the table_names column can have rows with same table_name values
    query = 'SELECT * FROM table_names WHERE '
    for pt in result_list:
        if len(tuple(pt['items'])) == 1:
            formatted_tuple = str(tuple(pt['items'])).replace(',', '')
            query = query + f'(table_name in {formatted_tuple} AND project_id={pt["hiddenItem"]}) OR '
        else:
            query = query + f'(table_name in {tuple(pt["items"])} AND project_id={pt["hiddenItem"]}) OR '
    query = query[:-4]

    cursor.execute(query)
    table_info = cursor.fetchall()


    # To edit the tables which other tables reference to
    cursor.execute('SET FOREIGN_KEY_CHECKS = 0')
    mysql.connection.commit()

    # Fetch the id of the new project inserted
    cursor.execute(f'SELECT * FROM projects WHERE project_name="{projectName}" AND project_version={projectVersion}')
    project_id = cursor.fetchall()
    project_id = project_id[0]['project_id']

    # For resuming the new project creation functionality if left without clicking on create project
    cursor.execute("SELECT * FROM projects WHERE project_created <> 1")
    newprojectincomplete = cursor.fetchall()

    newproject_incomplete = []
    for newproject in newprojectincomplete:
        newproject_incomplete.append(newproject)

    session['newproject_incomplete'] = newproject_incomplete

    # For deleting projects
    cursor.execute("SELECT * FROM projects")
    allprojects = cursor.fetchall()

    all_projects = []
    for project in allprojects:
        all_projects.append(project)

    session['all_projects'] = all_projects

    columns = []
    field = []
    for infoo in table_info:
        # The columns with NULL values are replace with 'None' i dictionaries so put a random value where column
        # value is None to replace it with NULL when constructing the SQL query as shown below
        info = {key: value if value is not None else '0MtkYnDQtc2jVSdg4thWSqSDxyayCdvS' for key, value in infoo.items()}

        # Insert the names of the selected existing tables into the table table_names with new project id value
        # which is the project id of the new project inserted into the database previously
        query = f"INSERT INTO table_names (table_name, project_id, exception, module_ids, category_ids, category_type, table_prefix) VALUES  ('{info['table_name']}', {project_id}, {info['exception']}, '{info['module_ids']}', '{info['category_ids']}', '{info['category_type']}', {info['table_prefix']})"
        query = query.replace("'0MtkYnDQtc2jVSdg4thWSqSDxyayCdvS'", 'NULL')
        query = query.replace('0MtkYnDQtc2jVSdg4thWSqSDxyayCdvS', 'NULL')
        cursor.execute(query)
        mysql.connection.commit()

        # To fetch the table ids of the newly inserted table names
        cursor.execute(f"SELECT * FROM table_names WHERE table_name='{info['table_name']}' AND project_id={project_id}")
        table_id = cursor.fetchall()
        table_id = table_id[0]['table_id']

        # The tables with exception means that they have different structure than
        # that of master test cases and have separate tables in the database
        if info['exception'] == 1:
            # pass
            # The database table name of exception tables is just the lower case
            # form of the table name with ' ' replaced with '_'
            table = info['table_name'].lower()
            table = table.replace(' ', '_')

            # check if the table has prefix
            try:
                check_prefix = info['table_prefix'] > 0
            except:
                check_prefix = False

            # If the table has prefix then append it to the "table"
            if check_prefix:
                table = table + "_" + str(info['table_prefix'])

            cursor.execute(f"DESCRIBE {table}")
            fetched_data = cursor.fetchall()
            cols = ""
            for fd in fetched_data:
                if fd['Field'] not in ['id', 'project_id', 'table_id', 'module_id', 'note_id', 'category_id']:
                    cols = cols + f"{fd['Field']}, "
                    x = str(fd['Field'])
                    field.append(x)
                    x = x.replace('_', ' ')
                    x = x.title()
                    columns.append(x.replace("Id", "ID"))
            cols = cols[:-2]
            cursor.execute(f"SELECT * from {table} where project_id={info['project_id']}")
            data = cursor.fetchall()

            # If there is no entry in tha table, do not create and execute the INSERT query or it will result in a
            # MySQL error
            if len(data) == 0:
                continue

            query = f'INSERT INTO {table} ({cols}, project_id, table_id, module_id, note_id, category_id) VALUES '
            for drd in data:
                dr = {key: value if value is not None else '0MtkYnDQtc2jVSdg4thWSqSDxyayCdvS' for key, value in
                      drd.items()}
                dr.pop('id')
                dr['project_id'] = project_id
                dr['table_id'] = table_id
                tuple_of_values = tuple(dr.values())
                query = query + f'{tuple_of_values}, '
            query = query[:-2]
            query = query.replace("'0MtkYnDQtc2jVSdg4thWSqSDxyayCdvS'", 'NULL')
            query = query.replace('0MtkYnDQtc2jVSdg4thWSqSDxyayCdvS', 'NULL')
            cursor.execute(query)
            mysql.connection.commit()

        else:
            cursor.execute(f"SELECT * FROM master_test_cases where table_id={info['table_id']}")
            data = cursor.fetchall()

            # If there is no entry in tha table, do not create and execute the INSERT query or it will result in a
            # MySQL error
            if len(data) == 0:
                continue

            query = f'INSERT INTO master_test_cases (test_case_id, test_case_type, test_case_description, prerequisites, steps_to_execute, expected_result, actual_result, remarks,  project_id, table_id, module_id, note_id, category_id) VALUES '
            for drd in data:
                dr = {key: value if value is not None else '0MtkYnDQtc2jVSdg4thWSqSDxyayCdvS' for key, value in
                      drd.items()}
                dr.pop('id')
                dr['project_id'] = project_id
                dr['table_id'] = table_id
                tuple_of_values = tuple(dr.values())
                query = query + f'{tuple_of_values}, '
            query = query[:-2]
            query = query.replace("'0MtkYnDQtc2jVSdg4thWSqSDxyayCdvS'", 'NULL')
            query = query.replace('0MtkYnDQtc2jVSdg4thWSqSDxyayCdvS', 'NULL')
            cursor.execute(query)
            mysql.connection.commit()

    createprojectmode = 1

    return redirect(url_for('dashboard', projectName=projectName, projectVersion=projectVersion,
                            createprojectmode=createprojectmode))


def create_table(tableName, project_id, columnValuesEnc, templateType):
    def exception_tables(columnValuesList, tableName, table, project_id):
        cursor = get_db()

        # We will compare the new table fields with the fields of the tables having the same name so the application can
        # decide whether to create an entirely new table in MySQL if fields new table's fields are different or use any
        # of the existing table for storing data in case the fields and their order are same.
        new_columns = []
        for item in columnValuesList:
            new_columns.append(item['columnName'].lower().replace(' ', '_'))

        cursor.execute(f'Select * from table_names where table_name = "{tableName}" AND exception = 1')
        does_table_exists = cursor.fetchall()


        #  if the 'tabel_prefix' is to be added then we will increment this value to the required table_prefix value
        # or NULL will be inserted into the 'table_prefix' filed in 'table_names' MySQL table.
        add_table_prefix = 0

        # Flag that checks if there is a need to create a new table if the existing tables with the same name as the new
        # table has different or same fields in terms of order, count, and names
        flag_create_table = True

        if len(does_table_exists) > 0:
            # If table fields are different in any way, we will need to create a new MySQL table with new prefix value,
            # And we are using int because if the for loop below completes all iterations, it means that the new and
            # existing tables have different field values, orders, or counts, so a new table should be created with
            # prefix value as the entered table name and a suffix
            table_with_new_prefix = 0

            for existing_table in does_table_exists:
                if isinstance(existing_table["table_prefix"], int):
                    existing_table_name = existing_table['table_name'].lower().replace(' ', '_') + "_" + str(
                        existing_table["table_prefix"])
                else:
                    existing_table_name = table

                # We need table definition to get the fields of the table and compare the fields and their order with
                # the fields of the new table. The purpose of doing this is defined above.
                cursor.execute(f"DESCRIBE {existing_table_name}")
                existing_table_definition = cursor.fetchall()

                existing_table_fields = []
                for etf in existing_table_definition:
                    if etf['Field'] not in ['id', 'project_id', 'table_id', 'module_id', 'note_id', 'category_id']:
                        existing_table_fields.append(etf['Field'])

                # Check if the lists have the same length
                if len(new_columns) != len(existing_table_fields):

                    # For an existing table with same name that was created first, its 'table_prefix' value is NULL,
                    # so we have to check if the value was null then do not update 'table_with_new_prefix'
                    if isinstance(existing_table["table_prefix"], int):

                        # If the length of the fields are not same, continue to next iteration
                        table_with_new_prefix = existing_table["table_prefix"] + 1
                    else:
                        table_with_new_prefix = 1

                    continue

                else:
                    # Check if both lists are equal in a case-insensitive manner
                    fields_are_equal = all(x == y for x, y in zip(new_columns, existing_table_fields))

                    if fields_are_equal:
                        flag_create_table = False

                        # For an existing table with same name that was created first, its 'table_prefix' value is NULL,
                        # so we have to check if the value was null then do not update 'table' and 'add_table_prefix'
                        if isinstance(existing_table["table_prefix"], int):
                            table = table + "_" + str(existing_table["table_prefix"])
                            add_table_prefix = existing_table["table_prefix"]

                        break
                    else:
                        # For an existing table with same name that was created first, its 'table_prefix' value is NULL,
                        # so we have to check if the value was null then do not update 'table_with_new_prefix'
                        if isinstance(existing_table["table_prefix"], int):

                            # If the length of the fields are not same, continue to next iteration
                            table_with_new_prefix = existing_table["table_prefix"] + 1
                        else:
                            table_with_new_prefix = 1
                        continue

            if table_with_new_prefix > 0:
                table = table + "_" + str(table_with_new_prefix)
                add_table_prefix = table_with_new_prefix

        if flag_create_table:
            query = f'CREATE TABLE {table} (id INT PRIMARY KEY AUTO_INCREMENT,'
            for item in columnValuesList:
                col = item['columnName'].lower().replace(' ', '_')
                col = col.replace('-', '_')
                col = col.replace('/', '_or_')
                col = col.replace('#', 'no')

                if item['columnType'] == 'number':
                    query = query + f" {col} INT,"
                else:
                    query = query + f" {col} TEXT,"

            query = query + ' project_id INT, table_id INT, module_id INT, note_id int, category_id int, FOREIGN KEY (project_id) REFERENCES projects (project_id), FOREIGN KEY (table_id) REFERENCES table_names (table_id), FOREIGN KEY (module_id) REFERENCES modules (module_id))'
            cursor.execute(query)
            mysql.connection.commit()

            cursor.execute("CALL get_users()")
            users = cursor.fetchall()
            for user in users:
                cursor.execute(f"GRANT SELECT, INSERT ON {table} TO '{user['username']}'@'%'")

            cursor.execute("flush privileges")

        # If the table has prefix, then add it otherwise the value of 'table_prefix' should be NULL for the new table
        if add_table_prefix > 0:
            query = f"INSERT INTO table_names (table_name, project_id, exception, table_prefix) VALUES  ('{tableName}', {project_id}, 1, {add_table_prefix})"
        else:
            query = f"INSERT INTO table_names (table_name, project_id, exception) VALUES  ('{tableName}', {project_id}, 1)"

        cursor.execute(query)
        mysql.connection.commit()

    # Decode the URL parameter
    decoded_x = unquote(columnValuesEnc)

    # Parse the JSON string to obtain the original 'x' array
    columnValuesList = json.loads(decoded_x)


    # Extract values of the 'columnName' key into a new list
    # new_columns = [d['columnName'] for d in columnValuesList]

    # defaultcolumns = session.get('defaultcolumns')

    table = tableName.lower().replace(' ', '_')
    # Check if the lists have the same length
    # if len(new_columns) != len(defaultcolumns):
    #     exception_tables(columnValuesList, tableName, table, project_id)
    #
    # else:
    #     # Check if both lists are equal in a case-insensitive manner
    #     are_equal = all(x.lower() == y.lower() for x, y in zip(new_columns, defaultcolumns))
    #
    #     if are_equal:
    #         cursor = get_db()
    #
    #         query = f"INSERT INTO table_names (table_name, project_id, exception) VALUES  ('{tableName}', {project_id}, NULL)"
    #         cursor.execute(query)
    #         mysql.connection.commit()
    #     else:
    #         exception_tables(columnValuesList, tableName, table, project_id)

    if templateType == 'Standard':
        cursor = get_db()

        query = f"INSERT INTO table_names (table_name, project_id) VALUES  ('{tableName}', {project_id})"

        cursor.execute(query)
        mysql.connection.commit()
    else:
        exception_tables(columnValuesList, tableName, table, project_id)

    cursor = get_db()

    cursor.execute(f"SELECT * from table_names where project_id={project_id}")
    table_inf = cursor.fetchall()
    table_info = []
    for info in table_inf:
        if info['category_ids'] is not None:
            info['category_ids'] = json.loads(info['category_ids'])
        if info['module_ids'] is not None:
            info['module_ids'] = json.loads(info['module_ids'])
        table_info.append(info)
    table_info = tuple(table_info)
    session['table_info'] = table_info


@app.route('/newtableform', methods=['GET', 'POST'])
def newtableform():
    logger.info('Opening the "Add tables or Create New table" Form')
    logger.info('Connecting to the Database')
    cursor = get_db()

    project_id = request.args.get('project_id')

    project_tables_info = []
    query = f'SELECT * FROM table_names where project_id={project_id}'
    cursor.execute(query)
    project_tables_inf = cursor.fetchall()

    for tables in project_tables_inf:
        project_tables_info.append(tables['table_name'].lower())

    project_tables_info = list(set(project_tables_info))

    session['project_tables_info'] = project_tables_info

    closed_projects = session.get('closed_projects')
    user = session.get('user')
    projects = session.get('projects')

    return render_template("newtableform.html", closed_projects=closed_projects, user=user,
                           project_tables_info=project_tables_info, projects=projects)


# Called from 'table_createproj.html' when user wants to upload test cases from CSV file. The user selects a file,
# clicks on 'Upload CSV', the function 'import_csv_rows()' is called in the same file which fetches from the following
# function the data from CSV file in the table headers and csv headers match, else error will be sent back that the
# headers do not match.
@app.route('/upload_csv', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        modules = session.get('modules')
        modules_lower = {key: value.lower() for key, value in modules.items()}

        categories = session.get('categories')
        categories_lower = {key: value.lower() for key, value in categories.items()}

        category_or_module = request.form['categoryType']
        try:
            empty_table = int(request.form['empty_table'])
        except:
            empty_table = request.form['empty_table']


        csv_file = request.files['csv_file']

        logger.info(f'Opening the CSV File: "{csv_file}" in the dashboard')

        field = ast.literal_eval(request.form['field'])

        # Remove items only if they exist in the list
        for item in ('id', 'module_id', 'note_id', 'category_id', 'row_id'):
            if item in field:
                field.remove(item)

        columns = ast.literal_eval(request.form['columns'])
        for item in ('ID', 'Module ID', 'Note ID', 'Category ID', 'Row ID'):
            if item in columns:
                columns.remove(item)
        # Read the content of the FileStorage object into memory
        csv_content = csv_file.read()

        # List of encodings to try
        encodings_to_try = ['utf-8', 'latin1', 'ISO-8859-1', 'cp1252', 'utf-16', 'utf-32', 'ascii', 'cp437', 'cp850',
                            'cp858', 'cp866', 'mac_roman', 'mac_cyrillic', 'windows-1250', 'windows-1251',
                            'windows-1252', 'windows-1253', 'windows-1254', 'windows-1255', 'windows-1256',
                            'windows-1257', 'windows-1258']

        for encoding in encodings_to_try:
            try:
                # Convert the FileStorage object to a TextIOWrapper
                csv_file_wrapper = TextIOWrapper(io.BytesIO(csv_content), encoding=encoding)

                # Print the encoding and the content

                # Reset the stream position for the next encoding
                csv_file_wrapper.seek(0)

                # Read CSV file and create a Pandas DataFrame
                df = pd.read_csv(csv_file_wrapper)

                # Read CSV file and print its contents
                # csv_reader = csv.reader(csv_file_wrapper)
                #
                # for row in csv_reader:

                # Break after the first successful encoding
                break

            except UnicodeDecodeError:
                pass
            except Exception as e:
                pass

        #  xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

        # Drop rows with missing values in all columns
        df = df.dropna(how='all')

        # Check if DataFrame has only one header and the rest are "Unnamed: X"
        count_named_headers = 0
        header_index = []
        for index, col in enumerate(df.columns):
            if col.startswith("Unnamed:"):
                pass
            else:
                header_index.append(index)
                count_named_headers = count_named_headers + 1


        #  Check if the header row with single named header is a module/category
        if count_named_headers == 1:

            #  If the single named header is a module/category then add the module/category in the first row of the df
            rearrange_dataframe = 0  # Flag that decides if the single named header should be added in the first row

            if empty_table == 1:

                # If the table is empty, then check if the single named header belongs to a category or module and
                # assign to it a category type
                if df.columns[header_index[0]].lower() in modules_lower.values():
                    category_or_module = 'm'
                    rearrange_dataframe = 1
                elif df.columns[header_index[0]].lower() in categories_lower.values():
                    category_or_module = 'c'
                    rearrange_dataframe = 1
            else:

                # If the table is not empty, do not let the CSV import category or modules if the table do not have them
                # or if the table and CSV have different category type
                if df.columns[header_index[0]].lower() in modules_lower.values():
                    if category_or_module == 'c':
                        return jsonify({'error': 'The table already has test cases divided into categories and cannot '
                                                 'import modules from CSV'})
                    elif category_or_module == 'm':
                        rearrange_dataframe = 1
                    else:
                        return jsonify({'error': 'The table does not have category or modules and cannot import '
                                                 'categories or modules from CSV'})
                elif df.columns[header_index[0]].lower() in categories_lower.values():
                    if category_or_module == 'c':
                        rearrange_dataframe = 1
                    elif category_or_module == 'm':
                        return jsonify({'error': 'The table already has test cases divided into modules and cannot '
                                                 'import categories from CSV'})
                    else:
                        return jsonify({'error': 'The table does not have category or modules and cannot import '
                                                 'categories or modules from CSV'})

            # Add the module/category in the first row of the dataframe
            if rearrange_dataframe == 1:
                # Insert a new row at index 0 and set the value at the specified column position
                df.loc[-1] = [None] * len(df.columns)

                # Assign a row index to each row starting from 0 and increasing sequentially. The new row added above
                # will not be part of the dataframe just yet.
                df.index = df.index + 1

                # Sort the dataframe row indexes, this will make the new empty row added above appear at the first
                # row with index 0.
                df.sort_index(inplace=True)

                # Insert the module/category at the same column position where the rest of modules/categories are stored
                df.iloc[0, header_index[0]] = df.columns[header_index[0]]

        is_dataframe_header = 0  # flag that checks if the dataframe headers match the table headers

        # Check if each value in the header row matches the correct headers in the list
        if all(str(header).lower() == str(item).lower() for header, item in zip(df.columns.tolist(), columns)):
            if len(df.columns.tolist()) == len(columns):
                # The dataframe headers match the table headers
                is_dataframe_header = 1

        # Iterate through each row of the dataframe to check if any row in the dataframe has headers or if the CSV has
        # headers are repeating in the sheet. This will be the case if the CSV has more than 1 table.
        for ind, row in df.iterrows():
            if all(str(row).lower() == str(item).lower() for row, item in zip(row, columns)):
                if len(row) == len(columns):
                    if is_dataframe_header == 0:
                        # Replace the dataframe header with the correct header values
                        is_dataframe_header = 1
                        df.columns = row

                        # Set the name attribute of the index to None.
                        df.columns.name = None

                    # Delete the row where headers appear again
                    df = df.drop(ind)

        # Reset index after deleting rows
        df.reset_index(drop=True, inplace=True)


        # Till this line, the dataframe has been iterated to check if it has column headers matching the table column
        # headers. If the CSV do not have headers or if the headers do not match, the following if condition will be
        # true and error will be returned
        if is_dataframe_header == 0:
            return jsonify({'error': 'The table headers and the CSV headers do not match'})

        df["module_id"] = np.nan
        df["category_id"] = np.nan

        # Find rows with only one non-null value for the purpose of retrieving module/category values
        rows_with_one_value = df[df.count(axis=1) == 1]

        # Make a list of the index positions where the rows with one non-null value were found
        mod_cat_list = rows_with_one_value.index.tolist()


        # Stack the DataFrame to convert it into a Series
        stacked = rows_with_one_value.stack()

        # # Retrieve non-null values
        # non_null_values = stacked.dropna()




        # Iterate through the rows with non_null values to check if they are category/module. If they are not, remove
        # the item form the list having non-null values, so they are not treated as category or modules but as simple
        # DataFrame row values.
        # Also, if the table is not empty, check if the non-null value if it is a category/module type belongs to the
        # same category type as that allowed for the table. If the category type is not same, return with error. Also if
        # the non-empty table has no defined category type then return with error if the non-null value comes out to be
        # a category/module
        for i, ind in enumerate(stacked.index):
            if len(category_or_module) == 0:
                if stacked[ind[0]].values[0].lower() in modules_lower.values():
                    category_or_module = 'm'
                elif stacked[ind[0]].values[0].lower() in categories_lower.values():
                    category_or_module = 'c'
                else:
                    # If the non-null value is not a module/category, remove it from the list
                    mod_cat_list.remove(ind[0])
            else:
                if stacked[ind[0]].values[0].lower() in modules_lower.values():
                    if category_or_module == 'c':
                        return jsonify({'error': 'The table already has test cases divided into categories and cannot '
                                                 'import modules from CSV'})
                    elif category_or_module == 'm':
                        pass
                    else:
                        return jsonify({'error': 'The table does not have category or modules and cannot import '
                                                 'categories or modules from CSV'})
                elif stacked[ind[0]].values[0].lower() in categories_lower.values():
                    if category_or_module == 'm':
                        return jsonify({'error': 'The table already has test cases divided into categories and cannot '
                                                 'import modules from CSV'})
                    elif category_or_module == 'c':
                        pass
                    else:
                        return jsonify({'error': 'The table does not have category or modules and cannot import '
                                                 'categories or modules from CSV'})
                else:
                    # If the non-null value is not a module/category, remove it from the list
                    mod_cat_list.remove(ind[0])


        def get_key_from_value(dictionary, target_value):
            return next((key for key, value in dictionary.items() if value == target_value), None)

        for i, mod_cat in enumerate(mod_cat_list):
            if i + 1 < len(mod_cat_list):
                df_slice = df.iloc[mod_cat + 1:mod_cat_list[i + 1]]
            else:
                df_slice = df.iloc[mod_cat + 1:]
            # Create a new column 'mod_cat' and set its value as 'mod_cat'
            if category_or_module == 'm':
                df_slice.loc[:, 'module_id'] = get_key_from_value(modules, stacked[mod_cat].values[0])
            elif category_or_module == 'c':
                df_slice.loc[:, 'category_id'] = get_key_from_value(categories, stacked[mod_cat].values[0])

            # Update the corresponding rows in the original DataFrame df
            if i + 1 < len(mod_cat_list):
                df.iloc[mod_cat + 1:mod_cat_list[i + 1]] = df_slice
            else:
                df.iloc[mod_cat + 1:] = df_slice

            # df_before = df.iloc[:headers_indexes]
            # df_after = df.iloc[desired_index:]

        # Drop the rows having module/category names from the dataframe
        df = df.drop(mod_cat_list)


        # Convert DataFrame to tuple
        data = tuple(row.to_dict() for _, row in df.iterrows())


        # # Group data based on se_id and se_version
        # grouped_data = {}
        # for entry in data:
        #     if category_or_module == 'c':
        #         catid = entry['category_id']
        #     elif category_or_module == 'm':
        #         catid = entry['module_id']
        #     else:
        #         catid = entry['category_id']
        #     # note = entry['note_id']
        #
        #     if catid not in grouped_data:
        #         grouped_data[catid] = []
        #
        #     grouped_data[catid].append(entry)
        #
        # # Convert the dictionary values to tuples
        # data = tuple(
        #     tuple(
        #         entries for entries in lists
        #     )
        #     for lists in grouped_data.values()
        # )
        #

        # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        # Get column headers
        csv_columns = list(df)

        # Replace NaN values with an empty string
        df.replace(np.nan, "", inplace=True)

        rows = df.to_dict(orient='records')

        logger.info('Selected rows successfully fetched from the CSV to add in the opened table')
        return jsonify({'table_columns': csv_columns, 'table_rows': rows, 'category_or_module': category_or_module})

        # Get rows
        rows = df.to_dict(orient='records')

        #
        # # Check if the lists have the same length
        # if len(csv_columns) != len(columns):
        #     logger.error('The table headers and the CSV headers do not match')
        #     return jsonify({'error': 'The table headers and the CSV headers do not match'})
        # #
        # else:
        #     # Check if both lists are equal in a case-insensitive manner
        #     are_equal = all(x.lower() == y.lower() for x, y in zip(csv_columns, columns))
        # #
        #     if are_equal:
        #         logger.info('Selected rows successfully fetched from the CSV to add in the opened table')
        #         return jsonify({'table_columns': csv_columns, 'table_rows': rows})
        #     else:
        #         logger.error('The table headers and the CSV headers do not match')
        #         return jsonify({'error': 'The table headers and the CSV headers do not match'})


@app.route('/download_csv', methods=['GET', 'POST'])
def download_csv():
    if request.method == 'POST':

        table_name = request.form['table_name']
        logger.info(f'Downloading the table data of the table: "{table_name}" into CSV file')

        table_id = request.form['table_id']

        project_id = request.form['project_id']

        try:
            exception = int(request.form['exception'])
        except:
            exception = request.form['exception']

        columns_to_remove = ['id', 'project_id', 'table_id', 'module_id', 'note_id', 'category_id']

        logger.info('Connecting to the Database')
        cursor = get_db()

        table = table_name.lower()
        table = table.replace(' ', '_')

        if exception == 1:
            cursor.execute(f"SELECT * from table_names where table_id={table_id}")
            dat = cursor.fetchall()
            dat = dat[0]

            # check if the table has prefix
            try:
                check_prefix = dat['table_prefix'] > 0
            except:
                check_prefix = False

            # If the table has prefix then append it to the "table"
            if check_prefix:
                table = table + "_" + str(dat['table_prefix'])

            cursor.execute(f"SELECT * from {table} where table_id={table_id} and project_id={project_id}")
            dat = cursor.fetchall()

            df = pd.DataFrame(dat)

            df.drop(columns=columns_to_remove, inplace=True)

            # Replace spaces with underscores (useful if column names have spaces)
            df.columns = df.columns.str.replace('_', ' ')

            # Create a BytesIO buffer to hold the CSV data
            buffer = io.BytesIO()
            df.to_csv(buffer, index=False)
            buffer.seek(0)  # Rewind the buffer

            try:
                # Use send_file to send the CSV file to the client
                return send_file(
                    buffer,
                    as_attachment=True,
                    download_name='data.csv',
                    mimetype='text/csv'
                )

            except Exception as e:
                return jsonify({'error': 'File could not be created'})

            logger.info(
                f'Successfully Downloaded the table data of the table: "{table_name}" into CSV file in path:"{file_path}"')
            return jsonify({'success': 'success'})

        else:
            cursor.execute(f"SELECT * from master_test_cases where table_id={table_id} and project_id={project_id}")
            dat = cursor.fetchall()
            df = pd.DataFrame(dat)
            df.drop(columns=columns_to_remove, inplace=True)

            # Replace spaces with underscores (useful if column names have spaces)
            df.columns = df.columns.str.replace('_', ' ')


            # Create a BytesIO buffer to hold the CSV data
            buffer = io.BytesIO()
            df.to_csv(buffer, index=False)
            buffer.seek(0)  # Rewind the buffer

            try:
                # Use send_file to send the CSV file to the client
                return send_file(
                    buffer,
                    as_attachment=True,
                    download_name='data.csv',
                    mimetype='text/csv'
                )

            except Exception as e:
                return jsonify({'error': 'File could not be created'})

            logger.info(
                f'Successfully Downloaded the table data of the table: "{table_name}" into CSV file in path:"{file_path}"')

            return jsonify({'success': 'success'})


# This will be called from dashboard when new project form is filled and 'insertproject' is called to complete the
# required instructions. The 'insertproject' will render the 'dashboardrun' html template which includes the
# 'left_menus_run' html templates and based on createprojectmode value, when clicking on any table on the left menus,
# 'sendValues' function of the js script will call 'table_createproj'
@app.route('/table_createproj', methods=['GET', 'POST'])
@login_required
def table_createproj():
    table_id = request.args.get('table_id', '')
    table_name = request.args.get('table_name', '')
    project_id = request.args.get('project_id', '')
    category_or_module = request.args.get('category_module_type', '')

    # Saving it because it is not needed in the html scripts but when adding or deleting test cases the current function
    # is called from other functions in main.py and the 'category_or_module' is sent here from those modules by getting
    # its value from the session e.g., session.get('category_module_type')
    session['category_module_type'] = category_or_module
    try:
        category_id = int(request.args.get('category_id', ''))
    except:
        category_id = None

    try:
        module_id = int(request.args.get('module_id', ''))
    except:
        module_id = None

    logger.info(f'Fetching the table data of the selected table,\nTable name: "{table_name}"')
    try:
        createprojectmode = int(request.args.get('createprojectmode', ''))
    except:
        createprojectmode = 0

    try:
        CreateTestCycleMode = int(request.args.get('CreateTestCycleMode', ''))
    except:
        CreateTestCycleMode = 0

    categories = session.get('categories')
    modules = session.get('modules')



    logger.info('Connecting to the Database')
    cursor = get_db()

    cursor.execute(f"SELECT * from table_names where table_id={table_id}")
    dat = cursor.fetchall()
    dat = dat[0]

    columns = []
    field = []
    if dat['exception'] == 1:
        table = table_name.lower()
        table = table.replace(' ', '_')

        # check if the table has prefix
        try:
            check_prefix = dat['table_prefix'] > 0
        except:
            check_prefix = False

        # If the table has prefix then append it to the "table"
        if check_prefix:
            table = table + "_" + str(dat['table_prefix'])

        cursor.execute(f"DESCRIBE {table}")
        fetched_data = cursor.fetchall()
        cols = ""
        for fd in fetched_data:
            if fd['Field'] not in ['project_id', 'table_id']:
                if createprojectmode == 1:
                    cols = cols + f"{fd['Field']}, "
                elif CreateTestCycleMode == 1:
                    cols = cols + f"a.{fd['Field']}, "
                x = str(fd['Field'])
                field.append(x)
                x = x.replace('_', ' ')
                x = x.title()
                columns.append(x.replace("Id", "ID"))
        cols = cols[:-2]

        # If specific module's data of a table is requested e.g., hardware client sniffer, then
        # only the module's data for that table will be fetched, specified by its category_id,
        # or category in case of sanity test calls
        if createprojectmode == 1:
            if isinstance(category_id, int):
                cursor.execute(
                    f"SELECT {cols} from {table} where table_id={table_id} and category_id={category_id} ORDER BY test_case_id")
            elif isinstance(module_id, int):
                cursor.execute(
                    f"SELECT {cols} from {table} where table_id={table_id} and module_id={module_id} ORDER BY test_case_id")
            else:
                cursor.execute(f"SELECT {cols} from {table} where table_id={table_id} ORDER BY test_case_id")

        elif CreateTestCycleMode == 1:
            if isinstance(category_id, int):
                cursor.execute(
                    f"SELECT {cols}, b.row_id from {table} a LEFT join selected_test_cases_for_new_test_cycle b on a.id = b.row_id AND a.table_id = b.table_id AND a.project_id = b.project_id where a.table_id={table_id} and a.category_id={category_id} ORDER BY test_case_id")
            elif isinstance(module_id, int):
                cursor.execute(
                    f"SELECT {cols}, b.row_id from {table} a LEFT join selected_test_cases_for_new_test_cycle b on a.id = b.row_id AND a.table_id = b.table_id AND a.project_id = b.project_id where a.table_id={table_id} and a.module_id={module_id} ORDER BY test_case_id")
            else:
                cursor.execute(
                    f"SELECT {cols}, b.row_id from {table} a LEFT join selected_test_cases_for_new_test_cycle b on a.id = b.row_id AND a.table_id = b.table_id AND a.project_id = b.project_id where a.table_id={table_id} ORDER BY test_case_id")
            field.append('row_id')
            columns.append("Row ID")

        datta = cursor.fetchall()
        # for test_case_ids, we have to get the prefix and maximum id for that prefix, the result will be sent to the
        # add test case form where max test case id will already be entered from the result, the try except sees if the
        # tes case id is float (e.g., '1.1' in DA UAT) or has a prefix (e.g., 'TCSS1' in Redundancy test cases) before
        # it, for these cases different MySQL queries will be run to fetch the prefix and its maximum number (prefix)
        # make sure to add 1 to the number/prefix as it will be the new max number for new test case id
        try:
            try_float = float(datta[0]['test_case_id'])
            try_float = 1
        except:
            try_float = 0

        if try_float == 1:
            cursor.execute(
                f"select whole_number_part as prefix, max(decimal_part)+1 decimal_part FROM (SELECT replace(test_case_id, REGEXP_SUBSTR(test_case_id,'([0-9]*[.])?[0-9]+'), '') as prefix, convert(substring_index(REGEXP_SUBSTR(test_case_id,'([0-9]*[.])?[0-9]+'), '.', 1), float) whole_number_part, convert(substring_index(REGEXP_SUBSTR(test_case_id,'([0-9]*[.])?[0-9]+'), '.', -1), float) decimal_part FROM {table} WHERE table_id={dat['table_id']}) t group by whole_number_part")
        else:
            cursor.execute(
                f"select CASE WHEN suff LIKE '\n%' THEN SUBSTRING(suff, 2) ELSE suff END AS prefix, max(whole_number_part)+1 whole_number_part FROM (SELECT replace(test_case_id, REGEXP_SUBSTR(test_case_id,'([0-9]*[.])?[0-9]+'), '') as suff, convert(substring_index(REGEXP_SUBSTR(test_case_id,'([0-9]*[.])?[0-9]+'), '.', 1), float) whole_number_part, convert(substring_index(REGEXP_SUBSTR(test_case_id,'([0-9]*[.])?[0-9]+'), '.', -1), float) decimal_part FROM {table} WHERE table_id={dat['table_id']}) t group by prefix")

        last_test_case_id = cursor.fetchall()

        # The above queries will fetch either whole_number_part or decimal_part along with 'prefix' from MySQL,
        # hence the try-except To convert it to json in js script, the keys should be enclosed in double quotes
        try:
            last_test_case_id = [{"prefix": item['prefix'], "decimal_part": item['decimal_part']} for item in
                                 last_test_case_id]
        except:
            last_test_case_id = [{"prefix": item['prefix'], "whole_number_part": item['whole_number_part']} for item in
                                 last_test_case_id]

        # Fetch the test case ids from the table. This will be used in creating new test cases to ensure the test case
        # ids are not repeated.
        # The query extracts the non-numeric and numeric part and concatenates both of them. this is done to convert
        # test case ids that appear like "TC-01" OR "TC-012" to "TC-1" OR "TC-12"
        cursor.execute(
            f"SELECT CONCAT(TRIM(SUBSTRING_INDEX(test_case_id, SUBSTRING(test_case_id, REGEXP_INSTR(test_case_id, '[0-9]')), 1)), '', CAST(SUBSTRING(test_case_id, REGEXP_INSTR(test_case_id, '[0-9]')) AS FLOAT)) AS test_case_id FROM {table} WHERE table_id={dat['table_id']}")
        test_case_ids_ = cursor.fetchall()

        # Convert to list of values by removing the key 'test_case_id'
        test_case_ids = [item['test_case_id'] for item in test_case_ids_]


    else:
        if createprojectmode == 1:
            if isinstance(category_id, int):
                cursor.execute(
                    f"SELECT id, test_case_id, test_case_type, test_case_description, prerequisites, steps_to_execute, expected_result, actual_result, remarks, module_id, note_id, category_id FROM master_test_cases where table_id={dat['table_id']} and category_id={category_id} ORDER BY test_case_id")
            elif isinstance(module_id, int):
                cursor.execute(
                    f"SELECT id, test_case_id, test_case_type, test_case_description, prerequisites, steps_to_execute, expected_result, actual_result, remarks, module_id, note_id, category_id FROM master_test_cases where table_id={dat['table_id']} and module_id={module_id} ORDER BY test_case_id")
            else:
                cursor.execute(
                    f"SELECT id, test_case_id, test_case_type, test_case_description, prerequisites, steps_to_execute, expected_result, actual_result, remarks, module_id, note_id, category_id FROM master_test_cases where table_id={dat['table_id']} ORDER BY test_case_id")

            columns = ['ID', 'Test Case ID', 'Test Case Type', 'Test Case Description', 'Prerequisites',
                       'Steps To Execute', 'Expected Result', 'Actual Result', 'Remarks', 'Module ID', 'Note ID',
                       'Category ID']
            field = ['id', 'test_case_id', 'test_case_type', 'test_case_description', 'prerequisites',
                     'steps_to_execute', 'expected_result', 'actual_result', 'remarks', 'module_id', 'note_id',
                     'category_id']
        elif CreateTestCycleMode == 1:
            if isinstance(category_id, int):
                cursor.execute(
                    f"SELECT a.id, a.test_case_id, a.test_case_type, a.test_case_description, a.prerequisites, a.steps_to_execute, a.expected_result, a.actual_result, a.remarks, a.module_id, a.note_id, a.category_id, b.row_id FROM master_test_cases a LEFT join selected_test_cases_for_new_test_cycle b on a.id = b.row_id AND a.table_id = b.table_id AND a.project_id = b.project_id where a.table_id={dat['table_id']} and a.category_id={category_id} ORDER BY test_case_id")
            elif isinstance(module_id, int):
                cursor.execute(
                    f"SELECT a.id, a.test_case_id, a.test_case_type, a.test_case_description, a.prerequisites, a.steps_to_execute, a.expected_result, a.actual_result, a.remarks, a.module_id, a.note_id, a.category_id, b.row_id FROM master_test_cases a LEFT join selected_test_cases_for_new_test_cycle b on a.id = b.row_id AND a.table_id = b.table_id AND a.project_id = b.project_id where a.table_id={dat['table_id']} and a.module_id={module_id} ORDER BY test_case_id")
            else:
                cursor.execute(
                    f"SELECT a.id, a.test_case_id, a.test_case_type, a.test_case_description, a.prerequisites, a.steps_to_execute, a.expected_result, a.actual_result, a.remarks, a.module_id, a.note_id, a.category_id, b.row_id FROM master_test_cases a LEFT join selected_test_cases_for_new_test_cycle b on a.id = b.row_id AND a.table_id = b.table_id AND a.project_id = b.project_id where a.table_id={dat['table_id']} ORDER BY test_case_id")

            columns = ['ID', 'Test Case ID', 'Test Case Type', 'Test Case Description', 'Prerequisites',
                       'Steps To Execute',
                       'Expected Result', 'Actual Result', 'Remarks', 'Module ID', 'Note ID', 'Category ID', 'Row ID']
            field = ['id', 'test_case_id', 'test_case_type', 'test_case_description', 'prerequisites',
                     'steps_to_execute',
                     'expected_result', 'actual_result', 'remarks', 'module_id', 'note_id', 'category_id', 'row_id']
        datta = cursor.fetchall()

        try:
            try_float = float(datta[0]['test_case_id'])
            try_float = 1
        except:
            try_float = 0

        if try_float == 1:
            cursor.execute(
                f"select whole_number_part as prefix, max(decimal_part)+1 decimal_part FROM (SELECT replace(test_case_id, REGEXP_SUBSTR(test_case_id,'([0-9]*[.])?[0-9]+'), '') as prefix, convert(substring_index(REGEXP_SUBSTR(test_case_id,'([0-9]*[.])?[0-9]+'), '.', 1), float) whole_number_part, convert(substring_index(REGEXP_SUBSTR(test_case_id,'([0-9]*[.])?[0-9]+'), '.', -1), float) decimal_part FROM master_test_cases WHERE table_id={dat['table_id']}) t group by whole_number_part")
        else:
            cursor.execute(
                f"select CASE WHEN suff LIKE '\n%' THEN SUBSTRING(suff, 2) ELSE suff END AS prefix, max(whole_number_part)+1 whole_number_part FROM (SELECT replace(test_case_id, REGEXP_SUBSTR(test_case_id,'([0-9]*[.])?[0-9]+'), '') as suff, convert(substring_index(REGEXP_SUBSTR(test_case_id,'([0-9]*[.])?[0-9]+'), '.', 1), float) whole_number_part, convert(substring_index(REGEXP_SUBSTR(test_case_id,'([0-9]*[.])?[0-9]+'), '.', -1), float) decimal_part FROM master_test_cases WHERE table_id={dat['table_id']}) t group by prefix")

        last_test_case_id = cursor.fetchall()

        try:
            last_test_case_id = [{"prefix": item['prefix'], "decimal_part": item['decimal_part']} for item in
                                 last_test_case_id]
        except:
            last_test_case_id = [{"prefix": item['prefix'], "whole_number_part": item['whole_number_part']} for item in
                                 last_test_case_id]


        # Fetch the test case ids from the table. This will be used in creating new test cases to ensure the test case
        # ids are not repeated
        # The query extracts the non-numeric and numeric part and concatenates both of them. this is done to convert
        # test case ids that appear like "TC-01" OR "TC-012" to "TC-1" OR "TC-12"
        cursor.execute(
            f"SELECT CONCAT(TRIM(SUBSTRING_INDEX(test_case_id, SUBSTRING(test_case_id, REGEXP_INSTR(test_case_id, '[0-9]')), 1)), '', CAST(SUBSTRING(test_case_id, REGEXP_INSTR(test_case_id, '[0-9]')) AS FLOAT)) AS test_case_id FROM master_test_cases WHERE table_id={dat['table_id']}")
        test_case_ids_ = cursor.fetchall()

        test_case_ids = [item['test_case_id'] for item in test_case_ids_]


        # If any value is None, then None will be sent as an object and not as a string,
        # which will not open the edit test case form
    data = ()
    for drd in datta:
        dr = {key: value if value is not None else '' for key, value in drd.items()}
        data = data + (dr,)

    cursor.execute(f"SELECT project_name, project_version from projects where project_id={project_id}")
    projs = cursor.fetchall()

    # Saving it in session, so we can use it in other functions like for example "add_test_cases_from_csv" to prevent
    # duplication of Test Case ID values when adding a new test case to the table
    session['test_case_ids'] = test_case_ids

    project_name = projs[0]['project_name']
    projectVersion = projs[0]['project_version']
    projects = session.get('projects')
    table_info = session.get('table_info')
    notes = session.get('notes')
    closed_projects = session.get('closed_projects')
    newproject_incomplete = session.get('newproject_incomplete')
    all_projects = session.get('all_projects')
    running_cycles = session.get('running_cycles')
    historical_cycles = session.get('historical_cycles')
    user = session.get('user')
    users = session.get('users')

    # data = tuple(sorted(data, key=lambda x: x['module_id']))

    # # Use a set comprehension and Iterate through the list and add unique category_ids to the set and exclude value 0
    # category_ids_set = {entry['category_id'] for entry in data if entry['category_id'] not in (0, '')}
    # # Some of the data has no category ids
    # if len(category_ids_set) > 0:
    #     # Create categoryType using a dictionary comprehension
    #     # Before accessing categories[str(category_id)], you might want to ensure that the category_id
    #     # exists in the categories dictionary to avoid potential KeyError.
    #     categoryType = {category_id: categories.get(str(category_id), [])[1] for category_id in category_ids_set}
    #
    #     # Extract unique values from the dictionary values using a set and convert to list.
    #     # This parameter should be sent to the 'tablerun' to create module/category dropdown menus in 'edit'
    #     # and 'add' forms module/category will be created based the cat_type values of categories
    #     categoryType = list(set(categoryType.values()))
    #
    # else:
    #     # Send empty list if data has no parts belonging to a module or any category
    #     categoryType = []
    # # data = tuple(sorted(data, key=lambda x: x['module_id']))
    #
    # # If the table is new or has no rows, then categoryType will not be filled since table has no data to get category_id
    # if len(data) == 0:
    #     for info in table_info:
    #         if table_name in info['table_name']:
    #             if info['category_type'] != None:
    #                 categoryType.append(info['category_type'])

    # Group data based on se_id and se_version
    grouped_data = {}
    for entry in data:
        if category_or_module == 'c':
            catid = entry['category_id']
        elif category_or_module == 'm':
            catid = entry['module_id']
        else:
            catid = entry['category_id']
        note = entry['note_id']

        if catid not in grouped_data:
            grouped_data[catid] = {}

        if note not in grouped_data[catid]:
            grouped_data[catid][note] = []

        grouped_data[catid][note].append(entry)

    # Convert the dictionary values to tuples
    data = tuple(
        tuple(
            tuple(entries) for entries in subdict.values()
        )
        for subdict in grouped_data.values()
    )

    if category_or_module == 'c':
        categoryType = ['c']
    elif category_or_module == 'm':
        categoryType = ['m']
    else:
        categoryType = []

    if createprojectmode == 1:
        logger.info(
            f'The table data of the selected table: "{table_name}" of draft project project: {project_name} v{projectVersion} fetched successfully')
        return render_template("table_createproj.html", project_id=project_id, project_name=project_name,
                               projectVersion=projectVersion, table_name=table_name, data=data, columns=columns,
                               field=field, projects=projects, table_info=table_info, exception=dat['exception'],
                               table_id=table_id, categories=categories, modules=modules, notes=notes,
                               categoryType=categoryType,
                               category_id=category_id, last_test_case_id=last_test_case_id,
                               createprojectmode=createprojectmode,
                               closed_projects=closed_projects, user=user, users=users, test_case_ids=test_case_ids,
                               newproject_incomplete=newproject_incomplete, all_projects=all_projects,
                               CreateTestCycleMode=0,
                               running_cycles=running_cycles, historical_cycles=historical_cycles)
    elif CreateTestCycleMode == 1:
        logger.info(
            f'The table data of the selected table: "{table_name}" of draft project: {project_name} v{projectVersion} fetched successfully')
        return render_template("table_createproj.html", project_id=project_id, project_name=project_name,
                               projectVersion=projectVersion, table_name=table_name, data=data, columns=columns,
                               field=field, projects=projects, table_info=table_info, exception=dat['exception'],
                               table_id=table_id, categories=categories, modules=modules, notes=notes,
                               categoryType=categoryType,
                               category_id=category_id, last_test_case_id=last_test_case_id,
                               createprojectmode=createprojectmode,
                               closed_projects=closed_projects, user=user, users=users, test_case_ids=test_case_ids,
                               newproject_incomplete=newproject_incomplete, all_projects=all_projects,
                               CreateTestCycleMode=CreateTestCycleMode, running_cycles=running_cycles,
                               historical_cycles=historical_cycles)


# This function is called from 'table_createproj.html', during the new test cycle creation, when a user selects or
# unselects a test case
@app.route('/save_selected_test_cases_to_db', methods=['GET', 'POST'])
def save_selected_test_cases_to_db():
    logger.info('Saving the selected table rows for creating test cycle into table acting as cache')
    if request.method == 'POST':
        # Get the selected items from the request
        rowId = request.json['rowId']
        test_case_id = request.json['test_case_id']
        projectId = request.json['projectId']
        tableId = request.json['tableId']
        row_manipulation = request.json['row_manipulation']


        # Connect to MySQL
        logger.info('Connecting to the Database')
        cursor = get_db()

        # Perform table operations: if a test case is selected then opeartion will be 'insert'. If a test case is
        # unselected, then it is removed
        if row_manipulation == 'insert':
            cursor.execute(
                f"INSERT INTO selected_test_cases_for_new_test_cycle VALUES ({rowId}, {tableId}, {projectId}, \"{test_case_id}\")")
            mysql.connection.commit()
        elif row_manipulation == 'delete':
            cursor.execute('SET sql_safe_updates=0')
            mysql.connection.commit()
            cursor.execute(
                f"DELETE FROM selected_test_cases_for_new_test_cycle WHERE row_id={rowId} AND table_id={tableId} AND project_id={projectId}")
            mysql.connection.commit()
        return jsonify({'SUCCESS': 'successful'})


# This function is called from 'left_menus_createproject.html' to create a new test cycle and fill test cycles and
# test cases reult tables
@app.route('/confirm_create_test_cycle', methods=['GET', 'POST'])
def confirm_create_test_cycle():
    # The project id, name and version of the project from which test cycle is created.
    project_id = int(request.args.get('project_id', ''))
    projectName = request.args.get('projectName', '')
    projectVersion = float(request.args.get('projectVersion', ''))

    # Connect to MySQL
    logger.info('Connecting to the Database')
    cursor = get_db()

    # Fetch new test cycle id number for the new test cycle of the project to be created. If there is no existing test
    # cycle for the project then the try-except below will assign the id for the new test cycle as 1.
    cursor.execute(f"SELECT MAX(test_cycle_id)+1 as test_cycle_id FROM test_cycles WHERE project_id={project_id}")
    new_test_cycle_id = cursor.fetchall()

    try:
        new_test_cycle_id = int(new_test_cycle_id[0]['test_cycle_id'])
    except:
        new_test_cycle_id = 1


    logger.info(
        f'Creating new test cycle with tst cycle id: {new_test_cycle_id} of draft project: {projectName} v{projectVersion}')

    # The table in the inner query has data for a single project id only because this function is called from create
    # test cycle mode in 'table_createproj.html'. The test cases selected from the above-mentioned mode belong to a
    # single project (the project opened in that script) and after creating the test cycle, the table in the inner query
    # will be truncated.
    # Fetch table_names data on the basis of table id, the ids of the tables from which test cases were selected
    cursor.execute(
        f"SELECT * FROM table_names WHERE table_id IN (SELECT DISTINCT (table_id) table_ids FROM selected_test_cases_for_new_test_cycle)")
    table_inf = cursor.fetchall()
    table_info = []
    for info in table_inf:
        if info['category_ids'] is not None:
            info['category_ids'] = json.loads(info['category_ids'])
        if info['module_ids'] is not None:
            info['module_ids'] = json.loads(info['module_ids'])
        table_info.append(info)
    table_info = tuple(table_info)
    session['table_info'] = table_info

    categories = session.get('categories')
    session['projectName'] = projectName
    session['projectVersion'] = projectVersion

    # To edit the tables which other tables reference to
    cursor.execute('SET FOREIGN_KEY_CHECKS = 0')
    mysql.connection.commit()

    # Insert the data into test_cycles for creating a test cycle, project_closed and test_cycle_completed values areis 0
    # specifying that work on project and test cycle is not completed, start_date specifies test cycle start date.
    query = f"INSERT INTO test_cycles (test_cycle_id, project_id, project_closed, test_cycle_completed, start_date) VALUES ({new_test_cycle_id}, {project_id}, 0, 0, now())"
    cursor.execute(query)
    mysql.connection.commit()

    query = f'INSERT INTO test_cases_result (test_id, test_case_id, table_id) select row_id, test_case_id, table_id from selected_test_cases_for_new_test_cycle order by table_id, row_id'
    cursor.execute(query)
    mysql.connection.commit()

    query = F'UPDATE test_cases_result SET test_cycle_id={new_test_cycle_id}, project_id={project_id} WHERE test_cycle_id IS NULL'
    cursor.execute(query)
    mysql.connection.commit()

    cursor.execute(
        'select tc.*, p.project_name, p.project_version from test_cycles tc join projects p on (tc.project_id = p.project_id)')
    run_resume_hist_cycles = cursor.fetchall()
    running_cycles = []
    historical_cycles = []

    # Separate projects based on project_closed value
    for rrhc in run_resume_hist_cycles:
        if rrhc['test_cycle_completed'] == 0:
            running_cycles.append(rrhc)
        elif rrhc['test_cycle_completed'] == 1:
            historical_cycles.append(rrhc)

    running_cycles = tuple(running_cycles)
    historical_cycles = tuple(historical_cycles)

    session['running_cycles'] = running_cycles
    session['historical_cycles'] = historical_cycles

    logger.info(
        f'New test cycle with tst cycle id: {new_test_cycle_id} of draft project: {projectName} v{projectVersion} created successfully')

    return redirect(
        url_for('dashboardrun', projectName=projectName, projectVersion=projectVersion,
                test_cycle_id=new_test_cycle_id))


# This function is called when 'admin' user wants to delete a test cycle. This is called from "top_menus.html" form
# That is rendered by the js script "top_menus_unordered_lists.js"
@app.route('/delete_test_cycle', methods=['GET', 'POST'])
def delete_test_cycle():
    project_id = int(request.args.get('project_id', ''))
    test_cycle_id = request.args.get('test_cycle_id', '')

    cursor = get_db()

    cursor.execute("SET sql_safe_updates=0")
    cursor.execute("SET FOREIGN_KEY_CHECKS=0")

    # Create a list to store table IDs
    table_id_list = []

    cursor.execute(f"SELECT DISTINCT table_id FROM table_names WHERE project_id={project_id}")
    table_ids = cursor.fetchall()
    for table_id in table_ids:
        table_id_list.append(table_id["table_id"])

    # Convert the list to a tuple
    table_id_tuple = tuple(table_id_list)

    cursor.execute(f"DELETE from test_cases_result where table_id in {table_id_tuple}")
    mysql.connection.commit()
    cursor.execute(f"DELETE FROM test_cycles where project_id={project_id} and test_cycle_id={test_cycle_id}")
    mysql.connection.commit()

    logger.info('Selected Test cycle deleted successfully')

    return redirect(url_for("index"))


# This is called when you want to go to the dashboard in edit mode for finalizing new project creation
# (where you can add, delete or remove test cases).
@app.route('/dashboardrun', methods=['GET', 'POST'])
@login_required
def dashboardrun():
    project_id = request.args.get('project_id', '')
    projectName = request.args.get('projectName', '')
    projectVersion = request.args.get('projectVersion', '')
    test_cycle_id = request.args.get('test_cycle_id', '')
    project_startdate = request.args.get('project_startdate', '')
    project_enddate = request.args.get('project_enddate', '')

    logger.info('Connecting to the Database')
    cursor = get_db()

    cursor.execute(
        f"SELECT project_id, project_name, project_version from projects where project_name='{projectName}' and project_version={projectVersion}")
    projs = cursor.fetchall()
    project_id = projs[0]['project_id']
    project_name = projs[0]['project_name']
    projectVersion = projs[0]['project_version']

    cursor.execute(
        f"SELECT * FROM table_names WHERE table_id IN (SELECT DISTINCT (table_id) table_ids FROM test_cases_result where test_cycle_id={test_cycle_id} and project_id={project_id})")
    table_inf = cursor.fetchall()

    projects = session.get('projects')
    categories = session.get('categories')
    modules = session.get('modules')
    closed_projects = session.get('closed_projects')
    newproject_incomplete = session.get('newproject_incomplete')
    all_projects = session.get('all_projects')
    running_cycles = session.get('running_cycles')
    historical_cycles = session.get('historical_cycles')
    user = session.get('user')
    users = session.get('users')

    session['projectName'] = projectName
    session['projectVersion'] = projectVersion
    table_info = []
    for info in table_inf:
        if info['category_ids'] is not None:
            info['category_ids'] = json.loads(info['category_ids'])
        if info['module_ids'] is not None:
            info['module_ids'] = json.loads(info['module_ids'])
        table_info.append(info)
    table_info = tuple(table_info)
    session['table_info'] = table_info
    return render_template("dashboardrun.html", project_id=project_id, project_name=project_name,
                           projectVersion=projectVersion, projects=projects, table_info=table_info,
                           categories=categories,
                           modules=modules, test_cycle_id=test_cycle_id, closed_projects=closed_projects,
                           project_startdate=project_startdate, project_enddate=project_enddate,
                           newproject_incomplete=newproject_incomplete,
                           all_projects=all_projects, running_cycles=running_cycles,
                           historical_cycles=historical_cycles,
                           user=user, users=users)


# This will be called during run project when a table on left menus, rendered by left_menus_run, is clicked and the
# user can edit Remarks and Actual Result for test cases.
@app.route('/tablerun', methods=['GET', 'POST'])
@login_required
def tablerun():
    table_id = int(request.args.get('table_id', ''))
    table_name = request.args.get('table_name', '')
    project_id = int(request.args.get('project_id', ''))
    test_cycle_id = int(request.args.get('test_cycle_id', ''))
    project_startdate = request.args.get('project_startdate', '')
    project_enddate = request.args.get('project_enddate', '')
    try:
        category_id = int(request.args.get('category_id', ''))
    except:
        category_id = request.args.get('category_id', '')
    try:
        module_id = int(request.args.get('module_id', ''))
    except:
        module_id = request.args.get('module_id', '')

    category_or_module = request.args.get('category_module_type', '')

    selected_filter_value: str = request.args.get('selected_filter_value', '')

    # Saving it because when editing test cases Actual Results or Remarks the current function is called from other
    # functions in main.py and the 'category_or_module' is sent here from those modules by getting its value from the
    # session e.g., session.get('category_module_type')
    session['category_module_type'] = category_or_module

    categories = session.get('categories')
    modules = session.get('modules')

    # Connect to MySQL server
    cursor = get_db()

    cursor.execute(f"SELECT * from table_names where table_id={table_id}")
    dat = cursor.fetchall()
    dat = dat[0]
    columns = []
    field = []
    if dat['exception'] == 1:
        table = table_name.lower()
        table = table.replace(' ', '_')

        # check if the table has prefix
        try:
            check_prefix = dat['table_prefix'] > 0
        except:
            check_prefix = False

        # If the table has prefix then append it to the "table"
        if check_prefix:
            table = table + "_" + str(dat['table_prefix'])

        cursor.execute(f"DESCRIBE {table}")
        fetched_data = cursor.fetchall()
        cols = ""
        # In this case, the 'actual_result' and 'remarks' will be taken from test_case_result using table JOINS
        # but both of them should be appended to fields and columns lists as they will be used further
        for fd in fetched_data:
            if fd['Field'] not in ['actual_result', 'remarks', 'project_id', 'table_id']:
                cols = cols + f"a.{fd['Field']}, "
                x = str(fd['Field'])
                field.append(x)
                x = x.replace('_', ' ')
                x = x.title()
                columns.append(x.replace("Id", "ID"))
            elif fd['Field'] in ['actual_result', 'remarks']:
                x = str(fd['Field'])
                field.append(x)
                x = x.replace('_', ' ')
                x = x.title()
                columns.append(x.replace("Id", "ID"))

        cols = cols[:-2]

        # Join on both a.id = b.test_id and a.test_case_id=b.test_case_id and where test_cycle_id, this is so
        # because each table, master test cases and exception tables, have their own ids starting from 0, but
        # different test case ids, join only on ids can result in multiple rows, rows from master test cases and
        # exception tables. Test cycle id is important because if a project is run again, same rows will be inserted
        # to test case results table but will have different test cycle id value than previous run for same project
        if selected_filter_value == "All" or selected_filter_value == "":
            cursor.execute(
                f"SELECT {cols}, b.actual_result, b.remarks FROM {table} a JOIN test_cases_result b ON(a.id = b.test_id and a.table_id=b.table_id AND a.project_id=b.project_id) WHERE b.test_cycle_id={test_cycle_id} AND a.table_id={table_id} AND a.project_id={project_id} ORDER BY a.test_case_id")
        elif selected_filter_value == "Passed":
            cursor.execute(
                f"SELECT {cols}, b.actual_result, b.remarks FROM {table} a JOIN test_cases_result b ON(a.id = b.test_id and a.table_id=b.table_id AND a.project_id=b.project_id) WHERE b.test_cycle_id={test_cycle_id} AND a.table_id={table_id} AND a.project_id={project_id} AND b.actual_result='Pass' ORDER BY a.test_case_id")
        elif selected_filter_value == "Failed":
            cursor.execute(
                f"SELECT {cols}, b.actual_result, b.remarks FROM {table} a JOIN test_cases_result b ON(a.id = b.test_id and a.table_id=b.table_id AND a.project_id=b.project_id) WHERE b.test_cycle_id={test_cycle_id} AND a.table_id={table_id} AND a.project_id={project_id} AND b.actual_result not in ('Skipped', 'Pass') ORDER BY a.test_case_id")
        elif selected_filter_value == "Skipped":
            cursor.execute(
                f"SELECT {cols}, b.actual_result, b.remarks FROM {table} a JOIN test_cases_result b ON(a.id = b.test_id and a.table_id=b.table_id AND a.project_id=b.project_id) WHERE b.test_cycle_id={test_cycle_id} AND a.table_id={table_id} AND a.project_id={project_id} AND (b.actual_result = 'Skipped' OR b.actual_result is NULL) ORDER BY a.test_case_id")
        datta = cursor.fetchall()

        # for test_case_ids, we have to get the prefix and maximum id for that prefix, the result will be sent to the
        # add test case form where max test case id will already be entered from the result, the try except sees if the
        # tes case id is float (e.g., '1.1' in DA UAT) or has a prefix (e.g., 'TCSS1' in Redundancy test cases) before
        # it, for these cases different MySQL queries will be run to fetch the prefix and its maximum number (prefix)
        # make sure to add 1 to the number/prefix as it will be the new max number for new test case id
        try:
            try_float = float(datta[0]['test_case_id'])
            try_float = 1
        except:
            try_float = 0

        if try_float == 1:
            cursor.execute(
                f"select whole_number_part as prefix, max(decimal_part)+1 decimal_part FROM (SELECT replace(test_case_id, REGEXP_SUBSTR(test_case_id,'([0-9]*[.])?[0-9]+'), '') as prefix, convert(substring_index(REGEXP_SUBSTR(test_case_id,'([0-9]*[.])?[0-9]+'), '.', 1), float) whole_number_part, convert(substring_index(REGEXP_SUBSTR(test_case_id,'([0-9]*[.])?[0-9]+'), '.', -1), float) decimal_part FROM {table} WHERE table_id={dat['table_id']}) t group by whole_number_part")
        else:
            cursor.execute(
                f"select CASE WHEN suff LIKE '\n%' THEN SUBSTRING(suff, 2) ELSE suff END AS prefix, max(whole_number_part)+1 whole_number_part FROM (SELECT replace(test_case_id, REGEXP_SUBSTR(test_case_id,'([0-9]*[.])?[0-9]+'), '') as suff, convert(substring_index(REGEXP_SUBSTR(test_case_id,'([0-9]*[.])?[0-9]+'), '.', 1), float) whole_number_part, convert(substring_index(REGEXP_SUBSTR(test_case_id,'([0-9]*[.])?[0-9]+'), '.', -1), float) decimal_part FROM {table} WHERE table_id={dat['table_id']}) t group by prefix")

        last_test_case_id = cursor.fetchall()

        # The above queries will fetch either whole_number_part or decimal_part along with 'prefix' from MySQL, hence the try-except
        # To convert it to json in js script, the keys should be enclosed in double quotes
        try:
            last_test_case_id = [{"prefix": item['prefix'], "decimal_part": item['decimal_part']} for item in
                                 last_test_case_id]
        except:
            last_test_case_id = [{"prefix": item['prefix'], "whole_number_part": item['whole_number_part']} for item in
                                 last_test_case_id]

    else:
        if isinstance(category_id, int):
            if selected_filter_value == "All" or selected_filter_value == "":
                cursor.execute(
                    f"SELECT a.id, a.test_case_id, a.test_case_type, a.test_case_description, a.prerequisites, a.steps_to_execute, a.expected_result, a.module_id, a.note_id, a.category_id, b.actual_result, b.remarks FROM master_test_cases a JOIN test_cases_result b ON(a.id = b.test_id and a.table_id=b.table_id AND a.project_id=b.project_id) WHERE b.test_cycle_id={test_cycle_id} AND a.table_id={dat['table_id']} AND a.project_id={project_id} and a.category_id={category_id} ORDER BY a.test_case_id")
            elif selected_filter_value == "Passed":
                cursor.execute(
                    f"SELECT a.id, a.test_case_id, a.test_case_type, a.test_case_description, a.prerequisites, a.steps_to_execute, a.expected_result, a.module_id, a.note_id, a.category_id, b.actual_result, b.remarks FROM master_test_cases a JOIN test_cases_result b ON(a.id = b.test_id and a.table_id=b.table_id AND a.project_id=b.project_id) WHERE b.test_cycle_id={test_cycle_id} AND a.table_id={dat['table_id']} AND a.project_id={project_id} and a.category_id={category_id} AND b.actual_result='Pass' ORDER BY a.test_case_id")
            elif selected_filter_value == "Failed":
                cursor.execute(
                    f"SELECT a.id, a.test_case_id, a.test_case_type, a.test_case_description, a.prerequisites, a.steps_to_execute, a.expected_result, a.module_id, a.note_id, a.category_id, b.actual_result, b.remarks FROM master_test_cases a JOIN test_cases_result b ON(a.id = b.test_id and a.table_id=b.table_id AND a.project_id=b.project_id) WHERE b.test_cycle_id={test_cycle_id} AND a.table_id={dat['table_id']} AND a.project_id={project_id} and a.category_id={category_id} AND b.actual_result not in ('Skipped', 'Pass') ORDER BY a.test_case_id")
            elif selected_filter_value == "Skipped":
                cursor.execute(
                    f"SELECT a.id, a.test_case_id, a.test_case_type, a.test_case_description, a.prerequisites, a.steps_to_execute, a.expected_result, a.module_id, a.note_id, a.category_id, b.actual_result, b.remarks FROM master_test_cases a JOIN test_cases_result b ON(a.id = b.test_id and a.table_id=b.table_id AND a.project_id=b.project_id) WHERE b.test_cycle_id={test_cycle_id} AND a.table_id={dat['table_id']} AND a.project_id={project_id} and a.category_id={category_id} AND (b.actual_result = 'Skipped' OR b.actual_result is NULL) ORDER BY a.test_case_id")
        elif isinstance(module_id, int):
            if selected_filter_value == "All" or selected_filter_value == "":
                cursor.execute(
                    f"SELECT a.id, a.test_case_id, a.test_case_type, a.test_case_description, a.prerequisites, a.steps_to_execute, a.expected_result, a.module_id, a.note_id, a.category_id, b.actual_result, b.remarks FROM master_test_cases a JOIN test_cases_result b ON(a.id = b.test_id and a.table_id=b.table_id AND a.project_id=b.project_id) WHERE b.test_cycle_id={test_cycle_id} AND a.table_id={dat['table_id']} AND a.project_id={project_id} and a.module_id={module_id} ORDER BY a.test_case_id")
            elif selected_filter_value == "Passed":
                cursor.execute(
                    f"SELECT a.id, a.test_case_id, a.test_case_type, a.test_case_description, a.prerequisites, a.steps_to_execute, a.expected_result, a.module_id, a.note_id, a.category_id, b.actual_result, b.remarks FROM master_test_cases a JOIN test_cases_result b ON(a.id = b.test_id and a.table_id=b.table_id AND a.project_id=b.project_id) WHERE b.test_cycle_id={test_cycle_id} AND a.table_id={dat['table_id']} AND a.project_id={project_id} and a.module_id={module_id} AND b.actual_result='Pass' ORDER BY a.test_case_id")
            elif selected_filter_value == "Failed":
                cursor.execute(
                    f"SELECT a.id, a.test_case_id, a.test_case_type, a.test_case_description, a.prerequisites, a.steps_to_execute, a.expected_result, a.module_id, a.note_id, a.category_id, b.actual_result, b.remarks FROM master_test_cases a JOIN test_cases_result b ON(a.id = b.test_id and a.table_id=b.table_id AND a.project_id=b.project_id) WHERE b.test_cycle_id={test_cycle_id} AND a.table_id={dat['table_id']} AND a.project_id={project_id} and a.module_id={module_id} AND b.actual_result not in ('Skipped', 'Pass') ORDER BY a.test_case_id")
            elif selected_filter_value == "Skipped":
                cursor.execute(
                    f"SELECT a.id, a.test_case_id, a.test_case_type, a.test_case_description, a.prerequisites, a.steps_to_execute, a.expected_result, a.module_id, a.note_id, a.category_id, b.actual_result, b.remarks FROM master_test_cases a JOIN test_cases_result b ON(a.id = b.test_id and a.table_id=b.table_id AND a.project_id=b.project_id) WHERE b.test_cycle_id={test_cycle_id} AND a.table_id={dat['table_id']} AND a.project_id={project_id} and a.module_id={module_id} AND (b.actual_result = 'Skipped' OR b.actual_result is NULL) ORDER BY a.test_case_id")
        else:
            if selected_filter_value == "All" or selected_filter_value == "":
                cursor.execute(
                    f"SELECT a.id, a.test_case_id, a.test_case_type, a.test_case_description, a.prerequisites, a.steps_to_execute, a.expected_result, a.module_id, a.note_id, a.category_id, b.actual_result, b.remarks FROM master_test_cases a JOIN test_cases_result b ON(a.id = b.test_id and a.table_id=b.table_id AND a.project_id=b.project_id) WHERE b.test_cycle_id={test_cycle_id} AND a.table_id={dat['table_id']} AND a.project_id={project_id} ORDER BY a.test_case_id")
            elif selected_filter_value == "Passed":
                cursor.execute(
                    f"SELECT a.id, a.test_case_id, a.test_case_type, a.test_case_description, a.prerequisites, a.steps_to_execute, a.expected_result, a.module_id, a.note_id, a.category_id, b.actual_result, b.remarks FROM master_test_cases a JOIN test_cases_result b ON(a.id = b.test_id and a.table_id=b.table_id AND a.project_id=b.project_id) WHERE b.test_cycle_id={test_cycle_id} AND a.table_id={dat['table_id']} AND a.project_id={project_id} AND b.actual_result='Pass' ORDER BY a.test_case_id")
            elif selected_filter_value == "Failed":
                cursor.execute(
                    f"SELECT a.id, a.test_case_id, a.test_case_type, a.test_case_description, a.prerequisites, a.steps_to_execute, a.expected_result, a.module_id, a.note_id, a.category_id, b.actual_result, b.remarks FROM master_test_cases a JOIN test_cases_result b ON(a.id = b.test_id and a.table_id=b.table_id AND a.project_id=b.project_id) WHERE b.test_cycle_id={test_cycle_id} AND a.table_id={dat['table_id']} AND a.project_id={project_id} AND b.actual_result not in ('Skipped', 'Pass') ORDER BY a.test_case_id")
            elif selected_filter_value == "Skipped":
                cursor.execute(
                    f"SELECT a.id, a.test_case_id, a.test_case_type, a.test_case_description, a.prerequisites, a.steps_to_execute, a.expected_result, a.module_id, a.note_id, a.category_id, b.actual_result, b.remarks FROM master_test_cases a JOIN test_cases_result b ON(a.id = b.test_id and a.table_id=b.table_id AND a.project_id=b.project_id) WHERE b.test_cycle_id={test_cycle_id} AND a.table_id={dat['table_id']} AND a.project_id={project_id} AND (b.actual_result = 'Skipped' OR b.actual_result is NULL) ORDER BY a.test_case_id")

        columns = ['ID', 'Test Case ID', 'Test Case Type', 'Test Case Description', 'Prerequisites', 'Steps To Execute',
                   'Expected Result', 'Actual Result', 'Remarks', 'Module ID', 'Note ID', 'Category ID']
        field = ['id', 'test_case_id', 'test_case_type', 'test_case_description', 'prerequisites', 'steps_to_execute',
                 'expected_result', 'actual_result', 'remarks', 'module_id', 'note_id', 'category_id']
        datta = cursor.fetchall()

        try:
            try_float = float(datta[0]['test_case_id'])
            try_float = 1
        except:
            try_float = 0

        if try_float == 1:
            cursor.execute(
                f"select whole_number_part as prefix, max(decimal_part)+1 decimal_part FROM (SELECT replace(test_case_id, REGEXP_SUBSTR(test_case_id,'([0-9]*[.])?[0-9]+'), '') as prefix, convert(substring_index(REGEXP_SUBSTR(test_case_id,'([0-9]*[.])?[0-9]+'), '.', 1), float) whole_number_part, convert(substring_index(REGEXP_SUBSTR(test_case_id,'([0-9]*[.])?[0-9]+'), '.', -1), float) decimal_part FROM master_test_cases WHERE table_id={dat['table_id']}) t group by whole_number_part")
        else:
            cursor.execute(
                f"select CASE WHEN suff LIKE '\n%' THEN SUBSTRING(suff, 2) ELSE suff END AS prefix, max(whole_number_part)+1 whole_number_part FROM (SELECT replace(test_case_id, REGEXP_SUBSTR(test_case_id,'([0-9]*[.])?[0-9]+'), '') as suff, convert(substring_index(REGEXP_SUBSTR(test_case_id,'([0-9]*[.])?[0-9]+'), '.', 1), float) whole_number_part, convert(substring_index(REGEXP_SUBSTR(test_case_id,'([0-9]*[.])?[0-9]+'), '.', -1), float) decimal_part FROM master_test_cases WHERE table_id={dat['table_id']}) t group by prefix")

        last_test_case_id = cursor.fetchall()

        try:
            last_test_case_id = [{"prefix": item['prefix'], "decimal_part": item['decimal_part']} for item in
                                 last_test_case_id]
        except:
            last_test_case_id = [{"prefix": item['prefix'], "whole_number_part": item['whole_number_part']} for item in
                                 last_test_case_id]


    # If any value is None, then None will be sent as an object and not as a string,
    # which will not open the edit test case form
    data = ()
    for drd in datta:
        dr = {key: value if value is not None else '' for key, value in drd.items()}
        data = data + (dr,)

    cursor.execute(f"SELECT project_name, project_version from projects where project_id={project_id}")
    projs = cursor.fetchall()
    session['columns'] = columns
    session['field'] = field
    project_name = projs[0]['project_name']
    projectVersion = projs[0]['project_version']
    projects = session.get('projects')
    table_info = session.get('table_info')
    notes = session.get('notes')
    closed_projects = session.get('closed_projects')
    newproject_incomplete = session.get('newproject_incomplete')
    all_projects = session.get('all_projects')
    running_cycles = session.get('running_cycles')
    historical_cycles = session.get('historical_cycles')
    user = session.get('user')
    users = session.get('users')

    # Use a set comprehension and Iterate through the list and add unique category_ids to the set and exclude value 0
    # category_ids_set = {entry['category_id'] for entry in data if entry['category_id'] not in (0, '')}
    # # Some of the data has no category ids
    # if len(category_ids_set) > 0:
    #     # Create categoryType using a dictionary comprehension
    #     # Before accessing categories[str(category_id)], you might want to ensure that the category_id
    #     # exists in the categories dictionary to avoid potential KeyError.
    #     categoryType = {category_id: categories.get(str(category_id), [])[1] for category_id in category_ids_set}
    #
    #     # Extract unique values from the dictionary values using a set and convert to list.
    #     # This parameter should be sent to the 'tablerun' to create module/category dropdown menus in 'edit'
    #     # and 'add' forms module/category will be created based the cat_type values of categories
    #     categoryType = list(set(categoryType.values()))
    #
    # else:
    #     # Send empty list if data has no parts belonging to a module or any category
    #     categoryType = []
    # data = tuple(sorted(data, key=lambda x: x['module_id']))

    # Group data based on se_id and se_version
    grouped_data = {}
    for entry in data:
        if category_or_module == 'c':
            catid = entry['category_id']
        elif category_or_module == 'm':
            catid = entry['module_id']
        else:
            catid = entry['category_id']
        note = entry['note_id']

        if catid not in grouped_data:
            grouped_data[catid] = {}

        if note not in grouped_data[catid]:
            grouped_data[catid][note] = []

        grouped_data[catid][note].append(entry)

    # Convert the dictionary values to tuples
    data = tuple(
        tuple(
            tuple(entries) for entries in subdict.values()
        )
        for subdict in grouped_data.values()
    )

    if len(project_enddate) == 0:
        return render_template("tablerun.html", project_id=project_id, project_name=project_name,
                               projectVersion=projectVersion, table_name=table_name, data=data, columns=columns,
                               field=field, projects=projects, table_info=table_info, exception=dat['exception'],
                               table_id=table_id, categories=categories, modules=modules, notes=notes,
                               module_id=module_id,
                               category_id=category_id, test_cycle_id=test_cycle_id,
                               last_test_case_id=last_test_case_id,
                               closed_projects=closed_projects, newproject_incomplete=newproject_incomplete,
                               all_projects=all_projects, running_cycles=running_cycles,
                               historical_cycles=historical_cycles,
                               user=user, users=users, category_or_module=category_or_module,
                               selected_filter_value=selected_filter_value)
    else:
        return render_template("tablehist.html", project_id=project_id, project_name=project_name,
                               projectVersion=projectVersion, table_name=table_name, data=data, columns=columns,
                               field=field, projects=projects, table_info=table_info, exception=dat['exception'],
                               table_id=table_id, categories=categories, modules=modules, notes=notes,
                               category_id=category_id, test_cycle_id=test_cycle_id,
                               last_test_case_id=last_test_case_id,
                               closed_projects=closed_projects, project_startdate=project_startdate,
                               project_enddate=project_enddate,
                               newproject_incomplete=newproject_incomplete, all_projects=all_projects,
                               running_cycles=running_cycles,
                               historical_cycles=historical_cycles, user=user, users=users)


# When a new test case is added or an existing test case is edited in the draft project mode, the html is
# table_createproject.html, this function is called to add or edit test cases.
@app.route('/AddEditTestCase', methods=['GET', 'POST'])
def AddEditTestCase():
    table_name = request.args.get('table_name', '')
    project_id = int(request.args.get('project_id', ''))
    try:
        test_cycle_id = int(request.args.get('test_cycle_id', ''))
    except:
        test_cycle_id = request.args.get('test_cycle_id', '')

    try:
        row_id = int(request.args.get('row_id', ''))
    except:
        row_id = request.args.get('row_id', '')

    try:
        exception = int(request.args.get('exception', ''))
    except:
        exception = request.args.get('exception', '')

    table_id = int(request.args.get('table_id', ''))

    try:
        categoryid = int(request.args.get('category_id', ''))
    except:
        categoryid = request.args.get('category_id', '')

    try:
        module_id = int(request.args.get('module_id', ''))
    except:
        module_id = request.args.get('module_id', '')

    createprojectmode = request.args.get('createprojectmode', '')

    categories = session.get('categories')

    logger.info('Connecting to the Database')
    cursor = get_db()

    # Used to filter test cases based on their modules and categories, also used to insert
    # module and category names for test cases with different modules and categories
    cursor.execute("SELECT * from modules")
    modules = cursor.fetchall()
    modules = {item['module_id']: [item['module_name'], item['project_id']] for item in modules}

    # table_info = session.get('table_info')
    # table_desc = [inf for inf in table_info if inf['table_id'] == table_id]

    form_data = request.form

    # Convert to a regular dictionary, otherwise on deleting any item from the form_data will
    # give error: 'TypeError: 'ImmutableMultiDict' objects are immutable'
    form_data = dict(form_data)

    last_key = list(form_data.keys())[-1]

    # When adding or editing test cases, the submit button has id 'Add' and it is same for both edit and add test case
    # data form. Bt the values change, for adding, its values is 'Add' and for editing its value is 'Save'. But when
    # adding test case data, the form does not send submit key and its value so 'Add' key with value 'Add' will not be
    # in form_data. Hence, we have to store the value 'Add' in variable 'action' separately if last key is not 'Add'
    if last_key == 'Add':
        # Save the action 'Add'/'Save' before deleting it from the data
        action = form_data[last_key]

        # Remove the last item from the form_data dictionary, it is basically just the names of form buttons 'save'/'edit'
        del form_data[last_key]
    else:
        action = 'Add'

    fieldcheck = []
    if exception == 1:
        table = table_name.lower()
        table = table.replace(' ', '_')

        cursor.execute(f"SELECT * from table_names where table_id={table_id}")
        dat = cursor.fetchall()
        dat = dat[0]

        # check if the table has prefix
        try:
            check_prefix = dat['table_prefix'] > 0
        except:
            check_prefix = False

        # If the table has prefix then append it to the "table"
        if check_prefix:
            table = table + "_" + str(dat['table_prefix'])

        cursor.execute(f"DESCRIBE {table}")
        fetched_data = cursor.fetchall()
        for fd in fetched_data:
            if fd['Field'] in ['actual_result', 'remarks']:
                fieldcheck.append(fd['Field'])

    # An outer if to deal with Sanity Test Calls which do not have 'Actual Result', 'Reason For Fail' and
    # 'Remarks' Keys, remove it once resolved
    if exception == 1:
        if 'Actual Result' not in form_data and 'actual_result' in fieldcheck:
            form_data['Actual Result'] = 'Skipped'

        elif 'Actual Result' in form_data:
            if form_data['Actual Result'] == 'Fail':
                if len(form_data['Reason For Fail']) < 1:
                    form_data['Actual Result'] = 'Fail'
                else:
                    form_data['Actual Result'] = form_data['Reason For Fail']

    else:
        if 'Actual Result' not in form_data:
            form_data['Actual Result'] = 'Skipped'
        elif form_data['Actual Result'] == 'Fail':
            if len(form_data['Reason For Fail']) < 1:
                form_data['Actual Result'] = 'Fail'
            else:
                form_data['Actual Result'] = form_data['Reason For Fail']

    # A try to deal with Sanity Test Calls which do not have 'Actual Result', 'Reason For Fail' and 'Remarks'
    # Keys, delete it once resolved
    try:
        del form_data['Reason For Fail']
    except:
        pass

    columns = []
    field = []
    fieldtype = []
    valueslist = []
    colslist = []
    cols = ""

    # if the table has no categories/modules, then their values will be inserted as null in the database
    module_id = 'NULL'
    category_id = 'NULL'

    # if in create project edit mode, then remove the values of 'actual_result' and 'remarks' from valueslist and cols
    # colslist will be used for adding test cases or editing test cases so in editing option we have to make sure that
    # no values are added in 'remarks' or 'actual_result'. also 'actual_result' get default value skipped coded above
    # for run projects functionality
    if not isinstance(test_cycle_id, int):
        try:
            del form_data['Remarks']
        except:
            pass
        try:
            del form_data['Actual Result']
        except:
            pass

    for key, value in form_data.items():
        if key == 'Moduless':
            module_name = value
            module_id = [key for key, value in modules.items() if value[0] == module_name][0]

            # The modules are also inserted in category_id column as this column is the one that actually groups the
            # data into modules/categories
            # category_id = [key for key, value in categories.items() if value[0] == module_name][0]
            category_id = 'NULL'
        elif key == 'Categoryss':
            module_id = 'NULL'
            category_name = value

            # When adding test cases from 'all test cases' in left menus, then category id value sent/received is 'None'
            category_id = [key for key, value in categories.items() if value == category_name][0]

        else:
            x = key
            columns.append(x)
            x = x.replace(' ', '_')
            x = x.lower()

            # append column names to field (the column names in SQL)
            field.append(x)
            cols = cols + f"{x}, "

            # Append new values to the valaus list
            valueslist.append(value)

            colslist.append(x)

    # In new tables, if a new test case is added with a module or category, then the category_ids column in
    # table_names should be filled with the module or category id if it does not have it already.
    table_info = session.get('table_info')
    # cursor.execute(f"SELECT * from table_names where project_id={project_id}")
    # table_inf = cursor.fetchall()
    # table_info = []
    # for info in table_inf:
    #     if info['category_ids'] is not None:
    #         info['category_ids'] = json.loads(info['category_ids'])
    #     table_info.append(info)
    # table_info = tuple(table_info)

    if category_id != 'NULL':
        category_id = int(category_id)
        for info in table_info:
            if table_name in info['table_name']:
                if info['category_ids'] == None:
                    info['category_ids'] = [category_id]
                elif category_id not in info['category_ids']:
                    table = table_name.lower()
                    table = table.replace(' ', '_')
                    info['category_ids'].append(category_id)
                    query = f'UPDATE table_names SET category_ids=\"{info["category_ids"]}\" WHERE table_id={table_id}'
                    cursor.execute(query)
                    mysql.connection.commit()

    session['table_info'] = table_info

    cols = cols[:-2]
    # When creating queries, quotes will create problems. if string is enclosed in '' then it will give syntax
    # error if the string has a ' character. adding '\' to the quote will mitigate the problem
    for i in range(len(valueslist)):
        valueslist[i] = valueslist[i].replace('"', '\\"')
        valueslist[i] = valueslist[i].replace("'", "\\'")

    if exception == 1:
        table = table_name.lower()
        table = table.replace(' ', '_')

        cursor.execute(f"SELECT * from table_names where table_id={table_id}")
        dat = cursor.fetchall()
        dat = dat[0]

        # check if the table has prefix
        try:
            check_prefix = dat['table_prefix'] > 0
        except:
            check_prefix = False

        # If the table has prefix then append it to the "table"
        if check_prefix:
            table = table + "_" + str(dat['table_prefix'])

        cursor.execute(f"DESCRIBE {table}")
        fetched_data = cursor.fetchall()
        for fd in fetched_data:
            if fd['Field'] not in ['id', 'project_id', 'table_id', 'module_id', 'note_id', 'category_id']:
                fieldtype.append(fd['Type'])


        setvals = 'SET '
        for i in range(len(colslist)):
            if fieldtype[i] != 'int':
                setvals = setvals + f"{colslist[i]} = " + '"' + valueslist[i] + '", '
            else:
                # If int values are empty make sure to set them as NULL otherwise the query will be like "intcolumn= ,"
                if len(valueslist[i]) == 0:
                    setvals = setvals + f"{colslist[i]} = NULL, "
                else:
                    setvals = setvals + f"{colslist[i]} = " + valueslist[i] + ', '
        setvals = setvals[:-2]

        values = ""
        for i in range(len(valueslist)):
            if fieldtype[i] != 'int':
                if len(valueslist[i]) == 0:
                    values = values + 'NULL, '
                else:
                    values = values + '"' + valueslist[i] + '", '
            else:
                if len(valueslist[i]) == 0:
                    values = values + 'NULL, '
                else:
                    values = values + valueslist[i] + ', '
        values = values[:-2]

        if action == 'Add':
            query = f'INSERT INTO {table} ({cols}, project_id, table_id, module_id, note_id, category_id) VALUES ({values}, {project_id}, {table_id}, {module_id}, NULL, {category_id})'
            cursor.execute(query)
            mysql.connection.commit()

            query = f'SELECT id FROM {table} ORDER BY id DESC LIMIT 1'
            cursor.execute(query)
            id = cursor.fetchall()
            id = id[0]['id']
    else:
        cursor.execute(f"DESCRIBE master_test_cases")
        fetched_data = cursor.fetchall()
        for fd in fetched_data:
            if fd['Field'] not in ['id', 'project_id', 'table_id', 'module_id', 'note_id', 'category_id']:
                fieldtype.append(fd['Type'])


        setvals = 'SET '
        for i in range(len(colslist)):
            if fieldtype[i] != 'int':
                setvals = setvals + f"{colslist[i]} = " + '"' + valueslist[i] + '", '
            else:
                setvals = setvals + f"{colslist[i]} = " + valueslist[i] + ', '
        setvals = setvals[:-2]

        values = ""
        for i in range(len(valueslist)):
            if fieldtype[i] != 'int':
                values = values + '"' + valueslist[i] + '", '
            else:
                values = values + valueslist[i] + ', '
        values = values[:-2]

        if action == 'Add':
            query = f'INSERT INTO master_test_cases ({cols}, project_id, table_id, module_id, note_id, category_id) VALUES ({values}, {project_id}, {table_id}, {module_id}, NULL, {category_id})'
            cursor.execute(query)
            mysql.connection.commit()

            query = f'SELECT id FROM master_test_cases ORDER BY id DESC LIMIT 1'
            cursor.execute(query)
            id = cursor.fetchall()
            id = id[0]['id']

    if action == 'Add' and isinstance(test_cycle_id, int):
        query = "SET FOREIGN_KEY_CHECKS = 0"
        cursor.execute(query)
        mysql.connection.commit()

        query = f'INSERT INTO test_cases_result (test_cycle_id, test_id, test_case_id, project_id) VALUES ({test_cycle_id}, {id}, "{valueslist[0]}", {project_id})'
        cursor.execute(query)
        mysql.connection.commit()
    elif action == 'Save' and isinstance(test_cycle_id, int):
        query = 'UPDATE test_cases_result SET '
        try:
            index = field.index('actual_result')
            query = query + f'{field[index]}="{valueslist[index]}", '
        except:
            pass
        try:
            index = field.index('remarks')
            query = query + f'{field[index]}="{valueslist[index]}", '
        except:
            pass

        query = query[:-2]
        query = query + f'WHERE test_id={row_id} AND table_id={table_id} AND test_cycle_id={test_cycle_id}'
        cursor.execute(query)
        mysql.connection.commit()
    elif action == 'Save':
        if exception == 1:
            query = f'UPDATE {table} {setvals} WHERE id={row_id}'
        else:
            query = f'UPDATE master_test_cases {setvals} WHERE id={row_id}'
        cursor.execute(query)
        mysql.connection.commit()

    # The Category ID sent should be categoryid and not category_id, because in some tables, the category_id is 'None'
    # and in this part of the code, the category_id value changes if its 'None'. categoryid stores the original value
    if isinstance(test_cycle_id, int):
        return redirect(url_for('tablerun', table_name=table_name, project_id=project_id, table_id=table_id,
                                category_id=categoryid, test_cycle_id=test_cycle_id,
                                category_module_type=session.get('category_module_type')))
    return redirect(url_for('table_createproj', table_name=table_name, project_id=project_id, table_id=table_id,
                            category_id=categoryid, createprojectmode=createprojectmode,
                            category_module_type=session.get('category_module_type')))


# This function is called when the test cases are selected from a CSV file opened on the dashboard and user proceeds
# to add these test cases to the table.
@app.route('/add_test_cases_from_csv', methods=['GET', 'POST'])
def add_test_cases_from_csv():
    # table_name = request.args.get('table_name', '')
    # project_id = int(request.args.get('project_id', ''))
    # try:
    #     exception = int(request.args.get('exception', ''))
    # except:
    #     exception = request.args.get('exception', '')
    #
    # table_id = int(request.args.get('table_id', ''))
    #
    # try:
    #     categoryid = int(request.args.get('category_id', ''))
    # except:
    #     categoryid = request.args.get('category_id', '')
    #
    # createprojectmode = request.args.get('createprojectmode', '')
    #
    # selected_rows_str = request.args.get('selectedRows', '')

    # Retrieve the JSON data sent in the request
    data = request.json
    # Process the received data
    selectedRows = data['selectedRows']
    table_name = data['table_name']
    table_id = int(data['table_id'])
    exception = data['exception']
    project_id = data['project_id']
    category_id = data['category_id']
    createprojectmode = data['createprojectmode']
    category_or_module = data['cat_mod']
    empty_table = data['empty_table']




    logger.info(f'Adding Test Cases From CSV into table: {table_name}')

    logger.info('Connecting to the Database')
    cursor = get_db()

    columns = []
    field = []
    fieldtype = []
    valueslist = []
    colslist = []
    cols = ""

    # if in create project edit mode, then remove the values of 'actual_result' and 'remarks' from valueslist and cols
    # colslist will be used for adding test cases or editing test cases so in editing option we have to make sure that
    # no values are added in 'remarks' or 'actual_result'. also 'actual_result' get default value skipped coded above
    # for run projects functionality

    # IN SHORT, the 'actual_result' and 'remarks' not be inserted
    selectedRows = [{k: v for k, v in row.items() if k.lower() not in ('remarks', 'actual result')} for row in
                    selectedRows]


    for key, value in selectedRows[0].items():
        x = key
        if x == 'module_id':
            cols = cols + "project_id, table_id, "
            colslist.append('project_id')
            colslist.append('table_id')
        elif x == 'category_id':
            cols = cols + "note_id, "
            colslist.append('note_id')

        x = x.replace(' ', '_')
        x = x.lower()

        cols = cols + f"{x}, "

        colslist.append(x)

    cols = cols[:-2]

    for ind in range(len(selectedRows)):
        valueslist.append([])
        for key, value in selectedRows[ind].items():

            if key == "module_id":
                valueslist[ind].append(project_id)
                valueslist[ind].append(table_id)
            elif key == "category_id":
                valueslist[ind].append("")

            # Append new values to the values list
            valueslist[ind].append(value)

        # When creating queries, quotes will create problems. if string is enclosed in '' then it will give syntax
        # error if the string has a ' character. adding '\' to the quote will mitigate the problem
        for i in range(len(valueslist[ind])):
            valueslist[ind][i] = str(valueslist[ind][i]).replace("\\", "\\\\")
            valueslist[ind][i] = str(valueslist[ind][i]).replace('"', '\\"')
            valueslist[ind][i] = str(valueslist[ind][i]).replace("'", "\\'")


    # Get the position of the test case ID from the list of table columns
    test_case_id_position = colslist.index('test_case_id')


    test_case_ids = session.get('test_case_ids')


    if exception == 1:
        table = table_name.lower()
        table = table.replace(' ', '_')

        cursor.execute(f"SELECT * from table_names where table_id={table_id}")
        dat = cursor.fetchall()
        dat = dat[0]

        # check if the table has prefix
        try:
            check_prefix = dat['table_prefix'] > 0
        except:
            check_prefix = False

        # If the table has prefix then append it to the "table"
        if check_prefix:
            table = table + "_" + str(dat['table_prefix'])

        cursor.execute(f"DESCRIBE {table}")
        fetched_data = cursor.fetchall()
        for fd in fetched_data:
            if fd['Field'] not in ['id', 'actual_result', 'remarks']:
                fieldtype.append(fd['Type'])

        query = f'INSERT INTO {table} ({cols}) VALUES '
        for ind in range(len(selectedRows)):
            values = ""
            for i in range(len(valueslist[ind])):
                if fieldtype[i] != 'int':
                    if len(valueslist[ind][i]) == 0:
                        # Check if the index is a test case id value
                        if i == test_case_id_position:
                            # Return error if test case id value is empty
                            return jsonify({'error': 'The Test Case ID Value Is Empty In One Of The Selected Columns'})
                        else:
                            values = values + 'NULL, '
                    else:
                        # Return error if the test case ID already exists
                        if i == test_case_id_position:
                            if str(valueslist[ind][i]) in test_case_ids:
                                return jsonify(
                                    {'error': f'The test case id "{valueslist[ind][i]}" already exists in the table'})

                        values = values + '"' + valueslist[ind][i] + '", '
                else:
                    if len(valueslist[ind][i]) == 0:
                        # Check if the index is a test case id value
                        if i == test_case_id_position:
                            # Return error if test case id value is empty
                            return jsonify({'error': 'The Test Case ID Value Is Empty In One Of The Selected Columns'})
                        else:
                            values = values + 'NULL, '
                    else:
                        # Return error if the test case ID already exists
                        if i == test_case_id_position:
                            if str(valueslist[ind][i]) in test_case_ids:
                                return jsonify(
                                    {'error': f'The test case id already "{valueslist[ind][i]}" exists in the table'})

                        values = values + valueslist[ind][i] + ', '
            values = values[:-2]

            query = query + f'({values}), '

        query = query[:-2]
        cursor.execute(query)
        mysql.connection.commit()

    else:
        cursor.execute(f"DESCRIBE master_test_cases")
        fetched_data = cursor.fetchall()
        for fd in fetched_data:
            if fd['Field'] not in ['id', 'actual_result', 'remarks']:
                fieldtype.append(fd['Type'])

        query = f'INSERT INTO master_test_cases ({cols}) VALUES '
        for ind in range(len(selectedRows)):
            values = ""
            for i in range(len(valueslist[ind])):
                if fieldtype[i] != 'int':
                    if len(valueslist[ind][i]) == 0:
                        # Check if the index is a test case id value
                        if i == test_case_id_position:
                            # Return error if test case id value is empty
                            return jsonify({'error': 'The Test Case ID Value Is Empty In One Of The Selected Columns'})
                        else:
                            values = values + 'NULL, '
                    else:
                        # Return error if the test case ID already exists
                        if i == test_case_id_position:
                            if str(valueslist[ind][i]) in test_case_ids:
                                return jsonify(
                                    {
                                        'error': f'The test case id "{valueslist[ind][i]}" already exists in the table'})

                        values = values + '"' + valueslist[ind][i] + '", '
                else:
                    if len(valueslist[ind][i]) == 0:
                        # Check if the index is a test case id value
                        if i == test_case_id_position:
                            # Return error if test case id value is empty
                            return jsonify({'error': 'The Test Case ID Value Is Empty In One Of The Selected Columns'})
                        else:
                            values = values + 'NULL, '
                    else:
                        # Return error if the test case ID already exists
                        if i == test_case_id_position:
                            if str(valueslist[ind][i]) in test_case_ids:
                                return jsonify(
                                    {
                                        'error': f'The test case id "{valueslist[ind][i]}" already exists in the table'})

                        values = values + valueslist[ind][i] + ', '
            values = values[:-2]

            query = query + f'({values}), '

        query = query[:-2]
        cursor.execute(query)
        mysql.connection.commit()

    # Set the category or module of the new table if the data is being inserted for the first time and has
    # categories/modules.
    if empty_table == 1:
        if category_or_module == 'm':
            query = f"update table_names set category_type = 'm' where `table_name` = '{table_name}' and project_id = {project_id} and table_id = {table_id}"
            cursor.execute(query)
            mysql.connection.commit()
        elif category_or_module == 'c':
            query = f"update table_names set category_type = 'c' where `table_name` = '{table_name}' and project_id = {project_id} and table_id = {table_id}"
            cursor.execute(query)
            mysql.connection.commit()

    # Update the module or category ids in the table_names row in MySQL
    table_info = session.get('table_info')
    if category_or_module == 'c':
        # Use a set comprehension to collect unique module_id values
        unique_cat_mod_ids = {int(d["category_id"]) for d in selectedRows}
        # Convert the set back to a list if needed
        unique_category_ids_list = list(unique_cat_mod_ids)
    elif category_or_module == 'm':
        # Use a set comprehension to collect unique module_id values
        unique_cat_mod_ids = {int(d["module_id"]) for d in selectedRows}
        # Convert the set back to a list if needed
        unique_module_ids_list = list(unique_cat_mod_ids)

    if category_or_module == 'c':
        for info in table_info:
            # Table_ID is being compared here because table names can be same for different projects
            if table_id == int(info['table_id']):
                if info['category_ids'] is None:
                    # If info['category_ids'] is 'None' then using the method in else statement will give error:
                    # argument of type 'NoneType' is not iterable
                    new_category_ids = unique_category_ids_list
                else:
                    # Find elements in unique_category_ids_list that are not in info['category_ids'] Or the category ids
                    # not in added to the table
                    new_category_ids = [category_id for category_id in unique_category_ids_list if
                                        category_id not in info['category_ids']]
                if new_category_ids:
                    table = table_name.lower()
                    table = table.replace(' ', '_')

                    # if info['category_ids'] is None then using "extend" will give error: 'NoneType' object has no
                    # attribute 'extend'
                    if info['category_ids'] is None:
                        info['category_ids'] = new_category_ids
                    else:
                        # The 'extend' method is used to add the elements of new_category_ids to info['category_ids']
                        info['category_ids'].extend(new_category_ids)

                    # Sort the combined list
                    info['category_ids'].sort()
                    query = f'UPDATE table_names SET category_ids=\"{info["category_ids"]}\" WHERE table_id={table_id}'
                    cursor.execute(query)
                    mysql.connection.commit()

    elif category_or_module == 'm':
        for info in table_info:
            # Table_ID is being compared here because table names can be same for different projects
            if table_id == int(info['table_id']):
                if info['module_ids'] is None:
                    # If info['module_ids'] is 'None' then using the method in else statement will give error:
                    # argument of type 'NoneType' is not iterable
                    new_module_ids = unique_module_ids_list
                else:
                    # Find elements in unique_module_ids_list that are not in info['module_ids'] Or the module ids not
                    # in added to the table
                    new_module_ids = [module_id for module_id in unique_module_ids_list if
                                      module_id not in info['module_ids']]
                if new_module_ids:
                    table = table_name.lower()
                    table = table.replace(' ', '_')
                    # if info['module_ids'] is None then using "extend" will give error: 'NoneType' object has no
                    # attribute 'extend'
                    if info['module_ids'] is None:
                        info['module_ids'] = new_module_ids
                    else:
                        # The 'extend' method is used to add the elements of new_module_ids to info['module_ids']
                        info['module_ids'].extend(new_module_ids)

                    # Sort the combined list
                    info['module_ids'].sort()
                    query = f'UPDATE table_names SET module_ids=\"{info["module_ids"]}\" WHERE table_id={table_id}'
                    cursor.execute(query)
                    mysql.connection.commit()

    session['table_info'] = table_info

    logger.info(f'Test cases added from CSV into table: {table_name} successfully')

    return jsonify({'ok': 'successfully inserted data into the table'})


# This function is called when the admin wants to delete a row from a table.
@app.route('/DeleteTestCase', methods=['GET', 'POST'])
def DeleteTestCase():
    table_name = request.args.get('table_name', '')
    project_id = int(request.args.get('project_id', ''))
    row_id = int(request.args.get('row_id', ''))
    test_cycle_id = request.args.get('test_cycle_id', '')
    try:
        exception = int(request.args.get('exception', ''))
    except:
        exception = request.args.get('exception', '')

    table_id = int(request.args.get('table_id', ''))
    categoryid = request.args.get('category_id', '')
    createprojectmode = request.args.get('createprojectmode', '')

    print('table_name: ', table_name, 'project_id: ', project_id, 'row_id: ', row_id, 'exception: ', exception,
          'table_id: ', table_id, 'categoryid: ', categoryid, 'test_cycle_id: ', type(test_cycle_id))

    logger.info(f'Deleting selected Test Case from table: {table_name}')

    logger.info('Connecting to the Database')
    cursor = get_db()

    cursor.execute('SET FOREIGN_KEY_CHECKS = 0')
    mysql.connection.commit()

    # tablecreate also has 'delete' option and the whole createproject functionality do not use test_cycle_id and do not
    # work with historical tables
    if isinstance(test_cycle_id, int):
        query = f'DELETE FROM test_cases_result WHERE test_id={row_id} AND test_cycle_id={test_cycle_id} AND project_id={project_id}'
        cursor.execute(query)
        mysql.connection.commit()

        query = f'ALTER TABLE test_cases_result AUTO_INCREMENT = 1'

        cursor.execute(query)
        mysql.connection.commit()

    if exception == 1:
        table = table_name.lower()
        table = table.replace(' ', '_')

        cursor.execute(f"SELECT * from table_names where table_id={table_id}")
        dat = cursor.fetchall()
        dat = dat[0]
        # check if the table has prefix
        try:
            check_prefix = dat['table_prefix'] > 0
        except:
            check_prefix = False

        # If the table has prefix then append it to the "table"
        if check_prefix:
            table = table + "_" + str(dat['table_prefix'])

        query = f'DELETE FROM {table} WHERE id={row_id}'

        cursor.execute(query)
        mysql.connection.commit()

        query = f'ALTER TABLE {table} AUTO_INCREMENT = 1'

        cursor.execute(query)
        mysql.connection.commit()

    else:
        query = f'DELETE FROM master_test_cases WHERE id={row_id}'

        cursor.execute(query)
        mysql.connection.commit()

        query = 'ALTER TABLE master_test_cases AUTO_INCREMENT = 1'

        cursor.execute(query)
        mysql.connection.commit()

    logger.info(f'Selected Test Case from table: {table_name} Deleted successfully')

    if isinstance(test_cycle_id, int):
        return redirect(url_for('tablerun', table_name=table_name, project_id=project_id, table_id=table_id,
                                category_id=categoryid, test_cycle_id=test_cycle_id,
                                category_module_type=session.get('category_module_type')))
    return redirect(url_for('table_createproj', table_name=table_name, project_id=project_id, table_id=table_id,
                            category_id=categoryid, createprojectmode=1,
                            category_module_type=session.get('category_module_type')))


@app.route('/CloseProject', methods=['GET', 'POST'])
def CloseProject():
    project_name = request.args.get('project_name', '')
    projectVersion = request.args.get('projectVersion', '')
    test_cycle_id = int(request.args.get('test_cycle_id', ''))

    cursor = get_db()

    cursor.execute('SET sql_safe_updates=0')
    mysql.connection.commit()

    cursor.execute(f'UPDATE test_cycles SET project_closed=1, end_date=now() WHERE test_cycle_id={test_cycle_id}')
    mysql.connection.commit()

    cursor.execute(f'select start_date, end_date from test_cycles where test_cycle_id={test_cycle_id}')
    project_dates = cursor.fetchall()
    project_startdate = project_dates[0]['start_date']
    project_enddate = project_dates[0]['end_date']


    return redirect(url_for('dashboardrun', projectName=project_name, projectVersion=projectVersion,
                            test_cycle_id=test_cycle_id, project_startdate=project_startdate,
                            project_enddate=project_enddate))


# This will be called when project is created and by clicking on create project and finalized, this will also notify
# in DB that the new project creation has been finalized and no more edits, deletion or addition of test cases are left.
@app.route('/FinalizeCreateProject', methods=['GET', 'POST'])
def FinalizeCreateProject():
    project_name = request.args.get('projectName', '')
    projectVersion = request.args.get('projectVersion', '')
    project_id = int(request.args.get('project_id', ''))

    cursor = get_db()

    cursor.execute('SET sql_safe_updates=0')
    mysql.connection.commit()

    # set project_created to 1 to ensure that the project has been created and no more edits are left
    cursor.execute(f'UPDATE projects SET project_created=1 WHERE project_id={project_id}')
    mysql.connection.commit()

    cursor.execute("SELECT project_name, project_version from projects WHERE project_created = 1")
    projs = cursor.fetchall()

    grouped_items = {}
    for item in projs:
        project_name = item['project_name']
        if project_name not in grouped_items:
            grouped_items[project_name] = []
        grouped_items[project_name].append(item['project_version'])

    # Create a new list of dictionaries
    closed_projects = [{'project_name': project_name, 'project_version': project_version} for
                       project_name, project_version in
                       grouped_items.items()]

    session['closed_projects'] = closed_projects

    # For resuming the new project creation functionality if left without clicking on create project
    cursor.execute("SELECT * FROM projects WHERE project_created <> 1")
    newprojectincomplete = cursor.fetchall()

    newproject_incomplete = []
    for newproject in newprojectincomplete:
        newproject_incomplete.append(newproject)

    session['newproject_incomplete'] = newproject_incomplete

    # For deleting projects
    cursor.execute("SELECT * FROM projects")
    allprojects = cursor.fetchall()

    all_projects = []
    for project in allprojects:
        all_projects.append(project)

    grouped_items = {}
    for item in allprojects:
        project_name = item['project_name']
        if project_name not in grouped_items:
            grouped_items[project_name] = []
        grouped_items[project_name].append(item['project_version'])

    projects = [{'project_name': project_name, 'project_version': project_version} for project_name, project_version in
                grouped_items.items()]

    session['projects'] = projects
    session['all_projects'] = all_projects

    # This will send the user to the dashboard/view page for the newly created project where he can view contents only.
    return redirect(url_for('dashboard', projectName=project_name, projectVersion=projectVersion))


# Called from "top_menus.html" admin wants to delete a project/ This function will delete the project data and its
# tables' details from MySQL database tables
@app.route('/delete_project', methods=['GET', 'POST'])
def delete_project():
    project_name = request.args.get('projectName', '')
    projectVersion = request.args.get('projectVersion', '')
    project_id = int(request.args.get('project_id', ''))


    logger.info(f'Deleting the selected project: {project_name} v{projectVersion}')

    logger.info('Connecting to the Database')
    cursor = get_db()

    cursor.execute('SET sql_safe_updates=0')
    mysql.connection.commit()

    cursor.execute('SET FOREIGN_KEY_CHECKS = 0')
    mysql.connection.commit()

    query = f'SELECT * FROM table_names WHERE project_id={project_id}'
    cursor.execute(query)
    del_tables_inf = cursor.fetchall()

    for info in del_tables_inf:
        if info['exception'] == 1:
            # The database table name of exception tables is just the lower case
            # form of the table name with ' ' replaced with '_'
            table = info['table_name'].lower()
            table = table.replace(' ', '_')

            # check if the table has prefix
            try:
                check_prefix = info['table_prefix'] > 0
            except:
                check_prefix = False

            # If the table has prefix then append it to the "table"
            if check_prefix:
                table = table + "_" + str(info['table_prefix'])

            cursor.execute(f"DELETE FROM {table} WHERE project_id={project_id}")
            mysql.connection.commit()

            query = f'ALTER TABLE {table} AUTO_INCREMENT = 1'
            cursor.execute(query)
            mysql.connection.commit()
        else:
            cursor.execute(f"DELETE FROM master_test_cases WHERE project_id={project_id}")
            mysql.connection.commit()

            query = 'ALTER TABLE master_test_cases AUTO_INCREMENT = 1'
            cursor.execute(query)
            mysql.connection.commit()

    query = f'DELETE FROM table_names WHERE project_id={project_id}'
    cursor.execute(query)
    mysql.connection.commit()

    query = 'ALTER TABLE table_names AUTO_INCREMENT = 1'
    cursor.execute(query)
    mysql.connection.commit()

    # set project_created to 1 to ensure that the project has been created and no more edits are left
    cursor.execute(f'DELETE FROM projects WHERE project_id={project_id}')
    mysql.connection.commit()

    query = 'ALTER TABLE projects AUTO_INCREMENT = 1'
    cursor.execute(query)
    mysql.connection.commit()

    query = f'SELECT * FROM table_names'
    cursor.execute(query)
    all_tables_inf = cursor.fetchall()

    all_tables_info = []
    for tables in all_tables_inf:
        if tables['exception'] == 1:
            if isinstance(tables['table_prefix'], int):
                all_tables_info.append(tables['table_name'] + "_" + str(tables['table_prefix']))
            else:
                all_tables_info.append(tables['table_name'])

    all_tables_info = list(set(all_tables_info))

    deleted_tables = []
    for info in del_tables_inf:
        if info['exception'] == 1:
            if isinstance(info['table_prefix'], int):
                deleted_tables.append(info['table_name'] + "_" + str(info['table_prefix']))
            else:
                deleted_tables.append(info['table_name'])

    deleted_tables = list(set(deleted_tables))

    drop_tables_list = [item for item in deleted_tables if item not in all_tables_info]

    for drop_table in drop_tables_list:
        table = drop_table.lower().replace(' ', '_')
        query = f'DROP TABLE {table}'
        cursor.execute(query)
        mysql.connection.commit()

    # Delete test cycles of the project to be deleted
    cursor.execute(f'DELETE FROM test_cycles WHERE project_id={project_id}')
    mysql.connection.commit()

    # Delete test cases result of the project to be deleted
    cursor.execute(f'DELETE FROM test_cases_result WHERE project_id={project_id}')
    mysql.connection.commit()

    query = 'ALTER TABLE test_cycles AUTO_INCREMENT = 1'
    cursor.execute(query)
    mysql.connection.commit()

    query = 'ALTER TABLE test_cases_result AUTO_INCREMENT = 1'
    cursor.execute(query)
    mysql.connection.commit()

    # For resuming the new project creation functionality if left without clicking on create project
    cursor.execute("SELECT * FROM projects WHERE project_created <> 1")
    newprojectincomplete = cursor.fetchall()

    newproject_incomplete = []
    for newproject in newprojectincomplete:
        newproject_incomplete.append(newproject)

    # For deleting projects
    cursor.execute("SELECT * FROM projects")
    allprojects = cursor.fetchall()

    all_projects = []
    for project in allprojects:
        all_projects.append(project)

    grouped_items = {}
    for item in allprojects:
        project_name = item['project_name']
        if project_name not in grouped_items:
            grouped_items[project_name] = []
        grouped_items[project_name].append(item['project_version'])

    projects = [{'project_name': project_name, 'project_version': project_version} for project_name, project_version in
                grouped_items.items()]

    session['projects'] = projects
    session['all_projects'] = all_projects
    session['newproject_incomplete'] = newproject_incomplete

    logger.info(f'Deleted the selected project: {project_name} v{projectVersion} successfully')
    return redirect(url_for('index'))


@app.route('/resumeandhistproject', methods=['GET', 'POST'])
def resumeandhistproject():
    projectName = request.args.get('project_name', '')
    projectVersion = request.args.get('project_version', '')
    projectName = request.args.get('project_name', '')
    projectVersion = request.args.get('project_version', '')
    projectName = request.args.get('project_name', '')
    projectVersion = request.args.get('project_version', '')
    closed_projects = session.get('closed_projects')

    cursor = get_db()

    cursor.execute(
        f"SELECT project_id, project_name, project_version from projects where project_name='{projectName}' and project_version={projectVersion}")
    projs = cursor.fetchall()
    project_id = projs[0]['project_id']
    project_name = projs[0]['project_name']
    projectVersion = projs[0]['project_version']


@app.route('/submit_test_cycle', methods=['GET', 'POST'])
def submit_test_cycle():
    pass


if __name__ == '__main__':
    app.run()