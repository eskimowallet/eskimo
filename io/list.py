from tools import db

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
	c.execute('select * from eskimo_currencies;')
	currencies = c.fetchall()
	db.close(conn)
	if not currencies:
		print('No currencies exist in the system')
		return False
	print('')
	for currency in currencies:
		print('{0: <5}'.format(str(currency[1])) + '   |   ' + '{0: >5}'.format(str(currency[2])))
	return True
	
def help():
	print('')
	print('eskimo - crypto-currency cold storage')
	print('')
	print('disclaimer - eskimo comes as is.')
	print('no promises are made as to the suitability or security of the addresses it generates.')
	print('it is up to you to ensure the continued security of your crypto-currencies.')
	print('no liability is assumed by eskimo or its creators.')
	print('')	
	print('== commands ==')
	print('')
	print('exit')
	print('  quit eskimo. (you can use ctrl+c too).')
	print('help')
	print('  show this dialogue.') 
	print('bip')
	print('  generate a BIP38 encrypted private key.')
	print('dumpprivkey')
	print('  enter an eskimo generated address when prompted to view the associated private key in WIF format.')
	print('dumpprivkeyraw')
	print('  enter an eskimo generated address when prompted to view the associated raw private key.')
	print('entropycheck')
	print('  check your platform for a strong source of entropy.')
	print('listaddr')
	print('  list the addresses which eskimo has generated for a given currency.')
	print('listcur')
	print('  list the currencies which have been added to the eskimo system.')
	print('addcur')
	print('  add a new crypto-currency to your eskimo system.')
	print('editcur')
	print('  edit an existing crypto-currency.')
	print('import')
	print('  import an alts.json currency data file to overwrite the currency data in your system.')
	print('export')
	print('  export your systems currency data to an alts.json file')
	print('')
	print('==============')
	return
	