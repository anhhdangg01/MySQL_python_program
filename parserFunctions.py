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
	result = f'INSERT INTO viewers\nVALUES ({uid}, "{first}", "{last}", "{subscription}")'
	insertUserParser(db, uid, email, joined_date, nickname, street, city, state, zip, genres)
	#result = 'INSERT INTO Viewers\nVALUES ('
	#result += uid + ', "' + email + '", "' + nickname + '", "' + street + '", "' + city + '", "' + state + '", "' + zip + '", "' + genres + '", ' + joined_date + ', "' + first + '", "' + last + '", "' + subscription + '");'
	return result

def insertUserParser(db, uid, email, joined_date, nickname, street, city, state, zip, genres):
	result = f'INSERT INTO users\nVALUES ({uid}, "{email}", "{joined_date}", "{nickname}", "{street}", "{city}", "{state}", "{zip}", "{genres}");'
	helperFunctions.execute_boolean_query(db, result)
	
def deleteViewerParser(uid):
	return 'DELETE FROM Viewers V\nWHERE V.uid = ' + uid + ';'
	
	
def selectGenresParser(uid, db):
	cursor = db.cursor()
	cursor.execute('SELECT U.genres\nFROM Users U\nWHERE U.uid = ' + uid + ';')
	query = cursor.fetchone()
	cursor.close()
	return query[0]

def addGenreParser(uid, genre, old_genres):
	currGenres = old_genres + '; ' + genre
	return 'UPDATE Users\nSET genres = ' + currGenres + '\nWHERE uid = ' + uid + ';'
	
def insertMovieParser(rid, website_url):
	return 'INSERT INTO movies\nVALUES (' + rid + ', "' + website_url + '");'
	
def insertSessionParser(sid, uid, rid, ep_num, initiate_at, leave_at, quality, device):
	return 'INSERT INTO Sessions\nVALUES (' + sid + ', ' + uid + ', ' + rid + ', ' + ep_num + ', ' + initiate_at + ', '+  leave_at + ', ' + quality + ', ' + device + ');'
	
def updateReleaseParser(rid, title):
	return 'UPDATE Releases\nSET title = ' + title + '\nWHERE rid = ' + rid + ';'
	
def releasesReviewedParser(uid):
	return 'SELECT DISTINCT R.rid, R.genre, R.title\nFROM Releases R\nWHERE R.uid = ' + uid + \
	'ORDER BY title ASC;'
	
def popularReleaseParser(N):
	return 'SELECT R.rid, R.title, R.reviewCount\nFROM Releases\nORDER BY reviewCount DESC\nLIMIT ' + N + ';'

def releaseTitleParser(sid):
	return 'SELECT S.rid, S.release_title, S.genre, S.video_title, S.ep_num, S.length\n' + \
	'FROM Sessions S\nWHERE S.sid = ' + sid + ';'
	
def activeViewersParser(N, start, end):
	return 'SELECT V.uid, V.firstname, V.lastname\n' + \
	'FROM Viewers V\n' + \
	'WHERE V.uid in (SELECT V1.uid\nFROM Viewers V1\nWHERE V1.initiate_at >= ' + start + ' AND V1.leave_at <= ' + end + ');'


def viewedVideosParser(rid):
    return ('SELECT V.rid, V.ep_num, V.title, V.length, COALESCE(view_counts.view_count, 0) AS view_count\n'
            'FROM Videos V LEFT JOIN (SELECT S.rid, COUNT(DISTINCT S.uid) AS view_count FROM Sessions S WHERE S.rid = ' 
            + str(rid) + ' GROUP BY S.rid) view_counts ON V.rid = view_counts.rid WHERE V.rid = ' + str(rid) + ' ORDER BY V.rid DESC;')
