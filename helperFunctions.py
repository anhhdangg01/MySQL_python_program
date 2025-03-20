import os
import csv
import mysql.connector
import datetime

def execute_boolean_query(db, query_string):
	try:
		cursor = db.cursor()
		#print(f" DEBUG: {query_string}")
		cursor.execute(query_string)
		cursor.close()
		print("Success")
	except mysql.connector.IntegrityError as e:
		print("Fail")


def execute_record_query(db, query_string):
	"""
	Executes the given query and outputs each record in one line and separates columns using csv.

	"""
	try:
		cursor = db.cursor()
		cursor.execute(query_string)
		query = cursor.fetchall()
		cursor.close()
		
		# record_output = ""
		# for record in range(len(query) - 1):
		# 	record_output += str(query[record]) + ","
		# record_output += str(query[len(query) - 1])
		# print(record_output)
		for record in query:
			record_output = ""
			for attribute in range(len(record) - 1):
				record_output += str(record[attribute]) + ","
			record_output += str(record[len(record) - 1])
			print(record_output)

	except mysql.connector.IntegrityError as e:
		return


def get_data_type(data):
	"""
    Description:
     - Determines what integrity contraint should be
	   put on the data given to the function
    
    Args:
     - data: value to be tested
    
    Return:
     - None
    """
	try:
		# check if it is int
		int(data)
		return "INT"
	except ValueError:
		pass
	try:
		# check if it is date
		datetime.datetime.strptime(data, "%Y-%m-%d")
		return "DATE"
	except ValueError:
		pass
	try:
		# check if it is datetime
		datetime.datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
		return "DATETIME"
	except ValueError:
		pass
	# must be text
	return "TEXT"


def import_files(fpath, db):
	"""
    Description:
     - Imports all the csv files into the database
    
    Args:
     - fpath: path to the folder containing the csv
	   files
     - db: mysql.connector object
    
    Return:
     - None
    """
	for file in os.listdir(fpath):
		if file.endswith(".csv"):
			# split the file name and extension and keep name
			table_name = os.path.splitext(file)[0]
			file_path = os.path.join(fpath, file)
			
			with open(file_path, newline="", encoding="utf-8") as input_file:
				reader = csv.reader(input_file)
				# get the first row of the csv file holding the names
				attribute_names = next(reader)
				# get the first row of data to determine the types
				first_data_row = next(reader)
				all_data_rows = [first_data_row] + list(reader)
				
            # create table
			create_table(db, table_name, attribute_names, first_data_row)
			# insert data into the tables
			insert_values(db, table_name, all_data_rows)


def insert_values(db, table_name, rows):
	"""
    Description:
     - Inserts all the rows into the given table
    
    Args:
     - db: mysql.connector object
	 - table_name: name of the table to create
	 - rows: list of tuples containing the rows
	   to insert into the table
    
    Return:
     - None
    """
	cursor = db.cursor()
	values = ", ".join(["%s"] * len(rows[0]))
	query = f"INSERT INTO {table_name} VALUES ({values})"
	# using batch insertion
	cursor.executemany(query, rows)
	cursor.close()


def create_table(db, table_name, attribute_names, first_data_row):
	"""
    Description:
     - Creates a table given the name, db connection,
	   and attribute names
    
    Args:
     - db: mysql.connector object
	 - table_name: name of the table to create
	 - attribute_names: names of the attributes for
	   the table
	 - first_data_row: has the first row to input into
	   the table
    
    Return:
     - None
    """
	cursor = db.cursor()
	attributes = []
	for i, attribute in enumerate(attribute_names):
		# get the data type
		att_type = get_data_type(first_data_row[i])
		# add the name and type to list of attributes
		attributes.append(f"{attribute} {att_type}")

	attributes = ", ".join(attributes)
	table_create_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({attributes})"
	# create the table
	cursor.execute(table_create_query)
	cursor.close()


def delete_db_tables(db):
	"""
    Description:
     - Deletes all tables in the database
    
    Args:
     - db: mysql.connector object 
    
    Return:
     - None
    """
	cursor = db.cursor()

	# get all the table names
	cursor.execute("SHOW TABLES")
	# store results in list of tuples
	tables = cursor.fetchall()

	# loop through all table names and delete them
	for (table, ) in tables:
		query = f"DROP TABLE {table}"
		cursor.execute(query)
	
	# close the cursor
	cursor.close()