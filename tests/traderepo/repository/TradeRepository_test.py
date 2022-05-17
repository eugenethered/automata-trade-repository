import unittest

from cache.holder.RedisCacheHolder import RedisCacheHolder
from core.number.BigFloat import BigFloat
from core.trade.InstrumentTrade import InstrumentTrade, Status

from traderepo.repository.TradeRepository import TradeRepository


class TradeRepositoryTestCase(unittest.TestCase):

    def setUp(self) -> None:
        options = {
            'REDIS_SERVER_ADDRESS': '192.168.1.90',
            'REDIS_SERVER_PORT': 6379,
            'TRADE_KEY': 'test:trade'
        }
        self.cache = RedisCacheHolder(options)
        self.repository = TradeRepository(options)

    def tearDown(self):
        self.cache.delete('test:trade')

    def test_should_store_and_retrieve_trade(self):
        trade = InstrumentTrade(instrument_from='OTC', instrument_to='GBP', quantity=BigFloat('100.00'), price=BigFloat('1.01'), value=BigFloat('101'), status=Status.SUBMITTED, order_id='88888888')
        self.repository.store_trade(trade)
        stored_trade = self.repository.retrieve_trade()
        self.assertEqual(trade, stored_trade)


if __name__ == '__main__':
    unittest.main()
