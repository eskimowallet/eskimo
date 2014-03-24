#!/usr/bin/env python
"""
Bitcoin paper wallet generator v1.2

This code, excepting the MIT-licensed libraries,
is public domain. Everyone has the right to do whatever they want
with it for any purpose.

Also MIT licensed, when needed for redistribution:

The MIT License (MIT)

Copyright (c) 2013 deepceleron of bitcointalk.org
pybitcointools Copyright (c) 2013 Vitalik Buterin
https://github.com/vbuterin/pybitcointools/

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

from random import random
from input import inp
from input import getch










# Address encoding




# Bitcoin compressed address only





# Bitcoin compressed address only - (todo: rewrite due to b58 incompatible with BIP38)







# This is the real program, all that other stuff was just a clever ploy to distract you ;)
from optparse import OptionParser, OptionGroup


def paperwal():
    parser = OptionParser()
    parser.add_option("-e", "--encrypted", action='store_true', dest="encrypted", default=False,
                      help="create BIP38-encrypted privkey (takes a LONG time)")
    parser.add_option("-v", "--validate", action='store_true', dest="validate", default=False,
                      help="enable extensive system tests for entropy")
    parser.add_option("-s", "--silent", action='store_true', dest="silent", default=False,
                      help="disable most console output except address")
    parser.add_option("-l", "--loop", action='store_true', dest="repeat", default=False,
                      help="restart instead of exit")
    parser.add_option("-p", "--nopause", action='store_true', dest="nopause", default=False,
                      help="disable the pause before exiting")
    parser.add_option("-d", "--doublecalc", action='store_true', dest="doublecalc", default=False,
                      help="calculate twice and test results")
    parser.add_option("-z", "", dest='just a helpful hint', default='',
                      help="try ctrl-tab to abort the program")
    entropy_warning = OptionGroup(parser, "Warning",
                                          "If you use this option, you should supply REAL randomly generated entropy. "
                                          "It is probably a good idea not to reuse a seed.")
    entropy_warning.add_option("-r", "--entropy", dest='entropy', default='',
                               help="random seed instead of keypresses, 64+ characters")
    parser.add_option_group(entropy_warning)
    (options, args) = parser.parse_args()

    if options.doublecalc:
        calcs = 2
    else:
        calcs = 1

    if options.entropy and len(options.entropy) < 64:
        prnt('\n** User-supplied seed too short, using keypresses instead\n')
    if options.validate:
        check_rounds = 1000
    else:
        check_rounds = 50
    random.platform_check(check_rounds)
    runcount = 0

    while runcount < 1 or options.repeat:
        bip38pass1 = showpass = ''
        bip38pass2 = 'not equal'

        if options.encrypted:
            while bip38pass1 != bip38pass2 or len(bip38pass1) < 1:
                bip38pass1 = keyboard_passphrase()
                bip38pass2 = keyboard_passphrase(2)
                if bip38pass1 != bip38pass2:
                    prnt('\n** The passphrase entered did not match!\n')
                elif len(bip38pass1) < 1:
                    prnt('\n** No passphrase was entered!\n')

            prnt('\n Show your passphrase before continuing? (y/n)\n')
            getkey = _Getch()
            while True:
                showpass = getkey()
                if showpass != '':
                    break
            if showpass.lower() == 'y' and not options.silent:
                prnt('   Passphrase: (' + bip38pass1 + ')\n')
                pwcounter = '1234567890123456789012345678901234567890'[:len(bip38pass1)]
                prnt('    (counter):  ' + pwcounter + '\n\n')

        if len(options.entropy) > 63:
            userentropy = int(options.entropy.encode('hex'), 16)
        else:
            userentropy = inp.keyboard_entropy(quiet=options.silent)

        privk = random_key(userentropy)
        wallettest = ['', '']
        for loop in xrange(calcs):
            privc = o_priv_wif_c(privk, 48)
            print(base58_to_hex(privc))
            #priv_wif_c = o_b58(encode(privk, 256, 32) + '\x01', ord('\x80'))
            pubc = o_priv_to_pub(privk)
            paper_address = 'Bitcoin Address:\n ' + o_pub_to_addr(pubc, 48) + '\n'
            if not options.encrypted:
                paper_address += 'Private Key:\n ' + privc + '\n'
            else:
                priv_enc = bip38(privk, bip38pass1, options.silent)
                #priv_enc = 'FakePrivateEncryptedKey'  # debugging without waiting 15 minutes
                paper_address += 'Encrypted Private Key:\n ' + priv_enc + '\n'

            wallettest[loop] = paper_address
            # wallettest[1] += 'junk'  # debug - simulate calcuation failure
            if loop > 0:
                if wallettest[loop] != wallettest[loop-1]:
                    print("### CALCULATION FAILURE DETECTED - DO NOT USE ###")
                    prnt("### CALCULATION FAILURE DETECTED - DO NOT USE ###\n")
            else:
                prnt('\n' + paper_address + '\n')
        runcount += 1

    if not options.nopause:
        raw_input('Press "Enter" to close')


if __name__ == "__main__":
    paperwal()
