# Address encoding

# Bitcoin compressed address only

# Bitcoin compressed address only - (todo: rewrite due to b58 incompatible with BIP38)

# This is the real program, all that other stuff was just a clever ploy to distract you ;)
#from optparse import OptionParser, OptionGroup

#parser = OptionParser()
	#parser.add_option("-e", "--encrypted", action='store_true', dest="encrypted", default=False,
	#                  help="create BIP38-encrypted privkey (takes a LONG time)")
	#parser.add_option("-v", "--validate", action='store_true', dest="validate", default=False,
	#                  help="enable extensive system tests for entropy")
	#parser.add_option("-s", "--silent", action='store_true', dest="silent", default=False,
	#                  help="disable most console output except address")
	#parser.add_option("-l", "--loop", action='store_true', dest="repeat", default=False,
	#                  help="restart instead of exit")
	#parser.add_option("-p", "--nopause", action='store_true', dest="nopause", default=False,
	#                  help="disable the pause before exiting")
	#parser.add_option("-d", "--doublecalc", action='store_true', dest="doublecalc", default=False,
	#                  help="calculate twice and test results")
	#parser.add_option("-z", "", dest='just a helpful hint', default='',
	#                  help="try ctrl-tab to abort the program")
	#entropy_warning = OptionGroup(parser, "Warning",
	#                                      "If you use this option, you should supply REAL randomly generated entropy. "
	#                                      "It is probably a good idea not to reuse a seed.")
	#entropy_warning.add_option("-r", "--entropy", dest='entropy', default='',
	#                           help="random seed instead of keypresses, 64+ characters")
	#parser.add_option_group(entropy_warning)
	#(options, args) = parser.parse_args()

	#if options.doublecalc:
	#    calcs = 2
	#else:
	#    calcs = 1

	#if options.entropy and len(options.entropy) < 64:
	#    prnt('\n** User-supplied seed too short, using keypresses instead\n')
	#if options.validate:
	#    check_rounds = 1000
	#else:
	#    check_rounds = 50
	
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
		
	paper_address = 'Bitcoin Address:\n ' + address.o_pub_to_addr(pubc, 48) + '\n'
	    if not options.encrypted:
		paper_address += 'Private Key:\n ' + privc + '\n'
	    else:
		priv_enc = bip38(privk, bip38pass1, options.silent)
		#priv_enc = 'FakePrivateEncryptedKey'  # debugging without waiting 15 minutes
		paper_address += 'Encrypted Private Key:\n ' + priv_enc + '\n
