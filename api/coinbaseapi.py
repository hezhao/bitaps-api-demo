import json
import qrcode
from coinbase.wallet.client import Client


class Coin():
    """
    """
    def __init__(self):
        API_KEY = os.getenv('COINBASE_API_KEY', False)
        API_SECRET = os.getenv('COINBASE_API_SECRET', False)
        self.client = Client(API_KEY, API_SECRET)
        self.primary_account = self.client.get_primary_account()

    def list_accounts(self):
        accounts = self.client.get_accounts()
        for account in accounts.data:
            balance = account.balance
            print('{0}: {1} {2}'.format(account.name, balance.amount, balance.currency))
            print(account.get_transactions)

    def create_account(self, wallet_name):
        account = self.client.create_account(name=wallet_name)
        balance = account.balance
        print('{0}: {1} {2}'.format(account.name, balance.amount, balance.currency))

    def create_order(self):
        metadata = dict()
        metadata['name'] = 'Joe Doe'
        metadata['email'] = 'joe.doe@gmail.com'
        metadata['shipping_address'] = '123 5th Avenue, Portland OR 97171'
        order = self.client.create_order(amount='0.00000108', currency='BTC', name='Order #0108', description='Awesome energy bar', metadata=metadata)
        self.generate_qrcode(order.bitcoin_uri)
        print(order)
        return order

    def generate_qrcode(self, uri):
        img = qrcode.make(uri)
        img.save('out.png')

    def get_order(self, order_id):
        order = self.client.get_order(order_id)
        print(order)

    def list_orders(self):
        orders = self.client.get_orders().data
        for order in orders:
            print(json.dumps(order))
            # print('{0}: {1} {2} {3} {4}'.format(order.id, order.created_at, order.status, order.bitcoin_amount, order.name))

    def receive_money(self):
        address = self.primary_account.create_address()
        print(address)

    def request_money(self):
        self.primary_account.request_money(to="zhao.he@wk.com", amount="1", currency="BTC")

    def get_account_balance(self):
        balance = self.primary_account.balance
        print(balance)

    def list_transactions(self):
        transactions = self.primary_account.get_transactions().data
        for transaction in transactions:
            print('{0} {1}: {2} {3} {4}'.format(transaction.id, transaction.created_at, transaction.type, transaction.amount, transaction.status))

    def get_latest_transaction(self):
        transactions = self.primary_account.get_transactions().data
        if len(transactions):
            transaction = transactions[-1]
            print('{0} {1}: {2} {3} {4}'.format(transaction.id, transaction.created_at, transaction.type, transaction.amount, transaction.status))

    def list_notifications(self):
        print(self.client.get_notifications())


if __name__ == '__main__':
    coin = Coin()
    order = coin.create_order()
    # order = coin.list_orders()
    # coin.get_order('ea154ead-99ad-5f4f-81a1-a96d64f8fc95')
    # coin.bitaps()
    # coin.list_notifications()
    # coin.list_accounts()
    # coin.get_account_balance()
    # coin.get_notifications()
    # coin.request_money()
    # coin.list_transactions()
    # coin.create_account("Robot Wallet")
