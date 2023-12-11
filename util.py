import os
import bcrypt
import pwinput

from cryptography.fernet import Fernet
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

#Dict = dict({})

#-------------------------------------------------------------------------------#
def checkPasswd(passwd, hashed1, check, hashed2):
    if bcrypt.checkpw(passwd, hashed1) == True and bcrypt.checkpw(check, hashed2) == True and passwd == check:
        print("Passwords Match.\nUser Registered.\nExiting SecureDrop.")
        return bytes(hashed1)
    else:
        print("Passwords do not match")
        checkP = pwinput.pwinput("Please Re-enter Password: ").encode()
        checksalt = bcrypt.gensalt()
        checkHash = bcrypt.hashpw(checkP, checksalt)
        return checkPasswd(passwd, hashed1, checkP, checkHash)      
#-------------------------------------------------------------------------------#
def checkDBEmpty(filename):
    return os.stat(filename).st_size
#-------------------------------------------------------------------------------#
def generateKey():
    key = Fernet.generate_key()
    with open("Key.pem", "wb") as file:
        file.write(key)
        file.close()
#-------------------------------------------------------------------------------#
def getKey():
    return open("Key.pem", "rb").read()
#-------------------------------------------------------------------------------#
def encryptFile(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()
        file.close()
    encrypt = f.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypt)
        file.close()
#-------------------------------------------------------------------------------#
def decryptFile(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        dataEncrypt = file.read()
        file.close()
    dataDecrypted = f.decrypt(dataEncrypt)
    with open(filename, "wb") as file:
        file.write(dataDecrypted)
        file.close()
#-------------------------------------------------------------------------------#
def getPassword():
    passwd = pwinput.pwinput("Enter Password: ", mask='*').encode()
    return passwd
#-------------------------------------------------------------------------------#
def getReEnterPassword():
    reenter = pwinput.pwinput("Re-enter Password: ", mask='*').encode()
    return reenter