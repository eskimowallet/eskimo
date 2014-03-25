from encode import enc
import hashlib
from elip import elip

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
