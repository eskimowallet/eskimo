import sqlite3
from output import out

b58_digits = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def base58_to_hex(b58str):
  	n = 0
  	for s in b58str:
  		n *= 58
    		digit = b58_digits.index(s)
    		n += digit
  	return hex(n)
  	
def getPrivKey():
	cur = raw_input('Enter the currency abbreviation : ')
	conn = sqlite3.connect('eskimo.db')
	c = conn.cursor()
	c.execute('select id from eskimo_currencies where currency=?;', (cur,))
	if c.fetchone() is not None:
		out.prnt(cur + ' already exists in the system')
		conn.close()
		return
	longName = raw_input('Enter the full name of the currency : ')
	privK = raw_input('Enter a private key : ')
	hexK = base58_to_hex(privK)
	prefix = hexK[0:3]
	i = 3
	while int(prefix, 16) < 128:
		prefix += hexK[i]
		i += 1
	c.execute('select id from eskimo_versions where version=?;', ((int(prefix, 16)-128),))
	version = c.fetchone()
	if version is None:
		out.prnt('Version ' + str(int(prefix, 16)-128) + ' does not exist in the system\n\n')
	c.execute('insert into eskimo_currencies (currency, longName, version) values (?,?,?);', (cur, longName, version[0]))
	out.prnt(longName + ' is version ' + str(int(prefix, 16)-128) + '\n\n')
	conn.commit()
	conn.close()
	return

