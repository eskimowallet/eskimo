import input.inp as inp

class passW:
    
    password = ''
    
    def setPass(self):
        print('Welcome to eskimo')
        print('To encrypt your database please enter a password')
        print('keep this password safe as it is not stored anywhere')
        print('if you loose it, you will loose all your private keys')
        print('')
        pass1 = 'pass1' 
        pass2 = 'pass2'
        while pass1 != pass2 or len(pass1) < 1:
            pass1 = inp.keyboard_passphrase()
            pass2 = inp.keyboard_passphrase(2)
            if pass1 != pass2:
                print('The passwords entered did not match!')
            elif len(pass1) < 1:
                print('No password was entered!')
        self.password = pass1
        print('password has been set')
        return
    
    def getPass(self):
        while self.password == '':
            self.password = inp.keyboard_passphrase()
            if self.password == '':
                print('no password was entered')
        return self.password
        
    def editPass(self):
        currentpass = raw_input('Enter your current password : ')
        if currentpass != self.password:
            print('incorrect password entered')
            return
        new_pass = raw_input('Enter your new password : ')
        new_pass2 = raw_input('and again : ')
        if new_pass == new_pass2:
            self.password = new_pass
            print('password changed')
        else:
            print('passwords don\'t match')
        return
        
        