import system.db as db

def showAddresses(cur):
	conn = db.open()
	c = conn.cursor()
	c.execute('select a.address from eskimo_addresses as a inner join eskimo_currencies as c on a.currency = c.id where c.currency = ?;', (cur.upper(),))
	addresses = c.fetchall()
	db.close(conn)
	if not addresses:
		print('No addresses found for ' + cur.upper())
		return False
	print('')
	for address in addresses:
		print(str(address[0]).decode('base64', 'strict'))
	return True
	
def showCurrencies():
	conn = db.open()
	c = conn.cursor()
	c.execute('select c.currency,c.longName,v.version from eskimo_currencies as c inner join eskimo_versions as v on c.version=v.id;')
	currencies = c.fetchall()
	db.close(conn)
	if not currencies:
		print('No currencies exist in the system')
		return False
	print('')
	for currency in currencies:
		print('{0: ^8}'.format(str(currency[0])) + '   |   ' + '{0: ^16}'.format(str(currency[1])) + '   |   ' + '{0:>4}'.format(str(currency[2])))
	return True
	
def help():
	print('')
	print('eskimo - crypto-currency cold storage')
	print('')
	print('DISCLAIMER')
	print('##########')
	print('eskimo comes as is.')
	print('No promises are made as to the suitability or security of the addresses it generates.')
	print('It is up to you to ensure the continued security of your crypto-currencies.')
	print('No liability is assumed by eskimo or its creators.')
	print('')	
	print('== commands ==')
	print('')
	print('exit')
	print('  Quit eskimo. (you can use ctrl+c too).')
	print('help')
	print('  Show this dialogue.') 
	print('gen <cur>')
	print('  Generate an address/private key pair for the supplied currency abbreviation.')
	print('  BIP38 encryption is an option.')
	print('dumpprivkey <address>')
	print('  View the private key for the given eskimo generated address.')
	print('listaddr <cur>')
	print('  list the addresses which eskimo has generated for the given currency abbreviation.')
	print('listcur')
	print('  List the currencies available in the eskimo system.')
	print('addcur')
	print('  Add a new crypto-currency to your eskimo system.')
	print('editcur')
	print('  Edit an existing crypto-currency.')
	print('exportcur')
	print('  Export your systems currency data to a currencies.json file')
	print('importcur')
	print('  Import a currencies.json currency data file into your system.')
	print('entropycheck')
	print('  Check your platform for a strong source of time based entropy.')
	print('setpass')
	print('  Set a new database encryption password.')
	print('')
	print('==============')
	return
	
