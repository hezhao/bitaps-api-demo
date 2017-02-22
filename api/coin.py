import json
import os
import qrcode
import stripe
from cStringIO import StringIO


class Coin():
    """
    Stripe API wrapper to receive bitcoin payment
    """
    def __init__(self):
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY', False)

    def create_source(self, amount_in_cents, metadata, email):
        """
        Create bitcoin payment receiving address and qrcode.
        """
        source = stripe.Source.create(
            type='bitcoin',
            amount=amount_in_cents,
            currency='usd',
            metadata=metadata,
            owner={
                'email':email,
            }
        )
        self.generate_qrcode(source.bitcoin.uri)
        return source

    def create_charge(self, amount, currency, source_id, receipt_email, description, metadata):
        """
        Charge sender when source becomes available.
        This method should be called in the callback, source is retrieved from source.chargeable event payload
        """
        print(metadata)
        charge = stripe.Charge.create(
            amount=amount,
            currency=currency,
            source=source_id,
            receipt_email=receipt_email,
            description=description,
            metadata=metadata)
        return charge

    def create_source_demo(self):
        metadata = {
            'Name': 'Joe Doe',
            'Email address':'payinguser+fill_now@example.com',
            'Shipping address': '123 5th Avenue',
            'City': 'Portland',
            'State': 'OR',
            'Postal Code': '97171',
        }
        return self.create_source(amount_in_cents=123, metadata=metadata, email='foo@bar.com')

    def create_charge_demo(self, source):
        # This method should be called in the callback,
        # source is retrieved from source.chargeable event payload
        return self.create_charge(
            amount=source.amount,
            currency=source.currency,
            source_id=source.id,
            receipt_email=source.owner.email,
            description=source.owner.email,
            metadata=source.metadata)

    def generate_qrcode(self, uri):
        """
        Generate base64 string of QR code for a certain uri.
        """
        img = qrcode.make(uri)
        img.save('out.png')
        output = StringIO()
        img.save(output, format='PNG')
        img_uri = output.getvalue().encode("base64")
        return img_uri


if __name__ == '__main__':
    coin = Coin()
    source = coin.create_source_demo()
    print('source id: ' + source.id)
    raw_input('Waiting payment...')
    charge = coin.create_charge_demo(source)
    print('charge id: ' + charge.id)
