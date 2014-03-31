import sqlite3
import os.path


def open():
	return sqlite3.connect('igloo.dat')
	
def close(conn):
	conn.commit()
	conn.close()
	return True
	
def testEnc():
    if not os.path.isfile('igloo.dat'):
        return True
    else:
        return False
        
def testDec():
    if os.path.isfile('igloo.dat'):
        conn = open()
        c = conn.cursor()
        try:
            c.execute('select * from eskimo_versions where id=?;', (1,))
        except sqlite3.Error, e:
            if e.args[0] == 'file is encrypted or is not a database':
                return False
            else:
                print(e)
    else:
        return False
    return True