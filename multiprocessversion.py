# Simple vanity address generator in python
import multiprocessing
from time import time
from urllib import parse
from algosdk import account
import algosdk
import time
import re
from multiprocessing import Manager, Process
import os
import argparse


def worker_address_search(i, regexes, q):
    joined = "|".join(regexes)
    print( f"worker {i} searching for {joined}" )
    compiled = re.compile(joined,re.IGNORECASE)

    i = 0

    while 1:
        vanity_private_key, vanity_address = account.generate_account()
        i+=1
        if compiled.match(vanity_address):
            result = f"Address:{vanity_address}\n{algosdk.mnemonic.from_private_key(vanity_private_key)}"
            q.put((True,result))
        else:
            if i%(1237+i)==0:
                q.put((False,i))    # send and update on number of attempts failed

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='awesome algorand vanity address search')
    parser.add_argument('--processes', type=int, default='1', help='number of processes to use')
    parser.add_argument('--regex', type=str)
    args=parser.parse_args()
    print(f"using {args.processes} processes")
    print("SECURITY WARNING - your mnemonic will appear below")
    print("It is VERY important that you don't share your seed phrase with anyone, not even your mum!")
    print("This controls access to all your funds in the wallet")
    
    ps=[]
    #regexes = \
    #["[0-9]?N[O0][O0][B8]",
    #"[0-9x]?NC[O0][I1]N"] 
    regexes=[args.regex]

    with multiprocessing.Pool(processes=args.processes) as pool:
        manager = multiprocessing.Manager()
        q = manager.Queue()
        try:
            for i in range(args.processes):
                workerbees = pool.apply_async( worker_address_search, (i, regexes, q,) )
            start = time.time()
            attempts = 0
            while 1:
                found, result = q.get()
                if found:
                    print( f"{result}" )
                else:
                    attempts += result
                    now = time.time()
                    if now-start > 10:
                        print(f"{attempts}..",end='',flush=True)
                        start = now
        except KeyboardInterrupt:
            pool.close()
            pool.terminate()

