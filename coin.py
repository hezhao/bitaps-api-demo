import json
import os
import qrcode
import stripe


class Coin():
    """
    """
    def __init__(self):
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY', False)
        self.source = None

    def create_source(self):
        metadata = dict()
        self.source = stripe.Source.create(type='bitcoin', amount=104, currency='usd',
            metadata={
                'Name': 'Joe Doe',
                'Email address':'joe.doe@example.com',
                'Shipping address': '123 5th Avenue',
                'City': 'Portland',
                'State': 'OR',
                'Postal Code': '97171'
            },
            owner={
                'email':'joe.doe@example.com'
                # 'email': 'payinguser+fill_now@example.com'
            }
        )
        print('source id: ' + self.source.id)
        self.generate_qrcode(self.source.bitcoin.uri)

    def create_charge(self):
        # This method should be called in the callback,
        # source is retrieved from source.chargeable event payload
        charge = stripe.Charge.create(
            amount=self.source.amount,
            currency=self.source.currency,
            source=self.source.id,
            receipt_email=self.source.owner.email,
            description=self.source.owner.email,
            metadata=self.source.metadata)
        print(charge)

    def generate_qrcode(self, uri):
        img = qrcode.make(uri)
        img.save('out.png')


if __name__ == '__main__':
    coin = Coin()
    order = coin.create_source()
    raw_input('Waiting payment...')
    order = coin.create_charge()
