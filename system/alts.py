import sqlite3

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
	if cur == '':
		print('a currency abbreviation is required')
		return False
	conn = sqlite3.connect('igloo.dat')
	c = conn.cursor()
	c.execute('select id from eskimo_currencies where currency=?;', (cur.upper(),))
	if c.fetchone() is not None:
		print(cur.upper() + ' already exists in the system')
		conn.close()
		return
	longName = raw_input('Enter the full name of the currency : ').capitalize().strip()
	if longName == '':
		print('currencies need a full name')
		return False
	privK = raw_input('Enter a private key : ').strip()
	if privK == '':
		print('No private key entered')
		return False
	#alow for direct entry of version number
	if len(privK) > 3:
		version = scanPrivKey(privK)
	else:
		version = privK
	#all version from 145-255 have the same prefix etc.
	#we only store up to 145 in the database
	versionInt = version if version < 145 else 145
	c.execute('select id from eskimo_versions where version=?;', (versionInt,))
	version = c.fetchone()
	if version is None:
		print('Version ' + str(version[0]) + ' does not exist in the system')
	c.execute('insert into eskimo_currencies (currency, longName, version) values (?,?,?);', (cur.upper(), longName, version[0]))
	print(longName + ' is version ' + str(version[0]))
	conn.commit()
	conn.close()
	return
	
def editAlt(cur):
	if cur == '':
		return False
	conn = sqlite3.connect('igloo.dat')
	c = conn.cursor()
	c.execute('select id,currency,longName,version from eskimo_currencies where currency=?;', (cur.upper(), ))
	curId = c.fetchone()
	if curId is None:
		print(cur.upper() + ' doesn\'t exist in the system')
		return False
	newCur = raw_input('Enter the new currency abbreviation (' + curId[1] + ') : ').upper().strip()
	newCur = curId[1] if newCur == '' else newCur
	newLongName = raw_input('Enter the new full name (' + curId[2] + ') : ').capitalize().strip()
	newLongName = curId[2] if newLongName == '' else newLongName
	imp = raw_input('Would you like to scan a different private key? ').lower().strip()
	if not imp == 'y':
		newVersion = curId[3]
	else:
		privK = raw_input('Enter a private key : ').strip()
		if privK =='':
			newVersion = curId[3]
		if len(privK) > 3:
			version = scanPrivKey(privK)
		else:
			version = privK
		print(str(version))
		versionInt = version if version < 145 else 145
		c.execute('select id from eskimo_versions where version=?;', (versionInt,))
		versionDb = c.fetchone()
		if versionDb is None:
			print('Version ' + str(version) + ' does not exist in the system')
			newVersion = curId[3]
		else:
			newVersion = versionDb[0]
	c.execute('update eskimo_currencies set currency=?, longName=?, version=? where id=?;', (newCur, newLongName, newVersion, curId[0]))
	conn.commit()
	conn.close()
	print(newCur + ' saved')
	return True
