def insertViewerParser(uid, email, nickname, street, city, state, zip, genres, joined_date, first, last, subscription):
	result = 'INSERT INTO Viewers\nVALUES ('
	result += uid + ', ' + email + ', ' + nickname + ', ' + street + ', ' + city + ', ' + state + ', ' + zip + ', ' + genres + ', ' + joined_date + ', ' + first + ', ' + last + ', ' + subscription + ');'
	return result;
	
def deleteViewerParser(uid):
	return 'DELETE FROM Viewers V\nWHERE V.uid = ' + uid + ';'
	
	
def selectGenresParser(uid):
	return 'SELECT U.genres\nFROM Users U\nWHERE U.uid = ' + uid + ';'
	 
def addGenreParser(uid, genre):
	currGenres = ''
	#currGenres = selectGenres(selectGenresParser)
	newGenres = currGenres + '; ' + genre #FIX THIS!!!!
	return 'UPDATE Users\nSET genres = ' + newGenres + '\nWHERE uid = ' + uid + ';'
	
def insertMovieParser(rid, website_url):
	return 'INSERT INTO Movies\nValues (' + rid + ', ' + website_url + ');'
	
def insertSessionParser(sid, uid, rid, ep_num, initiate_at, leave_at, quality, device):
	return 'INSERT INTO Sessions\nVALUES (' + sid + ', ' uid + ', ' rid + ', ' ep_num + ', ' initiate_at + ', ' leave_at + ', ' quality + ', ' device + ');'
	
def updateReleaseParser(rid, title):
	return 'UPDATE Releases\nSET title = ' + title + '\nWHERE rid = ' + rid + ';'
	
def releasesReviewedParser(uid):
	return 'SELECT DISTINCT R.rid, R.genre, R.title\nFROM Releases R\nWHERE R.uid = ' + uid + \
	'ORDER BY title ASC;'
	
def popularReleaseParser():
	return 'SELECT R.rid, R.titel, R.reviewCount\nFROM Releases\nORDER BY reviewCount DESC\nLIMIT ' + N + ';'
