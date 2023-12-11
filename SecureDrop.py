import os

import util
import user

from Crypto.Cipher import PKCS1_OAEP


#-------------------------------------------------------------------------------#
if os.path.exists("Key.pem") == 0:
    util.generateKey()

if util.checkDBEmpty("ud.yaml") == 0:
    user.initialUserCreation()
else:
    user.userLoginIn()
