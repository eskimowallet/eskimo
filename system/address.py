import hashlib

import io.inp as inp
import io.out as out
import encrypt.bip38 as bip38
import num.elip as elip
import num.enc as enc
import num.rand as rand
import system.db as db

def privateKey2Wif(privateKey, version=0):
	return base58Encode(enc.encode(privateKey, 256, 32) + '\x01', (128+version))


def privateKey2PublicKey(priv):
    """ integer 256 bit ECC private key to hexstring compressed public key
    """
    pub = elip.base10_multiply(elip.G, priv)
    return '0' + str(2 + (pub[1] % 2)) + enc.encode(pub[0], 16, 64)


def publicKey2Address(publicKey, version=0, prefix=1):
    """ Compressed ECC public key hex to address
    """
    return base58Encode(hashlib.new('ripemd160', hashlib.sha256(publicKey.decode('hex')).digest()).digest(), (0+version), prefix)


def base58Encode(r160, magicbyte=0, prefix=1):
    """ Base58 encoding w leading zero compact
    """
    from re import match as re_match
    inp_fmtd = chr(int(magicbyte)) + r160
    leadingzbytes = len(re_match('^\x00*', inp_fmtd).group(0))
    checksum = hashlib.sha256(hashlib.sha256(inp_fmtd).digest()).digest()[:4]
    return str(prefix) * leadingzbytes + enc.encode(enc.decode(inp_fmtd + checksum, 256), 58, 0)


def generate(cur, bip=False):
    '''
        public and private key generator.
        optional BIP0038 encryption
    '''
    #check that the given currency is in the system
    conn = db.open()
    c = conn.cursor()
    #pull the version details from the database
    c.execute('select v.version,v.prefix,v.length,c.id,c.longName from eskimo_versions as v inner join eskimo_currencies as c on c.version = v.id where c.currency=?;', (cur.upper(),))
    version = c.fetchone()
    if version is None:
        print(cur.upper() + ' is not currently listed as a currency')
        return False
    #generate the private and public keys
    privateKey = rand.randomKey(inp.keyboardEntropy())
    publicKey = privateKey2PublicKey(privateKey)
    publicAddress = publicKey2Address(publicKey, version[0], version[1])
    #optional BIP0038 encryption
    print('creation of a BIP0038 encrypted private key can take a long time (~10 minutes)')
    skip = raw_input('do you want to skip BIP0038 encryption? ').lower().strip()
    if skip == 'n':
        bip38pass1 = 'bip38pass1' 
        bip38pass2 = 'bip38pass2'
        while bip38pass1 != bip38pass2 or len(bip38pass1) < 1:
            bip38pass1 = inp.keyboard_passphrase()
            bip38pass2 = inp.keyboard_passphrase(2)
            if bip38pass1 != bip38pass2:
                print('The passphrases entered did not match!')
            elif len(bip38pass1) < 1:
                print('No passphrase was entered!')
        reminder = raw_input('Enter an optional reminder for your password : ').strip()
        privK = bip38.encrypt(privateKey, publicAddress, bip38pass1, version[0], version[1])
        isBip = True
    else:
        privK = privateKey
        isBip = False
    #save details to the database
    c.execute('insert into eskimo_privK (privK, currency) values (?,?);', (str(privK).encode('base64','strict'), version[3]))
    privKid = c.lastrowid
    c.execute('insert into eskimo_addresses (address, currency) values (?,?);', (publicAddress.encode('base64','strict'), version[3]))
    addId = c.lastrowid
    c.execute('insert into eskimo_master (address, privK) values (?,?);', (addId, privKid))
    if isBip is True:
        c.execute('insert into eskimo_bip (privK, reminder) values (?,?);', (privKid, reminder))
    db.close(conn)
    print('')
    print(version[4] + ' Address : ' + publicAddress)
    return	
	
def dumpPrivKey(addressIn,raw=0):
	conn = db.open()
	c = conn.cursor()
	c.execute('select p.privK,c.longName,v.version from eskimo_privK as p inner join eskimo_master as m on m.privK = p.id inner join eskimo_addresses as a on m.address = a.id inner join eskimo_currencies as c on p.currency = c.id inner join eskimo_versions as v on c.version = v.id where a.address = ?;', (addressIn.encode('base64', 'strict'),))
	privK = c.fetchone()
	db.close(conn)
	if privK is None:
		print('No matching private key was found')
		return False
	if raw == 1:
		print('Raw Private Key for ' + privK[1] + ' address ' + addressIn + ' is:')
		print(str(privK[0]).decode('base64', 'strict'))
	else:
		print('WIF Private Key for ' + privK[1] + ' address ' + addressIn + ' is:')
		print(privateKey2Wif(long(str(privK[0]).decode('base64', 'strict')), privK[2]))
	return 	 
