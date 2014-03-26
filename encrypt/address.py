from encode import enc
import hashlib
from elip import elip
from rand import rand
from input import inp
from output import out
import sqlite3

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


def sxor(s1, s2):
    """ XOR strings
    """
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))
    
 
def generate(cur):
	conn = sqlite3.connect('eskimo.db')
	c = conn.cursor()
	c.execute('select v.version,v.prefix,v.length,c.id,c.longName from eskimo_versions as v inner join eskimo_currencies as c on c.version = v.id where c.currency=?;', (cur.upper(),))
	version = c.fetchone()
	if version is None:
		out.prnt('\n' + cur.upper() + ' is not currently listed as a currency\n\n')
		return False
	privateKey = rand.randomKey(inp.keyboardEntropy())
	publicKey = privateKey2PublicKey(privateKey)
	publicAddress = publicKey2Address(publicKey, version[0], version[1])
	
	c.execute('insert into eskimo_privK (privK, currency) values (?,?);', (str(privateKey).encode('base64','strict'), version[3]))
	privKid = c.lastrowid
	c.execute('insert into eskimo_addresses (address, currency) values (?,?);', (publicAddress.encode('base64','strict'), version[3]))
	addId = c.lastrowid
	c.execute('insert into eskimo_master(address, privK) values (?,?);', (addId, privKid))
	conn.commit()
	conn.close()    
	out.prnt('\n' + version[4] + ' Address : ' + publicAddress + '\n\n')
	out.prnt(str(privateKey2Wif(privateKey, version[0])) + '\n\n')
	return	
	
def dumpPrivKey():
	addressIn = raw_input('Enter the address for which you want to see the private key : ')
	conn = sqlite3.connect('eskimo.db')
	c = conn.cursor()
	c.execute('select p.privK,c.longName,v.version from eskimo_privK as p inner join eskimo_master as m on m.privK = p.id inner join eskimo_addresses as a on m.address = a.id inner join eskimo_currencies as c on p.currency = c.id inner join eskimo_versions as v on c.version = v.id where a.address = ?;', (addressIn.encode('base64', 'strict'),))
	privK = c.fetchone()
	if privK is None:
		out.prnt('\nNo matching private key was found\n')
		return False
	out.prnt('\nPrivate Key for ' + privK[1] + ' address ' + addressIn + ' is:\n\n')
	out.prnt(privateKey2Wif(long(str(privK[0]).decode('base64', 'strict')), privK[2]) + '\n\n')
	return 	 
