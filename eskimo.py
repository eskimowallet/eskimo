#!/usr/bin/env python
"""
Eskimo

Cold storage crypto-currency address generator

"""

import rand.rand as rand
import input.inp as inp
import input.get as get
import output.list as list
import encrypt.address as address
import encrypt.bip38 as bip38
import encrypt.database as database
import os.path
import tools.dbCreate as dbCreate
import tools.alts as alts
import tools.curData as curData
import sys
from settings.settings import passW
passW = passW()

#build the database if it doesn't exist
if not os.path.isfile('igloo.dat') and not os.path.isfile('iceblock'):
    passW.setPass()
    dbCreate.buildDB()
	#as this is likely a first run, scan for good entropy
	#rand.platformCheck()	

else:
    if not os.path.isfile('igloo.dat') and os.path.isfile('iceblock'):
        while not database.decrypt(passW.getPass()):
            database.decrypt(passW.getPass())
    
try:
	
    while True:
		
        print('')
        command = raw_input('Enter command >> ').lower().strip().split()

        if command[0] == 'exit':
            while not database.encrypt(passW.password):
                database.encrypt(passW.password)
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

except KeyboardInterrupt:
    while not database.encrypt(passW.password):
                database.encrypt(passW.password)
    sys.exit() 
