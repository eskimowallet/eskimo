#!/usr/bin/env python
"""
Eskimo

Cold storage crypto-currency address generator

"""

import os.path
import sys

import encrypt.bip38 as bip38
import encrypt.database as database
import io.inp as inp
import io.get as get
import io.list as list
import num.rand as rand
import system.address as address
import system.alts as alts
import system.curData as curData
import system.dbCreate as dbCreate
from system.settings import passW
passW = passW()

#build the database if it doesn't exist
if not os.path.isfile('igloo.dat') and not os.path.isfile('iceblock'):
    passW.setPass()
    dbCreate.buildDB()
	#as this is likely a first run, scan for good entropy
	#rand.platformCheck()	

else:
    if not os.path.isfile('igloo.dat') and os.path.isfile('iceblock'):
        #decrypt the database if the encrypted version exists
        database.decrypt(passW)
    else:
        #otherwise get the password so that password encryption can take place
        passW.getPass()
    
try:
	
    while True:
		
        print('')
        command = raw_input('Enter command >> ').lower().strip().split()

        if command[0] == 'exit':
            database.encrypt(passW)
            sys.exit()

        elif command[0] == 'help':
            list.help()
            continue
            
        elif command[0] == 'setpass':
            dbCreate.setPwd(2)
            continue
            
        elif command[0] == 'dumpprivkey':
            if len(command) < 2:
                print('dumpprivkey requires an address as its first parameter')
                continue
            address.dumpPrivKey(command[1])
            continue		

        elif command[0] == 'entropycheck':
            rand.platformCheck()
            continue

        elif command[0] == 'listaddr':
            if len(command) < 2:
                print('listaddr requires a currency abbreviation as its first parameter')
                continue
            list.showAddresses(command[1])
            continue

        elif command[0] == 'listcur':
            list.showCurrencies()
            continue

        elif command[0] == 'addcur':
            if len(command) < 2:
                print('addcur requires a currency abbreviation as its first parameter')
                continue
            alts.addAlt(command[1])
            continue
            
        elif command[0] == 'editcur':
            if len(command) < 2:
                print('editcur requires a currency abbreviation as its first parameter')
                continue
            alts.editAlt(command[1])
            continue
            
        elif command[0] == 'import':
            curData.importAlts()
            continue
            
        elif command[0] == 'export':
            curData.exportAlts()
            continue

        elif command[0] == 'gen':
            if len(command) < 2:
                print('gen requires a currency abbreviation as its first parameter')
                continue
            address.generate(command[1])
            continue

        else:
            print(command[0] + ' was not recognised as a command')
            continue

except KeyboardInterrupt:
    database.encrypt(passW)
    sys.exit()
