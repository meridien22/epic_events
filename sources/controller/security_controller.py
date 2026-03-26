from private.parameter import parameter
from cryptography.hazmat.primitives import serialization

def get_private_key_ssh():
    pwd = parameter["ssh_private_key_password"]
    private_key = open(parameter["ssh_private_key_file"], 'r').read()
    return serialization.load_ssh_private_key(
         private_key.encode(), 
         password=pwd.encode('utf-8')
    )

def get_public_key_ssh():
    public_key = open(parameter["ssh_public_key_file"], 'r').read()
    return serialization.load_ssh_public_key(
         public_key.encode()
    )