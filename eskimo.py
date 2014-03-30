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
from encrypt import bip38
from encrypt import database
import os.path
from tools import dbCreate
from tools import alts
from tools import curData
import sys


#build the database if it doesn't exist
if not os.path.isfile('igloo.dat') and not os.path.isfile('iceblock'):
	dbCreate.buildDB()
	dbCreate.setPwd()
	#as this is likely a first run, scan for entropy
	#rand.platformCheck()

#decrypt database
else:
	database.decrypt()
	

try:
	
	while True:
		
		print('')
		command = raw_input('Enter command >> ').lower().strip().split()
		
		if command[0] == 'exit':
			database.encrypt()
			sys.exit()
		
		elif command[0] == 'help':
			list.help()
			continue
			
		elif command[0] == 'setpass':
			dbCreate.setPwd(2)
			continue
			
		elif command[0] == 'dumpprivkey':
			address.dumpPrivKey(command[1])
			continue
		
		elif command[0] == 'dumpprivkeyraw':
			address.dumpPrivKey(command[1], 1)
			continue		
		
		elif command[0] == 'entropycheck':
			rand.platformCheck()
			continue
		
		elif command[0] == 'listaddr':
			list.showAddresses(command[1])
			continue

		elif command[0] == 'listcur':
			list.showCurrencies()
			continue
		
		elif command[0] == 'addcur':
			alts.addAlt(command[1])
			continue
			
		elif command[0] == 'editcur':
			alts.editAlt(command[1])
			continue
			
		elif command[0] == 'import':
			curData.importAlts()
			continue
			
		elif command[0] == 'export':
			curData.exportAlts()
			continue
		
		elif command[0] == 'gen':
			 address.generate(command[1], command[2])
			 continue
		
		else:
			print('command not recognised')
			continue

except:
	database.encrypt()
	sys.exit() 
