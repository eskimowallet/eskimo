import io.inp as inp
import time

class passW:
    
    password = ''
    
    def setPass(self):
        print('Welcome to eskimo')
        time.sleep(1)
        print('To encrypt your database please enter a password')
        time.sleep(2)
        print('keep this password safe as it is not stored anywhere')
        time.sleep(2)
        print('if you loose it, you will loose all your private keys')
        print('')
        time.sleep(2)
        pass1 = 'pass1' 
        pass2 = 'pass2'
        while pass1 != pass2:
            pass1 = inp.secure_passphrase('Enter your database encryption password')
            pass2 = inp.secure_passphrase('Enter it again to confirm' )
            if pass1 != pass2:
                print('The passwords entered did not match!')
        self.password = pass1
        print('password has been set')
        return
    
    def getPass(self):
        self.password = inp.secure_passphrase('Enter your database password to decrypt the database')
        return self.password
        
    def editPass(self):
        currentpass = inp.secure_passphrase('Enter your current password : ')
        if currentpass != self.password:
            print('incorrect password entered')
            return
        new_pass = inp.secure_passphrase('Enter your new password : ')
        new_pass2 = inp.secude_passphrase('Enter it again to confirm : ')
        if new_pass == new_pass2:
            self.password = new_pass
            print('password changed')
        else:
            print('passwords don\'t match')
        return
        
        
