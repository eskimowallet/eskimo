from rand import rand
from input import get
from output import out
import hashlib

def keyboard_passphrase(turn=0):
	progress_step = 0
	pretty_progress = ['\b*', '\bo', '\bO']
	keypress = get._Getch()
	single_key = passw = ''
	msg = ' Enter your passphrase (will not appear)......'
	if turn != 0:
	    msg = ' Re-enter to verify your passphrase......'
	print(msg)
	
	while single_key != "\n" and single_key != chr(13):
	    while True:
	        single_key = keypress()
	        if single_key != '':
	            break
       
	    if single_key != "\n" and single_key != chr(13):
	        passw += single_key
	    print(pretty_progress[progress_step % 3])
	    progress_step += 1
	print('\b')
	return passw
	
def keyboardEntropy(keynum=64):
    """
    512 bit random number from keyboard and keypress timer
    """

    keypress = get._Getch()
    typed = kr = 'Press some keys to generate a secure address........\n'
    hashes = rand.clockrnd()
    out.prnt(kr)
    for step in range(keynum, 0, -1):
        for cnt in xrange(10000000):  # only loops on OSX
            hashes ^= rand.clockrnd()
            kr = keypress()
            if kr != '':
                break
        typed += kr
        hashes ^= rand.clockrnd()
        out.prnt('\b\b\b\b\b\b{0:4d}'.format(step-1))
    out.prnt('\nOK\n')
    return hashes ^ int(hashlib.sha512(typed*8).hexdigest(), 16)
