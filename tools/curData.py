import sqlite3
import json
import os.path

def exportAlts():
	conn = sqlite3.connect('eskimo.db')
	c = conn.cursor()
	c.execute('select c.currency, c.longName, v.version from eskimo_currencies as c inner join eskimo_versions as v on c.version = v.id;')
	currencies = c.fetchall()
	conn.close()
	currs = []
	for cur in currencies:
		currs.append({'currency': str(cur[0]), 'longName': str(cur[1]), 'version': int(cur[2])}) 
	with open('alts.json', 'w') as outfile:
		json.dump(currs, outfile)
	print('exported all currency data')
	return True

def importAlts():
	if not os.path.isfile('alts.json'):
		print('no alts.json file in your eskimo directory')
		return False
	with open('alts.json', 'r') as dataFile:
		currencies = json.load(dataFile)
	conn = sqlite3.connect('eskimo.db')
	c = conn.cursor()
	c.execute('delete from eskimo_currencies;')
	inCount = 0
	outCount = 0
	for cur in currencies:
		inCount += 1
		c.execute('select id from eskimo_versions where version=?;', (cur['version'],))
		version = c.fetchone()
		if version is None:
			continue
		outCount += 1
		version = version[0] if version[0] < 145 else 145
		c.execute('insert into eskimo_currencies (currency, longName, version) values (?,?,?);', (cur['currency'], cur['longName'], version))
	conn.commit()
	conn.close()
	if not inCount == outCount:
		print('not all currencies were imported due to incompatible version numbers')
	else:
		print('import finished')
	return True