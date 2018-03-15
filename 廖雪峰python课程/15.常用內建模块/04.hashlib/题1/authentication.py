import getpass
import hashlib
import json

def sigh_up(username,password):
    global Auth_file
    try:
        Auth_file=open('.\\passwd.txt','r')
        Auth_json_dict=json.load(Auth_file)
        Auth_file.close()
        Auth_file=open('.\\passwd.txt','w+')
        if username not in Auth_json_dict:
            Auth_json_dict.update({username:password})
            Auth_file.seek(0)
            json.dump(Auth_json_dict,Auth_file)
            print 'Create the account successful.'
        else:
            print '%s is exist.' % username
            return False
    finally:
        Auth_file.close()
def sigh_in(username,password):
    global Auth_file
    try:
        Auth_file=open('.\\passwd.txt','r')
        Auth_json_dict = json.load(Auth_file)
        if username in Auth_json_dict and Auth_json_dict[username]==password:
            print 'Now logining...'
            #time.sleep(1)
            print 'Login successful.'
        else:
            print 'Incorrect username or password.'
            return False
    finally:
        Auth_file.close()
def encrypt(username,password):
    salt='The_Salt_$3'
    md5=hashlib.md5()
    md5.update(password)
    md5.update(salt)
    md5.update(username)
    return md5.hexdigest()
if __name__=='__main__':
    sigh_in_flag=raw_input('Do you have an account? (Y/N): ')
    if sigh_in_flag.upper()=='N':
        print 'Create an account...'
        username=raw_input('Username: ')
        password=getpass.getpass()
        c_password=getpass.getpass(prompt='Confirm Password: ')
        if password==c_password:
            password_md5=encrypt(username,password)
            sigh_up(username,password_md5)
        else:
            print 'The twice importations of passwords are inconsistent'
    elif sigh_in_flag.upper()=='Y':
        print 'Now login...'
        username=raw_input('Username: ')
        password=getpass.getpass()
        password_md5=encrypt(username,password)
        sigh_in(username,password_md5)
