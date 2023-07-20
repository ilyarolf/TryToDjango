import datetime
from concurrent.futures import ThreadPoolExecutor

import requests
from items.models import BuyForCryptoUser


# import grequests
# import requests

class CryptoApiRequest:


    def __threading_get_requests(self, urls):
        responses = list()
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(lambda: requests.get(url)) for url in urls]
            for future in futures:
                response = future.result()
                responses.append(response)
        return responses
    def __get_key_by_value(self, dict: dict, value) -> any:
        reverse_dict = {v: k for k, v in dict.items()}
        key = reverse_dict.get(value)
        return key

    def __get_balances(self, user: BuyForCryptoUser):
        user_addresses = {'BTC': user.btc_address,
                          'LTC': user.ltc_address,
                          'TRX': user.trx_address}
        urls = {'BTC':f'https://blockchain.info/rawaddr/{user_addresses["BTC"]}',
                'LTC':f'https://apilist.tronscan.org/api/account?address={user_addresses["TRX"]}&includeToken=true',
                'USDT':f'https://api.blockcypher.com/v1/ltc/main/addrs/{user_addresses["LTC"]}'}
        responses = self.__threading_get_requests(list(urls.values()))
        crypto_balances = dict()
        for response in responses:
            if response.status_code == 200:
                response = response.json()
                if 'total_received' in response:
                    crypto_name = self.__get_key_by_value(user_addresses, response['address'])
                    crypto_balances[crypto_name] = float(response['total_received']) / 100000000
                else:
                    usdt_balance = None
                    for token in response['trc20token_balances']:
                        if token['tokenName'] == 'Tether USD':
                            usdt_balance = round(float(token['balance']) * pow(10, -token['tokenDecimal']), 6)
                            break
                    if usdt_balance is not None:
                        crypto_balances['USDT'] = usdt_balance
                    else:
                        crypto_balances['USDT'] = 0
            else:
                crypto_balances[self.__get_key_by_value(urls, response.url)] = 0
        return crypto_balances

    def __get_balances_from_db(self, user):
        return {'BTC': user.btc_balance,
                'LTC': user.ltc_balance,
                'USDT': user.usdt_balance}

    def __get_crypto_price(self):
        urls = [f'https://api.coinbase.com/v2/prices/BTC-USD/buy',
                'https://api.coinbase.com/v2/prices/LTC-USD/buy']
        crypto_prices = dict()
        responses = self.__threading_get_requests(urls)
        for response in responses:
            if response.status_code == 200:
                response = response.json()
                crypto_prices[response['data']['base']] = float(response['data']['amount'])
        return crypto_prices

    def refresh_balances(self, user: BuyForCryptoUser):
        old_balances = self.__get_balances_from_db(user)
        new_balances = self.__get_balances(user)
        balances_in_usd = dict()
        if new_balances != old_balances:
            crypto_prices = self.__get_crypto_price()
            for key, value in new_balances.items():
                if key == 'USDT':
                    balances_in_usd[key] = new_balances[key] * 1
                else:
                    balances_in_usd[key] = float(crypto_prices[key] * new_balances[key])
            user.btc_balance = new_balances['BTC']
            user.ltc_balance = new_balances['LTC']
            user.usdt_balance = new_balances['USDT']
            # (format(usd_balance, '.2f')
            user.top_up_amount = float(format(sum(list(balances_in_usd.values())), '.2f'))
            user.last_refresh_balance_datetime = datetime.datetime.now()
            user.save()
