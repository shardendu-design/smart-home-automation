import os
import binascii

def generate_secret_key():
    return binascii.hexlify(os.urandom(32)).decode()

# Generate a key and print it
print(generate_secret_key())
