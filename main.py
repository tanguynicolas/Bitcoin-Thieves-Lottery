import concurrent.futures
import threading
from bitcoinaddress import Wallet
import pandas as pd
import requests

print("Import datas.")
# utxos.csv généré par <https://github.com/in3rsha/bitcoin-utxo-dump>
df_data = pd.read_csv('../utxodump.csv')
print('Create dictionnary...')
address_amount_dict = dict(zip(df_data['address'], df_data['amount']))
print('Finish to create dictionnary')
total_tested_private_keys = 0
lock = threading.Lock()

def check_wallet(): 
    global total_tested_private_keys
    tested_private_keys = 0
    while True:
        # Générer une nouvelle adresse dans plusieurs formats
        wallet = Wallet()
        address1 = wallet.address.mainnet.pubaddr1
        address1c = wallet.address.mainnet.pubaddr1c
        address3 = wallet.address.mainnet.pubaddr3
        address1P2WSH = wallet.address.mainnet.pubaddrbc1_P2WSH
        addressP2WPKH = wallet.address.mainnet.pubaddrbc1_P2WPKH

        # Liste des adresses à vérifier
        addresses = [address1, address1c, address3, addressP2WPKH, address1P2WSH]

        # On teste la correspondance de notre adresse avec toutes celles du DataFrame
        for address in addresses:
            if address in address_amount_dict:
                # Affichage du nombre de BTC de l'adresse
                amount = float(address_amount_dict[address])
                print("💸 Find {address} : ₿{amount}\n")

                # Affichage du cours actuel du BTC en dollar
                response = requests.get("http://api.coindesk.com/v1/bpi/currentprice.json")
                data = response.json()
                rate = float(data['bpi']['USD']['rate'].replace(",", ""))
                print(f"💱 The current price of BTC is: ${rate}")

                # Affichage de la valeur au cours en dollar
                print(f"💰 This private key is worth: ${rate * amount}")
                
                with lock:
                    with open('resultat.txt', 'a') as f:
                        f.write(f'Address {address} match!\n')
                        f.write(str(wallet) + '\n')
                        f.write(f"This address has: ₿{amount/1000000}\n")
                        f.write(f"The current price of BTC is: ${rate}\n")
                        f.write(f"This private key is worth: ${rate * (amount/1000000)}\n")
        
        tested_private_keys += 1
        with lock:
            total_tested_private_keys += 1

        if total_tested_private_keys % 100 == 0:
            print(f"Total tested private keys: {total_tested_private_keys}")


print("Initialize threads")
num_threads = 16
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    for _ in range(num_threads):
        executor.submit(check_wallet)
        print(f"Start brute force for thread : {_}")

# Test with:
# Private key: 9cea6dc004acfe623abcdad9085388497da023cac6a7d1a2d44fddd72a797fec
# Transaction: 2263674,40492c8b1984b40b2e6098642445691354a583ae7242f37bbc8203e1c941e80a,2,57225,0,218,73d3c582ea649e303e7aae819116ab5ec4f6970f,p2pkh,1GLPoStEnCDYfPokWkQ5HXjoXbFZpmSkKy
