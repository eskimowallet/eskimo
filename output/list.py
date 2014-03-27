import sqlite3

def showAddresses():
	cur = raw_input('\nEnter a currency abbreviation :')
	conn = sqlite3.connect('eskimo.db')
	c = conn.cursor()
	c.execute('select a.address from eskimo_addresses as a inner join eskimo_currencies as c on a.currency = c.id where c.currency = ?;', (cur.upper(),))
	addresses = c.fetchall()
	conn.close()
	if not addresses:
		print('No addresses found for ' + cur.upper())
		return False
	print('')
	for address in addresses:
		print(str(address[0]).decode('base64', 'strict'))
	return True
	
def showCurrencies():
	conn = sqlite3.connect('eskimo.db')
	c = conn.cursor()
	c.execute('select * from eskimo_currencies;')
	currencies = c.fetchall()
	conn.close()
	if not currencies:
		print('No currencies exist in the system')
		return False
	print('')
	for currency in currencies:
		print(str(currency[1]) + '   |   ' + str(currency[2]) + '   |   ' + str(currency[3]))
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
	print('exit - quit eskimo.')
	print('(you can use ctrl+c too).')
	print('')
	print('help - show this dialogue.')
	print('')
	print('scanprivkey - add a new crypto-currency to your eskimo system.') 
	print('eskimo can only generate addresses and private keys for currencies which exist in the system.')
	print('')
	print('dumpprivkey - enter an eskimo generated address when prompted to view the associated private key.')
	print('')
	print('entropycheck - check your platform for a strong source of entropy.')
	print('this is important for generating random keys and secure addresses.')
	print('')
	print('listcur - list the currencies which have been added to the eskimo system.')
	print('')
	print('listadd - list the addresses which eskimo has generated for a given currency.')
	print('')
	print('==============')
	print('')
	return
	