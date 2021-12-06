# Simple vanity address generator in python
from time import time
from algosdk import account
import algosdk
import time

vanity_private_key, vanity_address = account.generate_account()
prefix = input("Enter a prefix:")
while (not vanity_address.startswith(prefix.upper())):
     vanity_private_key, vanity_address = account.generate_account()

print("Address:", vanity_address)
print("SECURITY WARNING - you will receive you mnemonic shortly")
print("It is VERY important that you don't share your seed phrase with anyone, not even your mum! This controls access to all your funds.")

time.sleep(6)

print(algosdk.mnemonic.from_private_key(vanity_private_key))

input("Press enter to exit...")