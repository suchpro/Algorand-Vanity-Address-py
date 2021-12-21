# Simple vanity address generator in python
from time import time
from algosdk import account, mnemonic
from algosdk.v2client import algod
import time

vanity_private_key, vanity_address = account.generate_account()
prefix = input("Enter a prefix:")
while (not vanity_address.startswith(prefix.upper())):
     vanity_private_key, vanity_address = account.generate_account()

print("Address:", vanity_address)
print("SECURITY WARNING - you will receive you mnemonic shortly")
print("It is VERY important that you don't share your seed phrase with anyone, not even your mum! This controls access to all your funds.")

time.sleep(6)

print(mnemonic.from_private_key(vanity_private_key))


existingmnemonic = input("Enter mnemonic to rekey..")

existing_private_key = mnemonic.to_private_key(existingmnemonic)
existing_address = account.address_from_private_key(existing_private_key)

input("By default, this vanity address finder will use a purestake node to use AlgoD. This node has a hard limit on the amount of transactions on mainnet. Feel free to change the node ip and token. (press any key to continue)")

# node details - purestake
algod_address = "https://mainnet-algorand.api.purestake.io/ps2"
algod_token = input("Purestake api key")
headers = {
   "X-API-Key": algod_token,
}
algod_client = algod.AlgodClient(algod_token, algod_address, headers)

from algosdk import transaction
params = algod_client.suggested_params()
txn_rekey = transaction.PaymentTxn(vanity_address, params.min_fee, params.first, params.last, params.gh, vanity_address, 0, rekey_to=existing_address)
input("Please press enter after you have sent 0.41 algos to the vanity address")
stxn_rekey = txn_rekey.sign(vanity_private_key)
tx = algod_client.send_transaction(stxn_rekey)
print(tx)