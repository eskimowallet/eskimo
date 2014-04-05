import sqlite3
import system.db as db

def base58_to_hex(b58str):
	n = 0
	b58_digits = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
	for s in b58str:
		n *= 58
		digit = b58_digits.index(s)
		n += digit
	return hex(n)
  	
def scanPrivKey(privK):
	hexK = base58_to_hex(privK)
	prefix = hexK[0:3]
	i = 3
	while int(prefix, 16) < 128:
		prefix += hexK[i]
		i += 1
	return int(prefix, 16)-128
  	
def addAlt(cur):
	conn = db.open()
	c = conn.cursor()
	c.execute('select id from eskimo_currencies where currency=?;', (cur.upper(),))
	if c.fetchone() is not None:
		print(cur.upper() + ' already exists in the system')
		db.close(conn)
		return
	longName = raw_input('Enter the full name of the currency : ').capitalize().strip()
	if longName == '':
		print('Currencies need a full name')
		db.close(conn)
		return False
	privK = raw_input('Enter a private key : ').strip()
	if privK == '':
		print('No private key entered')
		db.close(conn)
		return False
	#allow for direct entry of version number
	if len(str(privK)) > 3:
		version = scanPrivKey(privK)
	else:
		version = int(privK)
	#all version from 145-255 have the same prefix etc.
	#we only store up to 145 in the database
	versionInt = version if version < 145 else 145
	c.execute('select id from eskimo_versions where version=?;', (versionInt,))
	versionId = c.fetchone()
	if versionId is None:
		print('Version ' + str(versionId[0]) + ' does not exist in the system')
		db.close(conn)
		return
	c.execute('insert into eskimo_currencies (currency, longName, version) values (?,?,?);', (cur.upper(), longName, versionId[0]))
	print(longName + ' is version ' + str(version))
	db.close(conn)
	return
	
def editAlt(cur):
	conn = db.open()
	c = conn.cursor()
	c.execute('select c.id,c.currency,c.longName,v.version from eskimo_currencies as c inner join eskimo_versions as v on c.version = v.id where c.currency=?;', (cur.upper(), ))
	curId = c.fetchone()
	if curId is None:
		print(cur.upper() + ' doesn\'t exist in the system')
		db.close(conn)
		return False
	newCur = raw_input('Enter the new currency abbreviation (' + curId[1] + ') : ').upper().strip()
	newCur = curId[1] if newCur == '' else newCur
	newLongName = raw_input('Enter the new full name (' + curId[2] + ') : ').capitalize().strip()
	newLongName = curId[2] if newLongName == '' else newLongName
	privK = raw_input('Enter a private key (' + str(curId[3]) + ') : ').strip()
	if privK =='':
		version = curId[3]
	elif len(privK) > 3:
		version = scanPrivKey(privK)
	else:
		version = int(privK)
	versionInt = version if version < 145 else 145
	c.execute('select id from eskimo_versions where version=?;', (versionInt,))
	versionDb = c.fetchone()
	if versionDb is None:
		print('Version ' + str(version) + ' does not exist in the system')
		return False
	else:
		newVersion = versionDb[0]
	c.execute('update eskimo_currencies set currency=?, longName=?, version=? where id=?;', (newCur, newLongName, newVersion, curId[0]))
	db.close(conn)
	print(newCur + ' saved')
	return True
