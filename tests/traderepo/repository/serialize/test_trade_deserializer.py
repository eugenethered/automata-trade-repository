import unittest

from core.number.BigFloat import BigFloat
from core.trade.InstrumentTrade import Status, TradeMode

from traderepo.repository.serialize.trade_deserializer import deserialize_trade


class TradeDeserializeTestCase(unittest.TestCase):

    def test_currency_trade_order_deserializes(self):
        raw_trade = {
            'instrument_from': 'OTC',
            'instrument_to': 'BTC',
            'quantity': '10'
        }
        trade = deserialize_trade(raw_trade)
        self.assertEqual(trade.instrument_from, 'OTC')
        self.assertEqual(trade.instrument_to, 'BTC')
        self.assertEqual(trade.quantity, BigFloat('10'))
        self.assertEqual(trade.mode, TradeMode.TRADE, 'should have default trade mode')

    def test_currency_trade_order_deserializes_fraction_quantity(self):
        raw_trade = {
            'instrument_from': 'BTC',
            'instrument_to': 'OTC',
            'quantity': '0.000025'
        }
        trade = deserialize_trade(raw_trade)
        self.assertEqual(trade.instrument_from, 'BTC')
        self.assertEqual(trade.instrument_to, 'OTC')
        self.assertEqual(trade.quantity, BigFloat('0.000025'))

    def test_currency_trade_order_deserializes_with_status_and_description(self):
        raw_trade = {
            'instrument_from': 'OTC',
            'instrument_to': 'BTC',
            'quantity': '10',
            'status': 'cancelled',
            'description': 'cancelled order:11',
        }
        trade = deserialize_trade(raw_trade)
        self.assertEqual(trade.instrument_from, 'OTC')
        self.assertEqual(trade.instrument_to, 'BTC')
        self.assertEqual(trade.quantity, BigFloat('10'))
        self.assertEqual(trade.status, Status.CANCELLED)
        self.assertEqual(trade.description, 'cancelled order:11')

    def test_currency_trade_order_deserializes_with_status_and_description_and_order_id(self):
        raw_trade = {
            'instrument_from': 'OTC',
            'instrument_to': 'BTC',
            'quantity': '10',
            'status': 'executed',
            'description': 'order executed',
            'order_id': '8888-8888'
        }
        trade = deserialize_trade(raw_trade)
        self.assertEqual(trade.instrument_from, 'OTC')
        self.assertEqual(trade.instrument_to, 'BTC')
        self.assertEqual(trade.quantity, BigFloat('10'))
        self.assertEqual(trade.status, Status.EXECUTED)
        self.assertEqual(trade.description, 'order executed')
        self.assertEqual(trade.order_id, '8888-8888')

    def test_currency_trade_order_deserializes_with_price_and_value(self):
        raw_trade = {
            'instrument_from': 'OTC',
            'instrument_to': 'BTC',
            'quantity': '10',
            'price': '1.01',
            'value': '10.1',
            'status': 'executed',
            'description': 'order executed',
            'order_id': '8888-8888',
            'instant': 1
        }
        trade = deserialize_trade(raw_trade)
        self.assertEqual(trade.instrument_from, 'OTC')
        self.assertEqual(trade.instrument_to, 'BTC')
        self.assertEqual(trade.quantity, BigFloat('10'))
        self.assertEqual(trade.price, BigFloat('1.01'))
        self.assertEqual(trade.value, BigFloat('10.1'))
        self.assertEqual(trade.status, Status.EXECUTED)
        self.assertEqual(trade.description, 'order executed')
        self.assertEqual(trade.order_id, '8888-8888')
        self.assertEqual(trade.instant, 1)

    def test_currency_trade_with_predict_mode(self):
        raw_trade = {
            'instrument_from': 'OTC',
            'instrument_to': 'BTC',
            'quantity': '10',
            'price': '1.01',
            'value': '10.1',
            'status': 'executed',
            'mode': 'predict',
            'description': 'order executed',
            'order_id': '8888-8888',
            'instant': 1
        }
        trade = deserialize_trade(raw_trade)
        self.assertEqual(trade.instrument_from, 'OTC')
        self.assertEqual(trade.instrument_to, 'BTC')
        self.assertEqual(trade.quantity, BigFloat('10'))
        self.assertEqual(trade.price, BigFloat('1.01'))
        self.assertEqual(trade.value, BigFloat('10.1'))
        self.assertEqual(trade.status, Status.EXECUTED)
        self.assertEqual(trade.mode, TradeMode.PREDICT)
        self.assertEqual(trade.description, 'order executed')
        self.assertEqual(trade.order_id, '8888-8888')
        self.assertEqual(trade.instant, 1)


if __name__ == '__main__':
    unittest.main()
