import os
import csv
import mysql.connector
import datetime

def execute_insert_boolean_query(db, query_string):
	try:
		cursor = db.cursor()
		cursor.execute(query_string)
		cursor.close()
		print("Success")
	except mysql.connector.IntegrityError as e:
		print("Fail")


def execute_delete_boolean_query(db, query_string):
	try:
		cursor = db.cursor()
		cursor.execute(query_string)
		if cursor.rowcount == 0:
			print("Fail")
			return
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
	table_names = ["users", "producers", "viewers", "releases", "movies", "series", "videos", "sessions", "reviews"]
	create_tables(db)
	#for file in os.listdir(fpath):
	for table_name in table_names:
		file_path = f"{fpath}/{table_name}.csv"
		if os.path.isfile(file_path):
			with open(file_path, newline="", encoding="utf-8") as input_file:
				reader = csv.reader(input_file)
				# get the first row of the csv file holding the names
				attribute_names = next(reader)
				# get the first row of data to determine the types
				first_data_row = next(reader)
				all_data_rows = [first_data_row] + list(reader)
				
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


def create_tables(db):
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
	"""
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
	"""
	#ENUM('free', 'monthly', 'yearly') this was in viewers for subscription replaced with TEXT
	users_query = f"CREATE TABLE users (uid INT, email TEXT NOT NULL, joined_date DATE NOT NULL, nickname TEXT NOT NULL, street TEXT, city TEXT, state TEXT, zip TEXT, genres TEXT, PRIMARY KEY (uid));"
	producers_query = f"CREATE TABLE producers (uid INT, bio TEXT, company TEXT, PRIMARY KEY (uid), FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE);"
	viewers_query = f"CREATE TABLE viewers (uid INT, subscription TEXT, first_name TEXT NOT NULL, last_name TEXT NOT NULL, PRIMARY KEY (uid), FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE);"
	releases_query = f"CREATE TABLE releases (rid INT, producer_uid INT NOT NULL, title TEXT NOT NULL, genre TEXT NOT NULL, release_date DATE NOT NULL, PRIMARY KEY (rid),FOREIGN KEY (producer_uid) REFERENCES producers(uid) ON DELETE CASCADE);"
	movies_query = f"CREATE TABLE movies (rid INT, website_url TEXT, PRIMARY KEY (rid), FOREIGN KEY (rid) REFERENCES releases(rid) ON DELETE CASCADE);"
	series_query = f"CREATE TABLE series (rid INT, introduction TEXT, PRIMARY KEY (rid), FOREIGN KEY (rid) REFERENCES releases(rid) ON DELETE CASCADE);"
	videos_query = f"CREATE TABLE videos (rid INT, ep_num INT NOT NULL, title TEXT NOT NULL, length INT NOT NULL, PRIMARY KEY (rid, ep_num), FOREIGN KEY (rid) REFERENCES releases(rid) ON DELETE CASCADE);"
	sessions_query = f"CREATE TABLE sessions (sid INT, uid INT NOT NULL, rid INT NOT NULL, ep_num INT NOT NULL, initiate_at DATETIME NOT NULL, leave_at DATETIME NOT NULL, quality ENUM('480p', '720p', '1080p'), device ENUM('mobile', 'desktop'), PRIMARY KEY (sid), FOREIGN KEY (uid) REFERENCES viewers(uid) ON DELETE CASCADE, FOREIGN KEY (rid, ep_num) REFERENCES videos(rid, ep_num) ON DELETE CASCADE);"
	reviews_query = f"CREATE TABLE reviews (rvid INT, uid INT NOT NULL, rid INT NOT NULL, rating DECIMAL(2, 1) NOT NULL CHECK (rating BETWEEN 0 AND 5), body TEXT, posted_at DATETIME NOT NULL, PRIMARY KEY (rvid), FOREIGN KEY (uid) REFERENCES viewers(uid) ON DELETE CASCADE, FOREIGN KEY (rid) REFERENCES releases(rid) ON DELETE CASCADE);"
	cursor.execute(users_query)
	cursor.execute(producers_query)
	cursor.execute(viewers_query)
	cursor.execute(releases_query)
	cursor.execute(movies_query)
	cursor.execute(series_query)
	cursor.execute(videos_query)
	cursor.execute(sessions_query)
	cursor.execute(reviews_query)
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
	
	cursor.execute("DROP TABLE IF EXISTS reviews")
	cursor.execute("DROP TABLE IF EXISTS sessions")
	cursor.execute("DROP TABLE IF EXISTS videos")
	cursor.execute("DROP TABLE IF EXISTS series")
	cursor.execute("DROP TABLE IF EXISTS movies")
	cursor.execute("DROP TABLE IF EXISTS releases")
	cursor.execute("DROP TABLE IF EXISTS viewers")
	cursor.execute("DROP TABLE IF EXISTS producers")
	cursor.execute("DROP TABLE IF EXISTS users")
	
	"""
	# get all the table names
	cursor.execute("SHOW TABLES")
	# store results in list of tuples
	tables = cursor.fetchall()

	cursor.execute("SET FOREIGN_KEY_CHECKS=0")
	# loop through all table names and delete them
	for (table, ) in tables:
		query = f"DROP TABLE IF EXISTS {table}"
		cursor.execute(query)
	"""
	# close the cursor
	cursor.close()