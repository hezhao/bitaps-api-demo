import os
import sys
import time
import unittest
from nose.tools import assert_true, assert_equal, assert_is_not_none
sys.path.append('../')
from api import coin


class TestCoin(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        cls.coin = coin.Coin()
        cls.api_key = os.getenv('STRIPE_SECRET_KEY', False)
        cls.metadata = {
            'Name': 'Joe Doe',
            'Email address':'payinguser+fill_now@example.com',
            'Shipping address': '123 5th Avenue',
            'City': 'Portland',
            'State': 'OR',
            'Postal Code': '97171',
        }
        assert_is_not_none(cls.api_key)

    def test_create_source(self):
        source = self.coin.create_source(amount_in_cents=123, metadata=self.metadata, email='payinguser+fill_now@example.com')
        assert_is_not_none(source)

    def test_generate_qrcode(self):
        uri = 'bitcoin:test_1MBhWS3uv4ynCfQXF3xQjJkzFPukr4K56N?amount=0.02105448'
        img_uri = self.coin.generate_qrcode(uri)
        assert_is_not_none(img_uri)
