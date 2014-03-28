#!/usr/bin/env python
"""
Eskimo

Cold storage crypto-currency address generator

"""

from rand import rand
from input import inp
from input import get
from output import list
from encrypt import address
import os.path
from tools import dbCreate
from tools import alts
import sys


#build the database if it doesn't exist
if not os.path.isfile('eskimo.db'):
	dbCreate.buildDB()
	#as this is likely a first run, scan for entropy
	rand.platformCheck()


try:
	
	print('Enter a currency abbreviation to generate an address')
	print('or enter a command for a different function')
	print('("help" lists available functions)')
	
	while True:
		
		print('')
		command = raw_input('Enter command : ').lower().strip()
		
		if command == 'exit':
			sys.exit()
		
		if command == 'help':
			list.help()
			continue
			
		elif command == 'dumpprivkey':
			address.dumpPrivKey()
			continue
			
		elif command == 'entropycheck':
			rand.platformCheck()
			continue

		elif command == 'listcur':
			list.showCurrencies()
			continue
		
		elif command == 'addcur':
			alts.scanPrivKey()
			continue
		
		elif command == 'listaddr':
			list.showAddresses()
			continue
			
		else:
			address.generate(command)
			continue

except KeyboardInterrupt:
	sys.exit() 
