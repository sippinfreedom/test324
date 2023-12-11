import yaml
import util

#-------------------------------------------------------------------------------#
def add_contact(contact_file, name, email):
    try:
        with open(contact_file, 'r') as file:
            contacts = yaml.safe_load(file) or {}
    except FileNotFoundError:
        contacts = {}

    # Email as the key, name as the value
    contacts[email] = name

    with open(contact_file, 'w') as file:
        yaml.dump(contacts, file)

    print(f"Contact with email {email} added/updated.")
#-------------------------------------------------------------------------------#
def helpcmd():
    print("\t\"add\"  -> Add an new contact\n"
          "\t\"list\" -> List all online contacts\n"
          "\t\"send\" -> Transfer file to contact\n"
          "\t\"exit\" -> Exit SecureDrop")
    return 0

def addcmd():
    name = input("Enter contact's name: ")
    email = input("Enter contact's email: ").lower()
    add_contact("contacts.yaml", name, email)

def add_contact(contact_file, name, email):

    try:
        util.decryptFile(contact_file, util.getKey())
    except:
        #this will be triggered everytime when a user starts the program when the files are empty
        pass

    try:
        with open(contact_file, 'r') as file:
            contacts = yaml.safe_load(file) or {}
    except FileNotFoundError:
        contacts = {}

   
    if len(contacts) == 0:
        contacts[email] = name
        print(f"Contact with email {email} added/updated.")

    else:
        ct = list(contacts) #this is not used
        i = 0

        for emails,names in contacts.items():
            if names == name and emails == email:
                print('User + Email already present.')
                break
            elif (names == name and emails != email) or (names != name and emails == email):
                contacts.pop(emails)
                contacts[email] = name
                print(f"Contact with email {email} added/updated.")
                break
            elif i + 1 == len(contacts):
                contacts[email] = name
                print(f"Contact with email {email} added/updated.")
                break
            i+= 1


    with open(contact_file, 'w') as file:
        yaml.dump(contacts, file)
    
    util.encryptFile("contacts.yaml", util.getKey())
    

def listcmd():
    #current status is for viewing contact list as it stands
    #to be updated in next milestones to be only online contacts
    view_contacts("contacts.yaml")

def view_contacts(contact_file):
    util.decryptFile("contacts.yaml", util.getKey())
    
    try:
        with open(contact_file, 'r') as file:
            contacts = yaml.safe_load(file) or {}
        if not contacts:
            print("No contacts available.")
            return
        for email, name in contacts.items():
            print(f"{name}: {email}")
    except FileNotFoundError:
        print("Contact file not found.")
    
    util.encryptFile("contacts.yaml", util.getKey())


def sendcmd():
    #to be added in future milestone
    return 0

def switch(cmd):
    match cmd:
        case "help":
            helpcmd()
        case "add":
            addcmd()
        case "list":
            listcmd()
        case "send":
            sendcmd()

#-------------------------------------------------------------------------------#
def secureDrop():
    print("Type \"help\" For Commands\n")
    cmd = input("secure_drop> ")
    while cmd != "exit":
        switch(cmd)
        cmd = input("secure_drop> ")
    print("Exiting SecureDrop")
    return 0