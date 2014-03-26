#!/usr/bin/env python
"""
Eskimo

Cold storage crypto-currency address generator

This code, excepting the MIT-licensed libraries,
is public domain. Everyone has the right to do whatever they want
with it for any purpose.

Also MIT licensed, when needed for redistribution:

The MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from rand import rand
from input import inp
from input import get
from output import out
from encrypt import address
import os.path
from tools import dbCreate
from tools import alts




def generate():
	
	#build the database if it doesn't exist
	if not os.path.isfile('eskimo.db'):
		dbCreate.buildDB()
		
	alts.getPrivKey()
		
	
	rand.platformCheck()

	privateKey = rand.randomKey(inp.keyboardEntropy())
	wifKey = address.privateKey2Wif(privateKey, version)
	publicKey = address.privateKey2PublicKey(privateKey)
	publicAddress = address.publicKey2Address(publicKey, version, prefix)
	    
	out.prnt('\n' + currencyLongName + ' Address : ' + publicAddress + '\n\n')	

if __name__ == "__main__":
    generate()
