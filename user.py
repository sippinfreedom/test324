import bcrypt
import base64
import yaml
import pwinput

import util
import shell

def createuser():
    fname = input("Enter Full Name: ")
    email = input("Enter Email Address: ").lower()

    passwd = util.getPassword()
    if len(passwd) < 8:
        while len(passwd) < 8:
            print("Password MUST be 8 or more characters")
            passwd = util.getPassword()
    salt = bcrypt.gensalt()
    hashed1 = bcrypt.hashpw(passwd, salt)

    check = util.getReEnterPassword()
    salt2 = bcrypt.gensalt()
    hashed2 = bcrypt.hashpw(check, salt2)

    truePass = util.checkPasswd(passwd, hashed1, check, hashed2)

    user = {}
    user['Name'] = fname
    user['Email'] = email
    user['Password'] = truePass
    return user
#-------------------------------------------------------------------------------#
def initialUserCreation():
    yn = input("No users are registered with this client.\nDo you want to register a new user (y/n)? ")
    if yn.lower() == "y":
        #salt = bcrypt.gensalt()
        userData = createuser() #createuser(salt)
        with open("ud.yaml", "w") as file:
            # Encode the password in base64 to store as a string
            userData['Password'] = base64.b64encode(userData['Password']).decode('utf-8')
            yaml.dump([userData], file)  # Store as a list of users
            file.close()
        util.encryptFile("ud.yaml", util.getKey())
    elif yn.lower() == "n":
        print("Exiting SecureDrop")
        exit()  # Use exit() to terminate the program
#-------------------------------------------------------------------------------#
def userLoginIn():
    eIn = input("Enter Email Address: ").lower()
    pIn = pwinput.pwinput("Enter Password: ").encode()
    util.decryptFile("ud.yaml", util.getKey())
    # Load user data from 'ud.yaml'
    with open("ud.yaml", 'r') as file:
        stored_user_data = yaml.safe_load(file)

    # Assuming stored_user_data is a list of users
    user_entry = next((item for item in stored_user_data if item["Email"] == eIn), None)
    
    if user_entry:
        # Decode the base64 encoded password
        stored_password = base64.b64decode(user_entry['Password'])
        # Verify the password
        if bcrypt.checkpw(pIn, stored_password):
            print("Welcome to SecureDrop")
            util.encryptFile("ud.yaml", util.getKey())
            shell.secureDrop()  # Proceed to secureDrop if login is successful
        else:
            print("Email and Password Combination Invalid.")
            util.encryptFile("ud.yaml", util.getKey()) 
            userLoginIn()  # Only call itself if login fails
    else:
        print("Email not found.")
        util.encryptFile("ud.yaml", util.getKey())
        userLoginIn()  # Only call itself if email is not found


#-------------------------------------------------------------------------------#