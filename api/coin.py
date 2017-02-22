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
        charge = stripe.Charge.create(
            amount=amount,
            currency=currency,
            source=source_id,
            receipt_email=receipt_email,
            description=description,
            metadata=metadata)
        return charge

    def generate_qrcode(self, uri):
        """
        Generate base64 string of QR code for a certain uri.
        """
        img = qrcode.make(uri)
        # Save image to disk with img.save('out.png')
        output = StringIO()
        img.save(output, format='PNG')
        img_uri = output.getvalue().encode("base64")
        return img_uri
