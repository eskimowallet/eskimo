import json
import os.path
import sqlite3
import system.db as db


def exportAlts():
	conn = db.open()
	c = conn.cursor()
	c.execute('select c.currency, c.longName, v.version from eskimo_currencies as c inner join eskimo_versions as v on c.version = v.id;')
	currencies = c.fetchall()
	db.close(conn)
	currs = []
	for cur in currencies:
		currs.append({'currency': str(cur[0]), 'longName': str(cur[1]), 'version': int(cur[2])}) 
	with open('currencies.json', 'w') as outfile:
		json.dump(currs, outfile)
	print('exported all currency data')
	return True

def importAlts():
	if not os.path.isfile('currencies.json'):
		print('no currencies.json file in your eskimo directory')
		return False
	with open('currencies.json', 'r') as dataFile:
		currencies = json.load(dataFile)
	conn = db.open()
	c = conn.cursor()
	for cur in currencies:
		version = cur['version'] if cur['version'] < 145 else 145
		c.execute('select id from eskimo_versions where version=?;', (version,))
		versionId = c.fetchone()
		if versionId is None:
			continue
		c.execute('select id from eskimo_currencies where currency=?;', (cur['currency'],))
		curId = c.fetchone()
		if curId is None:
			#currency doesn't exist in the system so add it
			c.execute('insert into eskimo_currencies (currency, longName, version) values (?,?,?);', (cur['currency'], cur['longName'], versionId[0]))
		else:
			c.execute('update eskimo_currencies set currency=?, longName=?, version=? where id=?;', (cur['currency'], cur['longName'], versionId[0], curId[0]))
	db.close(conn)
	print('import finished')
	return True