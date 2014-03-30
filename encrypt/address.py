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


def generate(cur, bip=False):
	conn = sqlite3.connect('igloo.dat')
	c = conn.cursor()
	c.execute('select v.version,v.prefix,v.length,c.id,c.longName from eskimo_versions as v inner join eskimo_currencies as c on c.version = v.id where c.currency=?;', (cur.upper(),))
	version = c.fetchone()
	if version is None:
		print(cur.upper() + ' is not currently listed as a currency')
		return False
	privateKey = rand.randomKey(inp.keyboardEntropy())
	publicKey = privateKey2PublicKey(privateKey)
	publicAddress = publicKey2Address(publicKey, version[0], version[1])
	
	c.execute('insert into eskimo_privK (privK, currency, bip) values (?,?,?);', (str(privateKey).encode('base64','strict'), version[3], str(False)))
	privKid = c.lastrowid
	c.execute('insert into eskimo_addresses (address, currency) values (?,?);', (publicAddress.encode('base64','strict'), version[3]))
	addId = c.lastrowid
	c.execute('insert into eskimo_master(address, privK) values (?,?);', (addId, privKid))
	conn.commit()
	conn.close()
	print('')
	print(version[4] + ' Address : ' + publicAddress)
	#uncomment out the line below to show the WIF private key upon creation
	#print(str(privateKey2Wif(privateKey, version[0])))
	return	
	
def dumpPrivKey(addressIn,raw=0):
	conn = sqlite3.connect('igloo.dat')
	c = conn.cursor()
	c.execute('select p.privK,c.longName,v.version from eskimo_privK as p inner join eskimo_master as m on m.privK = p.id inner join eskimo_addresses as a on m.address = a.id inner join eskimo_currencies as c on p.currency = c.id inner join eskimo_versions as v on c.version = v.id where a.address = ?;', (addressIn.encode('base64', 'strict'),))
	privK = c.fetchone()
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
