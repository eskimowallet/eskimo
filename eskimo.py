#!/usr/bin/env python
"""
Eskimo

Cold storage crypto-currency address generator

"""

from rand import rand
from input import inp
from input import get
from output import out
from encrypt import address
import os.path
from tools import dbCreate
from tools import alts
import sys


#build the database if it doesn't exist
if not os.path.isfile('eskimo.db'):
	dbCreate.buildDB()


try:
	
	out.prnt('Enter a currency abbreviation to generate an address\n')
	out.prnt('or enter a command for a different function\n')
	out.prnt('("help" lists available functions)\n')
	
	while True:
		
		command = raw_input('Enter command : ')
		
		if command.lower() == 'exit':
			sys.exit()
		
		if command.lower() == 'help':
			out.prnt('show help\n')
			continue
		
		elif command.lower() == 'importprivkey':
			alts.getPrivKey()
			continue
			
		elif command.lower() == 'dumpprivkey':
			address.dumpPrivKey()
			continue
			
		elif command.lower() == 'entropycheck':
			rand.platformCheck()
			continue

		elif command.lower() == 'currencycheck':
			out.prnt('display available currencyies\n')
			continue
		
		elif command.lower() == 'showaddresses':
			out.prnt('ask for currency then show addresses\n')
			continue
			
		else:
			address.generate(command)
			continue

except KeyboardInterrupt:
	sys.exit() 
