import requests
import time

base_url = 'https://mempool.space/api'
address = '32ixEdVJWo3kmvJGMTZq5jAQVZZeuwnqzo'

current_time = int(time.time())

timestamp_30_days_ago = current_time - 30 * 24 * 60 * 60
timestamp_7_days_ago = current_time - 7 * 24 * 60 * 60

address_info = requests.get(f'{base_url}/address/{address}').json()
onchain_balance = address_info['chain_stats']['funded_txo_sum'] - address_info['chain_stats']['spent_txo_sum']
mempool_balance = address_info['mempool_stats']['funded_txo_sum'] - address_info['mempool_stats']['spent_txo_sum']

transactions = requests.get(f'{base_url}/address/{address}/txs').json()

variance_30_days_ago = 0
variance_7_days_ago = 0

def calculate_transaction_amount(tx, address):
    amount = 0

    for output in tx['vout']:
        if address in output['scriptpubkey_address']:
            amount += output['value']  

  
    for input_ in tx['vin']:
        if 'prevout' in input_ and address in input_['prevout']['scriptpubkey_address']:
            amount -= input_['prevout']['value']  
    return amount


for tx in transactions:
    if tx['status']['confirmed']:
        block_time = tx['status']['block_time']  
        
      
        if block_time < timestamp_30_days_ago:
            break  
        tx_amount = calculate_transaction_amount(tx, address)
        variance_30_days_ago += tx_amount

for tx in transactions:
    if tx['status']['confirmed']:
        block_time = tx['status']['block_time']  
        
        if block_time < timestamp_7_days_ago:
            break  

        tx_amount = calculate_transaction_amount(tx, address)
        variance_7_days_ago += tx_amount

currentbalanceonbtc = onchain_balance / 100000000
print(f'On-chain Balance: {onchain_balance} SATs / {currentbalanceonbtc} BTC')
print(f'Mempool Balance: {mempool_balance} SATs')
variance30btc = variance_30_days_ago / 100000000
variance7btc = variance_7_days_ago / 100000000

print(f'Variance on Balance 30 days ago: {variance_30_days_ago} SATs / + {variance30btc} BTC')
print(f'Variance on Balance Balance 7 days ago: {variance_7_days_ago} SATs / + {variance7btc} BTC')

