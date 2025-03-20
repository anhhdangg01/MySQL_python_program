import sys
import parserFunctions
import helperFunctions
import mysql.connector


def command_parser(db):
    """
    Parses the command retrieved from the command line.
    
    """
    command_input = sys.argv[1:]
    query = ""
    
    # Run this if you want to see all tables and rows
    # in db prior to a command
    """
    print("Pre")
    cursor = db.cursor()
    print(f"Table: viewers")
    query = f"SELECT * FROM viewers"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()
    """

    if command_input[0] == "import":
        parserFunctions.importParser(command_input[1], db)
    elif command_input[0] == "insertViewer":        
        parserFunctions.insertViewerParser(db, command_input[1], command_input[2], command_input[3], command_input[4],
                                           command_input[5], command_input[6], command_input[7], command_input[8],
                                           command_input[9], command_input[10], command_input[11], command_input[12])
        #helperFunctions.execute_boolean_query(db, query)
    elif command_input[0] == "addGenre":
        old_genre = parserFunctions.selectGenresParser(command_input[1], db)
        query = parserFunctions.addGenreParser(command_input[1], command_input[2], old_genre)
        helperFunctions.execute_boolean_query(db, query)
    elif command_input[0] == "deleteViewer":
        query = parserFunctions.deleteViewerParser(command_input[1])
        helperFunctions.execute_boolean_query(db, query)
    elif command_input[0] == "insertMovie":
        query = parserFunctions.insertMovieParser(command_input[1], command_input[2])
        helperFunctions.execute_boolean_query(db, query)
    elif command_input[0] == "insertSession":
        query = parserFunctions.insertSessionParser(command_input[1], command_input[2], command_input[3], command_input[4],
                                            command_input[5], command_input[6], command_input[7], command_input[8])
        helperFunctions.execute_boolean_query(db, query)
    elif command_input[0] == "updateRelease":
        query = parserFunctions.updateReleaseParser(command_input[1], command_input[2])
        helperFunctions.execute_boolean_query(db, query)
    elif command_input[0] == "listReleases":
        query = parserFunctions.releasesReviewedParser(command_input[1])
        helperFunctions.execute_record_query(db, query)
    elif command_input[0] == "popularRelease":
        query = parserFunctions.popularReleaseParser(command_input[1])
        helperFunctions.execute_record_query(db, query)
    elif command_input[0] == "releaseTitle":
        query = parserFunctions.releaseTitleParser(command_input[1])
        helperFunctions.execute_record_query(db, query)
    elif command_input[0] == "activeViewer":
        query = parserFunctions.activeViewersParser(command_input[1], command_input[2], command_input[3])
        helperFunctions.execute_record_query(db, query)
    elif command_input[0] == "videosViewed":
        query = parserFunctions.viewedVideosParser(command_input[1])
        helperFunctions.execute_record_query(db, query)

    # Run this if you want to see all tables and rows
    # in db
    """
    cursor = db.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    for (table, ) in tables:
        print(f"Table: {table}")
        query = f"SELECT * FROM {table}"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        print()
        print()
    cursor.close()
    """
    """
    print("Post")
    cursor = db.cursor()
    print(f"Table: viewers")
    query = f"SELECT * FROM viewers"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()
    """


def make_db_connection():
    """
    Description: 
     - Creates a connection between the program and the mysql database
    Return:
     - db: a mysql.connector object that represents a connection
           between the program and mysql database
    """
    # creating connection
    db = mysql.connector.connect(
        #host="localhost",
        user="test",
        password="password",
        database="cs122a"
    )
    return db

def close_db_connection(db):
    """
    Description:
     - Closes the database connection
    
    Args:
     - db: mysql.connector object to close
    
    Return:
     - None
    """

    db.close()

if __name__ == '__main__':
    db = make_db_connection()
    command_parser(db)
    # commit the changes to the database
    db.commit()
    close_db_connection(db)
