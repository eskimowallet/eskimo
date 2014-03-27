import sqlite3

def base58_to_hex(b58str):
  	n = 0
	b58_digits = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
  	for s in b58str:
  		n *= 58
    		digit = b58_digits.index(s)
    		n += digit
  	return hex(n)
  	
def scanPrivKey():
	cur = raw_input('Enter the currency abbreviation : ').upper()
	conn = sqlite3.connect('eskimo.db')
	c = conn.cursor()
	c.execute('select id from eskimo_currencies where currency=?;', (cur,))
	if c.fetchone() is not None:
		print(cur + ' already exists in the system')
		conn.close()
		return
	longName = raw_input('Enter the full name of the currency : ').capitalize()
	privK = raw_input('Enter a private key : ')
	if privK == '':
		print('No private key entered')
		return
	hexK = base58_to_hex(privK)
	prefix = hexK[0:3]
	i = 3
	while int(prefix, 16) < 128:
		prefix += hexK[i]
		i += 1
	#all version from 145-255 have the same prefix etc.
	#we only store up to 145 in the database
	versionInt = (int(prefix, 16)-128) if (int(prefix, 16)-128) < 145 else 145
	c.execute('select id from eskimo_versions where version=?;', (versionInt,))
	version = c.fetchone()
	if version is None:
		print('Version ' + str(int(prefix, 16)-128) + ' does not exist in the system')
	c.execute('insert into eskimo_currencies (currency, longName, version) values (?,?,?);', (cur, longName, version[0]))
	print(longName + ' is version ' + str(int(prefix, 16)-128))
	conn.commit()
	conn.close()
	return

