import helperFunctions
import mysql.connector

# have to change the params for this to include the db object
# I will also continue to test this function -Chris
def importParser(folderName, db):
	try:
		helperFunctions.delete_db_tables(db)
		helperFunctions.import_files(folderName, db)
		print("Success")
	except mysql.connector.IntegrityError as e:
		print("Fail")


def insertViewerParser(db, uid, email, nickname, street, city, state, zip, genres, joined_date, first, last, subscription):
	try:
		cursor = db.cursor()
		result = f'INSERT INTO users\nVALUES ({uid}, "{email}", "{joined_date}", "{nickname}", "{street}", "{city}", "{state}", "{zip}", "{genres}");'
		cursor.execute(result)
		result = f"INSERT INTO viewers\nVALUES ({uid}, '{first}', '{last}', '{subscription}');"
		cursor.execute(result)
		cursor.close()
		print("Success")
	except mysql.connector.IntegrityError as e:
		print("Fail")
	#result = 'INSERT INTO Viewers\nVALUES ('
	#result += uid + ', "' + email + '", "' + nickname + '", "' + street + '", "' + city + '", "' + state + '", "' + zip + '", "' + genres + '", ' + joined_date + ', "' + first + '", "' + last + '", "' + subscription + '");'
	#return result
"""
def insertUserParser(db, uid, email, joined_date, nickname, street, city, state, zip, genres):
	try:
		cursor = db.cursor()
		result = f'INSERT INTO users\nVALUES ({uid}, "{email}", "{joined_date}", "{nickname}", "{street}", "{city}", "{state}", "{zip}", "{genres}");'
		cursor.execute(result)
		cursor.close()
	except mysql.connector.IntegrityError as e:
		return False
"""
def deleteViewerParser(uid):
	return 'DELETE FROM viewers V\nWHERE V.uid = ' + uid + ';'
	

def selectGenresParser(uid, db):
	cursor = db.cursor()
	cursor.execute('SELECT genres\nFROM users\nWHERE uid = ' + uid + ';')
	query = cursor.fetchone()
	cursor.close()
	return query[0]


def addGenreParser(uid, genre, old_genres):
	currGenres = old_genres + ';' + genre
	return 'UPDATE users\nSET genres = "' + currGenres + '"\nWHERE uid = ' + uid + ';'
	
	
def insertMovieParser(rid, website_url):
	return 'INSERT INTO movies\nVALUES (' + rid + ', "' + website_url + '");'
	

def insertSessionParser(sid, uid, rid, ep_num, initiate_at, leave_at, quality, device):
	return 'INSERT INTO sessions\nVALUES (' + sid + ', ' + uid + ', ' + rid + ', ' + ep_num + ', "' + initiate_at + '", "'+  leave_at + '", "' + quality + '", "' + device + '");'
	

def updateReleaseParser(rid, title):
	return 'UPDATE releases\nSET title = "' + title + '"\nWHERE rid = ' + rid + ';'
	

def releasesReviewedParser(uid):
	return 'SELECT DISTINCT Rel.rid, Rel.genre, Rel.title\n' + \
	'FROM releases Rel, reviews Rev\n' + \
	'WHERE Rel.rid = Rev.rid AND Rev.uid = ' + uid + "\n" + \
	'ORDER BY Rel.title ASC;'


def popularReleaseParser(N):
    return 'SELECT Rel.rid, Rel.title, COUNT(Rev.rid) AS reviewCount\n' \
            'FROM releases Rel\n' \
            'LEFT JOIN reviews Rev ON Rel.rid = Rev.rid\n' \
            'GROUP BY Rel.rid, Rel.title\n' \
            'ORDER BY reviewCount DESC, Rel.rid DESC\n' \
            'LIMIT ' + N + ';'
    
	
    

def releaseTitleParser(sid):
	return 'SELECT S.sid, R.title, R.genre, V.title, V.ep_num, V.length\n' \
	'FROM sessions S, releases R, videos V\n' \
	'WHERE S.sid = ' + sid + ' AND S.rid = R.rid AND R.rid = V.rid\n' \
	'ORDER BY R.title ASC;'
	

def activeViewersParser(N, start, end):
    return f'''
    SELECT V.uid, V.first_name, V.last_name
    FROM viewers V
    WHERE V.uid IN (
        SELECT S.uid
        FROM sessions S
        WHERE S.initiate_at BETWEEN '{start}' AND '{end}'
        GROUP BY S.uid
        HAVING COUNT(S.sid) >= {N}
    )
    ORDER BY V.uid ASC;
    '''

def viewedVideosParser(rid):
    return ('SELECT V.rid, V.ep_num, V.title, V.length, COALESCE(view_counts.view_count, 0) AS view_count\n'
            'FROM videos V LEFT JOIN (SELECT S.rid, COUNT(DISTINCT S.uid) AS view_count FROM sessions S WHERE S.rid = ' 
            + str(rid) + ' GROUP BY S.rid) view_counts ON V.rid = view_counts.rid WHERE V.rid = ' + str(rid) + ' ORDER BY V.rid DESC;')
