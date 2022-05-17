import unittest

from core.number.BigFloat import BigFloat
from core.trade.InstrumentTrade import InstrumentTrade, Status

from traderepo.repository.serialize.trade_serializer import serialize_trade


class TradeSerializeTestCase(unittest.TestCase):

    def test_currency_trade_order_serializes(self):
        trade = InstrumentTrade('USDT', 'BTC', BigFloat('10'))
        actual = serialize_trade(trade)
        result = {
            'instrument_from': 'USDT',
            'instrument_to': 'BTC',
            'quantity': '10.0',
            'status': 'new'
        }
        self.assertEqual(actual, result)

    def test_currency_trade_order_serializes_fraction_quantity(self):
        trade = InstrumentTrade('BTC', 'OTC', BigFloat('0.000025'))
        actual = serialize_trade(trade)
        result = {
            'instrument_from': 'BTC',
            'instrument_to': 'OTC',
            'quantity': '0.000025',
            'status': 'new'
        }
        self.assertEqual(actual, result)

    def test_currency_trade_order_serializes_with_status_and_description(self):
        trade = InstrumentTrade('OTC', 'BTC', BigFloat('10'), status=Status.ERROR, description='Not enough funds')
        actual = serialize_trade(trade)
        result = {
            'instrument_from': 'OTC',
            'instrument_to': 'BTC',
            'quantity': '10.0',
            'status': 'error',
            'description': 'Not enough funds'
        }
        self.assertEqual(actual, result)

    def test_currency_trade_order_serializes_with_status_and_value_and_description_and_order_id(self):
        trade = InstrumentTrade('OTC', 'BTC', BigFloat('10'), BigFloat('1.01'), BigFloat('10.1'), Status.EXECUTED, 'Order Executed', '8888-8888', 1)
        actual = serialize_trade(trade)
        result = {
            'instrument_from': 'OTC',
            'instrument_to': 'BTC',
            'quantity': '10.0',
            'price': '1.01',
            'value': '10.1',
            'status': 'executed',
            'description': 'Order Executed',
            'order_id': '8888-8888',
            'interval': 1
        }
        self.assertEqual(actual, result)


if __name__ == '__main__':
    unittest.main()
