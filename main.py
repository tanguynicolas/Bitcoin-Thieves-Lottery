import concurrent.futures

from bitcoinaddress import Wallet
import pandas as pd
import requests

# utxos.csv généré par <https://github.com/in3rsha/bitcoin-utxo-dump>
df_data = pd.read_csv('utxos.csv')
df_sorted = df_data.sort_values('address')

def check_wallet():
    while True:
        # Générer une nouvelle adresse dans plusieurs formats
        wallet = Wallet('9cea6dc004acfe623abcdad9085388497da023cac6a7d1a2d44fddd72a797fec')
        address1 = wallet.address.mainnet.pubaddr1
        address1c = wallet.address.mainnet.pubaddr1c
        address3 = wallet.address.mainnet.pubaddr3
        address1P2WSH = wallet.address.mainnet.pubaddrbc1_P2WSH
        addressP2WPKH = wallet.address.mainnet.pubaddrbc1_P2WPKH

        # Liste des adresses à vérifier
        addresses = [address1, address1c, address3, addressP2WPKH, address1P2WSH]

        count_comparaisons = 0
        # On teste la correspondance de notre adresse avec toutes celles du DataFrame
        for address in addresses:
            count_comparaisons += 1
            matching_rows = df_sorted[df_sorted['address'] == address]

            # Si l'adresse générée correspond à une adresse dans le DataFrame
            if not matching_rows.empty:
                print(f'🏆 Address {address} match!')

                print(wallet)

                # Affichage du nombre de BTC de l'adresse
                amount = float(matching_rows['amount'].values[0])
                print(f"💸 This address has: ₿{amount}")

                # Affichage du cours actuel du BTC en dollar
                response = requests.get("http://api.coindesk.com/v1/bpi/currentprice.json")
                data = response.json()
                rate = float(data['bpi']['USD']['rate'].replace(",", ""))
                print(f"💱 The current price of BTC is: ${rate}")

                # Affichage de la valeur au cours en dollar
                print(f"💰 This private key is worth: ${rate * amount}")

                return
        
        return count_comparaisons

check_wallet()

# Test with:
# Private key: Wallet('9cea6dc004acfe623abcdad9085388497da023cac6a7d1a2d44fddd72a797fec')
# Transaction: 2263674,40492c8b1984b40b2e6098642445691354a583ae7242f37bbc8203e1c941e80a,2,57225,0,218,73d3c582ea649e303e7aae819116ab5ec4f6970f,p2pkh,1GLPoStEnCDYfPokWkQ5HXjoXbFZpmSkKy
